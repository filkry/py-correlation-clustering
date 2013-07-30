import networkx as nx
import random


class solver:
    def __init__(self, G, delta = 1.0/44):
        """
        Args:
            delta: "cleanness" parameter. Defaults to the assumed value of 1/44
                   given in the paper
        """

        self.__G__ = G
        self.__reset_caches__()
        self.__clusters__ = None
        self.__delta__ = delta

    def __reset_caches__():
        self.__G_nodes__ = set(G.nodes())
        self.__N_plus_cache__ = dict()

    def __remove_cluster__(C):
        self.__G__.remove_nodes_from(C)
        self.__reset_caches__()

    def positive_neighbours(self, u):
        """
        Returns N+(u), or {u} U {v : e(u, v) = +}

        Args:
            G: a networkx graph where presence of edges indicates a + edge
            u: a node in G
        """

        if u in self.__N_plus_cache__:
            return self.__N_plus_cache__[u]

        res = set(G.neighbours(u)).add(u)
        self.__N_plus_cache__[u] = res
        return res

    def delta_good(v, C, delta):
        """
        Returns true if v is delta-good with respect to C, where C is a cluster in
        G

        Args:
            G: a networkx graph
            v: a vertex v in G
            C: a set of vertices in G
            delta: "cleanness" parameter
        """

        Nv = positive_neighbours(v)

        return len(Nv & C) >= (1.0 - delta) * len(C) and
               len(Nv & (self.__G_nodes__ - C)) <= delta * len(C)

    def run():
        """
        Runs the "cautious algorithm" from the paper.

        """

        if self.__clusters__ is None:
            self.__clusters__ = []
            
            while not (len(self.__G_nodes__) > 0):
                # Make sure we try all the vertices until we run out
                vs = random.sample(self.__G_nodes__, len(self.__G_nodes__))

                Av = None

                for v in vs:
                    Av = positive_neighbours(v)

                    # Vertex removal step
                    for x in positive_neighbours(v):
                        if not delta_good(x, Av, 3 * self.__delta__):
                            Av.remove(x)

                    # Vertex addition step
                    Y = [y for y in self.__G_nodes__
                           if delta_good(y, Av, 7 * self.__delta__)]
                    Av = Av | Y

                    if len(Av) > 0:
                        break

                # Second quit condition: all sets Av are empty
                if len(Av) == 0:
                    break

                self.__clusters__.append(Av)
                self.__remove_cluster__(Av)

            # add all remaining vertices as singleton clusters
            for v in self.__G_nodes__:
                self.__clusters__.append(set(v))

        return self.__clusters__
