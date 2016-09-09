import graphviz as gv
import functools


graph = functools.partial(gv.Graph)
digraph = functools.partial(gv.Digraph)


def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph


def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph


def visualize(graph, pr, name=''):
    n_nodes = len(pr)
    node_nums = dict(zip(pr.keys(), map(str, range(n_nodes))))
    list_nodes = [(node_nums[x],
                  {'label': 'PR: %.2f%%' % (100 * y)}) for x, y in pr.items()]
    visual_graph = add_nodes(digraph(), list_nodes)
    for url in pr:
        edges = [(node_nums[url], node_nums[ref]) for ref in graph[url]]
        visual_graph = add_edges(visual_graph, edges)
    visual_graph.render('gv-' + name, view=True)
