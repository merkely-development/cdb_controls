from os import mkdir, path
from distutils.dir_util import copy_tree, remove_tree


class AutoDirCopier(object):
    def __init__(self, source_dir, target_dir):
        if not path.isdir(source_dir):
            raise ValueError("source dir '{} does not exist".format(source_dir))
        if path.exists(target_dir):
            raise ValueError("target dir '{}' already exists".format(target_dir))
        self._source_dir = source_dir
        self._target_dir = target_dir

    def __enter__(self):
        mkdir(self._target_dir)
        copy_tree(self._source_dir, self._target_dir)

    def __exit__(self, _type, _value, _traceback):
        remove_tree(self._target_dir)
