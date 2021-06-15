from anytree import Node as AnytreeNode
from anytree import PreOrderIter

from h5py import Group
from h5py import Dataset

from pyutils.viz_tree import get_tree

MAP_TYPE_STR = {Group: 'group',
                Dataset: 'dataset'}


class HdfNode(AnytreeNode):

    def __init__(self, name, parent=None, children=None):
        super().__init__(name, parent, children)
        self.full_name = name

    def _get_hdf_obj(self, file):
        return file[self.full_name]

    def get_hdf_type(self, file):
        return MAP_TYPE_STR.get(type(self._get_hdf_obj(file)), None)

    def get_dtype(self, file):
        obj = self._get_hdf_obj(file)
        if hasattr(obj, 'dtype'):
            return obj.dtype


def get_hdf_tree(file, root_name='.', simplify_names=True):

    # get items
    items_ls = []
    file.visit(items_ls.append)

    # create items dict
    items = [{'id': id_, 'name': name, 'parent_id': ''}
             for id_, name in enumerate(items_ls)]
    _assign_parent(items[1:], 0, items[0], level=0, level_last={0: ''})

    root = get_tree(items, Node=HdfNode)

    if simplify_names:
        _simplify_names(root)

    return root


def _assign_parent(items, i, parent, level, level_last):
    item = items[i]
    child_level = len(item['name'].split('/')) - 1

    if child_level > level:  # break cause
        parent_id = parent['id']
    elif child_level == level:
        parent_id = parent['parent_id']
    else:
        parent_id = level_last[child_level]

    item['parent_id'] = parent_id
    level_last[child_level] = parent_id

    try:
        _assign_parent(items, i + 1, item, child_level, level_last)
    except IndexError:  # end clause
        return


def _simplify_names(root):
    for node in PreOrderIter(root):
        node.name = node.name.split('/')[-1]
