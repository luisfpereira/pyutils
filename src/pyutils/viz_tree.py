from anytree import Node as AnytreeNode
from anytree import RenderTree
from anytree.exporter import DotExporter


def get_tree(items, root_name='.', name_key='name', id_key='id',
             parent_id_key='parent_id', Node=AnytreeNode):
    '''
    Args:
        items (list of dict)
    '''

    # create nodes
    nodes = {root_name: Node(root_name)}
    for item in items:
        nodes[item[id_key]] = Node(item[name_key])

    # assign relationships
    for item in items:
        parent_id = item[parent_id_key]
        parent_node = nodes[parent_id] if parent_id not in ['', None] else nodes[root_name]
        nodes[item[id_key]].parent = parent_node

    return nodes[root_name]


def print_tree(root):
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))


def export_graph(root, filename, **kwargs):
    # TODO: bad representation if nodes share name (even if different)
    exporter = DotExporter(root, **kwargs)
    exporter.to_picture(filename)
