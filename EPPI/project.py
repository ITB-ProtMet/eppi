# -*- coding: utf-8 -*-
# Copyright 2015 Pietro Brunetti <pietro.brunetti@itb.cnr.it>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Containing files tree class, to organize projects """

__authors__ = "Pietro Brunetti"

import os
import shutil
import io
import json
import raw.data_input as data_input

class project_error(Exception):
    pass

class DecodeError(project_error):
    """
    Dictionary keys have not correspondence with object parameters
    """
    pass

class DictDB(dict):
    """
    It is a DRM based on a dict-class and using  json format.
    This code is based on an Raymond Hettinger's `recipe`_.
    Wed, 4 Feb 2009 (MIT)

    :ivar filename: the db filename
    :ivar flag: type of action:
        * r=readonly,
        * c=create (if file exists open), or
        * n=new (if file exists truncate)
    :ivar mode: the permission, you can choose None or octal triple like 0x666

    .. _`recipe`:
        http://code.activestate.com/recipes/576642/
    """

    def __init__(self, filename, flag=None, mode=None, *args, **kwds):
        self.flag = flag or 'c'             # r=readonly, c=create, or n=new
        self.mode = mode                    # None or octal triple like 0x666

        self.filename = filename

        if flag != 'n' and os.access(filename, os.R_OK):
            file_handle = io.open(filename, 'rb')

            try:
                self.load(file_handle)
            except OSError:
                if flag == 'n' and os.access(filename, os.W_OK):
                    os.remove(filename)
                else:
                    raise OSError, 'File exists: {0}'.format(os.path.abspath(filename))
            finally:
                file_handle.close()
        self.update(*args, **kwds)

    def sync(self):
        """
        Synchronizes the dictionary with serialized file

        All changes are tried to a temporary file before
        """
        if self.flag == 'r':
                return
        filename = self.filename
        tempname = '{0}.tmp'.format(filename)
        file_handle = io.open(tempname, 'wb')
        try:
            self.dump(file_handle)
        except Exception:
            file_handle.close()
            os.remove(tempname)
            raise
        file_handle.close()
        shutil.move(tempname, self.filename)    # atomic commit
        if self.mode is not None:
            os.chmod(self.filename, self.mode)

    def close(self):
        self.sync()

    # --
    # the following two magic methods permits
    # whit as block
    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()
    # --

    def dump(self, file_name):
        try:
            json.dump(
                self,
                file_name,
                separators=(',', ':'),
                sort_keys=True,
                indent=4
            )
        except TypeError:
            # to determine how serialization fault
            for k,v in self.iteritems():
                try:
                    print k
                    json.dumps(
                        v,
                        sort_keys=True,
                        indent=4,
                        separators=(',', ': ')
                    )
                except TypeError:
                    print "TypeError ", v



    def load(self, file_name):
        try:
            return self.update(json.load(file_name))
        except Exception:
            pass
        raise ValueError('File not in recognized format')

def dbopen(filename, flag=None, mode=None):
    """
    A facade for the previous class DictDB

    >>> s = dbopen('tmp.shl', flag='n')
    >>> print s, 'start'
    {} start
    >>> s['abc'] = '123'
    >>> s['num'] = 10000
    >>> s.close()
    >>> print s
    {'abc': '123', 'num': 10000}
    >>> import io
    >>> f = io.open('tmp.shl', 'rb')
    >>> print f.read()
    {
        "abc":"123",
        "num":10000
    }
    >>> f.close()
    """
    return DictDB(filename, flag, mode)

