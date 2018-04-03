import networkx as nx
import handlers.DatabaseHandler as db
import random


try:
    import pygraphviz
    from networkx.drawing.nx_agraph import graphviz_layout
except ImportError:
    try:
        import pydot
        from networkx.drawing.nx_pydot import graphviz_layout
    except ImportError:
        raise ImportError("This example needs Graphviz and either "
                          "PyGraphviz or pydot.")

import matplotlib.pyplot as plt


def basic_properties(graph):

    pathlengths = []

    print("source vertex {target:length, }")
    for v in graph.nodes():
        print(v)
        spl = nx.single_source_shortest_path_length(graph, v)
        #print('%s %s' % (v, spl))
        for p in spl.values():
            pathlengths.append(p)

    print('')
    print("average shortest path length %s" % (sum(pathlengths) / len(pathlengths)))

    # histogram of path lengths
    dist = {}
    for p in pathlengths:
        if p in dist:
            dist[p] += 1
        else:
            dist[p] = 1

    print('')
    print("length #paths")
    verts = dist.keys()
    for d in sorted(verts):
        print('%s %d' % (d, dist[d]))

    print("radius: %d" % nx.radius(graph))
    print("diameter: %d" % nx.diameter(graph))
    print("eccentricity: %s" % nx.eccentricity(graph))
    print("center: %s" % nx.center(graph))
    print("periphery: %s" % nx.periphery(graph))
    print("density: %s" % nx.density(graph))


def draw_graph(graph):
    G = graph
    nx.draw(G)
    plt.show()

def generate_graph():
    cnt = 0
    graph = nx.Graph()
    users_iter = db.get_inline_iterator()
    file = open('test.sif', 'w')

    for user in users_iter:
        # print(user)
        print(cnt)
        cnt = cnt + 1
        user_steam_id = user['steam_id']
        friends = user['friends']
        print(user_steam_id)
        for friend in friends:
            file.write(user_steam_id + ' pp ' + friend['steamid'] + '\n')
            graph.add_edge(user_steam_id, friend['steamid'],
                           relationship=friend['relationship'],
                           friend_since=friend['friend_since'])
    return graph

if __name__ == '__main__':
    graph = generate_graph()
    draw_graph(graph)
    basic_properties(graph)






