class EPPI_DictDB(DictDB):
    """
    A version that:
        * create also a folder to store the file and
        * must have defined keyword to use imposed
        * files: - the files added to the project
    """
    def __init__(self, filename, flag='c', mode=None, *args, **kwds):

        if flag == 'n':
            filename = os.path.abspath(filename)
            # this part is for create a
            # a folder with the same name
            # of the file, where store it.
            old_folder, only_file = os.path.split(filename)
            folder_name = os.path.splitext(only_file)[0]
            new_folder = os.path.join(old_folder, folder_name)
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)
            filename = os.path.join(new_folder, only_file)
            DictDB.__init__(self, filename, flag, mode, *args, **kwds)
            self.__setitem__("files", [])
        else:
            DictDB.__init__(self, filename, flag=flag, mode=mode,  *args, **kwds)

    def append_file(self, f):
        """
        Adds a file inside project file list

        >>> foo = EPPI_DictDB('bar.prj', flag='n')
        >>> print foo
        {'files': []}
        >>> import io
        >>> baz = io.open('bar/quux', 'w')
        >>> baz.close()
        >>> foo.append_file("quux")
        >>> print foo
        {'files': ['quux']}
        >>> import os
        >>> os.unlink('bar/quux')

        :param f: the file to append
        :raises IOError: if the f is not in the path
        """
        filepath = os.path.join(self.get_project_dir(), f)
        if not os.path.exists(filepath):
            msg = "[Errno 2] No such file or directory: {0}"
            raise IOError, msg.format(filepath)
        temp = self.__getitem__("files")
        temp.append(f)
        self.__setitem__("files",temp)

    def extend_files(self, files):
        """
        Adds more files inside project file list

        >>> foo = EPPI_DictDB('bar.prj', flag='n')
        >>> print foo
        {'files': []}
        >>> import io
        >>> baz = io.open('bar/quux', 'w')
        >>> baz.close()
        >>> baz = io.open('bar/quuz', 'w')
        >>> baz.close()
        >>> foo.extend_files(["quux", "quuz"])
        >>> print foo
        {'files': ['quux', 'quuz']}
        >>> import os
        >>> os.unlink('bar/quux')
        >>> os.unlink('bar/quuz')

        :param files: the files for extending
        :raises IOError: if any file is not in the path
        exist
        """
        not_here = lambda x: not(os.path.exists(os.path.join(self.get_project_dir(), x)))
        if any(not_here(f) for f in files):
            files_list = ', '.join([each_file for each_file in files if os.path.exists(each_file)])
            msg = "[Errno 2] No such files or directories: {0}"
            raise IOError, msg.format(files_list)

        temp = self.__getitem__("files")
        temp.extend(files)
        self.__setitem__("files",temp)

    def get_project_name(self):
        """
        To obtain the project name

        >>> s = EPPI_dbopen('tmp.prj', flag='n')
        >>> print s.get_project_name()
        tmp

        :return project_name: the name of the project
        """

        #print dir(self)
        return os.path.splitext(os.path.basename(self.filename))[0]

    def get_project_dir(self):
        """
        To obtain the project directory

        >>> from os import curdir
        >>> import os.path as path
        >>> from os.path import abspath
        >>> s = EPPI_dbopen('tmp.prj', flag='n')
        >>> s.get_project_dir() == path.join(abspath(curdir), 'tmp')
        True

        :return project_name: the directory of the project
        """
        return os.path.split(os.path.abspath(self.filename))[0]

    def set_parser(self, p):
        """
        Add parser variable as dictionary items

        >>> import json
        >>> import raw.data_input as data_input
        >>> p = data_input.parser()
        >>> class seq():
        ...     def __str__(self):
        ...         return self.name
        >>> data1 = seq()
        >>> data1.name = "data1"
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQTWO']),
        ...                   ('acc2',['SEQONE'])]
        >>> p.parse(data1)
        >>> s = EPPI_dbopen('tmp.prj', flag='n')
        >>> s.set_parser(p)
        >>> print json.dumps(obj=s, indent=4) # doctest: +NORMALIZE_WHITESPACE
        {
            "files": [],
            "p_proteins": {
                "acc1": 1,
                "acc2": 1
            },
            "p_sources": [
                "data1"
            ],
            "p_spectral_count": false,
            "p_peptides": {
                "acc1": {
                    "SEQTWO": 1
                },
                "acc2": {
                    "SEQONE": 1
                }
            }
        }

        :param p: a parser
        :type p: raw.data_input.parser
        :raises TypeError: if p is not a raw.data_input.parser
        """
        # this means that I kill the duck typing now... think about
        if not isinstance(p, data_input.parser):
            raise TypeError, "accepting only a parser"
        result = p.__dict__
        for k, v in result.iteritems():
            self.__setitem__('p_{0}'.format(k), v)

    def get_parser(self):
        """
        To obtain a stored parser

        >>> import json
        >>> import raw.data_input as data_input
        >>> p = data_input.parser()
        >>> class seq():
        ...     def __str__(self):
        ...         return self.name
        >>> data1 = seq()
        >>> data1.name = "data1"
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQTWO']),
        ...                   ('acc2',['SEQONE'])]
        >>> p.parse(data1)
        >>> s = EPPI_dbopen('tmp.prj', flag='n')
        >>> s.set_parser(p)
        >>> print s.get_parser() # doctest: +NORMALIZE_WHITESPACE
        Spectral_count: False
        accession   freq_prot       sequence        freq_pept
        acc1        1       SEQTWO  1
        acc2        1       SEQONE  1
        <BLANKLINE>

        :return: a parser
        :rtype: raw.data_input.parser
        """
        p = data_input.parser()
        p.proteins = self.__getitem__("p_proteins")
        p.peptides = self.__getitem__("p_peptides")
        p.spectral_count = self.__getitem__("p_spectral_count")
        p.sources = self.__getitem__("p_sources")
        return p

    def set_selected(self, s):
        """
        set parser variable as dictionary items

        >>> import json
        >>> import raw.data_input as data_input
        >>> p = data_input.parser()
        >>> class seq():
        ...     def __str__(self):
        ...         return self.name
        >>> data1 = seq()
        >>> data1.name = "data1"
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
        ...                   ('acc2',['SEQONE', 'SEQTWO',])]
        >>> p.parse(data1)
        >>> data2 = seq()
        >>> data2.name = "data2"
        >>> data2.proteins = ['acc1','acc3']
        >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
        ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
        >>> p.parse(data2)
        >>> p_2 = data_input.selected(p, peptThr=1., protThr=1.)
        >>> s = EPPI_dbopen('tmp.prj', flag='n')
        >>> s.set_selected(p_2)
        >>> print json.dumps(obj=s, indent=4) # doctest: +NORMALIZE_WHITESPACE
        {
            "files": [],
            "s_peptThr": 1.0,
            "s_protThr": 1.0,
            "s_proteins": {
                "acc1": 2
            },
            "s_sources": [
                "data1",
                "data2"
            ],
            "s_spectral_count": false,
            "s_peptides": {
                "acc1": {
                    "SEQONE": 2,
                    "SEQTWO": 2
                }
            }
        }

        :param s: a selected parser
        :type s: raw.data_input.selected
        :raises TypeError: if s is not a raw.data_input.selected
        """
        # this means that I kill the duck typing now... think about
        if not isinstance(s, data_input.selected):
            raise TypeError, "accepting only a selected parser"
        result = s.__dict__
        for k, v in result.iteritems():
            self.__setitem__('s_{0}'.format(k), v)

    def get_selected(self):
        """
        To obtain a stored parser

        >>> import json
        >>> import raw.data_input as data_input
        >>> p = data_input.parser()
        >>> class seq():
        ...     pass
        >>> data1 = seq()
        >>> data1.proteins = ['acc1','acc2']
        >>> data1.peptides = [('acc1',['SEQONE', 'SEQTWO','SEQTHREE']),
        ...                   ('acc2',['SEQONE', 'SEQTWO',])]
        >>> p.parse(data1)
        >>> data2 = seq()
        >>> data2.proteins = ['acc1','acc3']
        >>> data2.peptides = [('acc1',['SEQONE', 'SEQTWO']),
        ...                   ('acc3',['SEQFIVE', 'SEQSIX'])]
        >>> p.parse(data2)
        >>> p_2 = data_input.selected(p, peptThr=1., protThr=1.)
        >>> s = EPPI_dbopen('tmp.prj', flag='n')
        >>> s.set_parser(p)
        >>> s.set_selected(p_2)
        >>> p_3 = s.get_selected()
        >>> print p_3 # doctest: +NORMALIZE_WHITESPACE
        Spectral_count: False
        accession   freq_prot       sequence        freq_pept
        acc1        2       SEQONE  2
        acc1        2       SEQTWO  2
        <BLANKLINE>

        :return: a parser
        :rtype: raw.data_input.parser
        """
        p = self.get_parser()
        s = data_input.selected(p)
        s.proteins = self.__getitem__("s_proteins")
        s.peptides = self.__getitem__("s_peptides")
        s.spectral_count = self.__getitem__("s_spectral_count")
        s.sources = self.__getitem__("s_sources")
        s.peptThr = self.__getitem__("s_peptThr")
        s.protThr = self.__getitem__("s_protThr")
        return s

def EPPI_dbopen(filename, flag=None, mode=None):
    """
    >>> s = EPPI_dbopen('tmp.prj', flag='n')
    >>> print s
    {'files': []}
    >>> s.close()
    >>> print os.listdir('tmp')
    ['tmp.prj']
    >>> import io
    >>> f = io.open('tmp/tmp.prj', 'rb')
    >>> print (f.read())
    {
        "files":[]
    }
    >>> f.close()
    """
    return EPPI_DictDB(filename, flag, mode)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

