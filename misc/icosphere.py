"""Create an icosphere from convex regular polyhedron.

Adapted from:

https://gist.github.com/AbhilashReddyM/aed58c60438bf4c313831718013ce48f

Thank you Abhilash Reddy (abhilashreddy.com)!

Original authorship:

Author: William G.K. Martin
(wgm2111@cu where cu=columbia.edu) (github.com/wgm2111)
copyright (c) 2010
liscence: BSD style

Modified by Abhilash Reddy (abhilashreddy.com):

* made to work with Python 3+
* made to work with recent versions of matplotlib

"""

from matplotlib import tri
import numpy


class Polyhedron(object):
    """Contain information about a polyhedron."""

    def __init__(self):
        """Define a normalized convex regular polyhedron."""
        self.triangle_centers = self._get_triangle_centers()
        self.edges = self._get_edges()
        self.edge_centers = self._get_edge_centers()

    def __repr__(self):
        """Return a representation of the object."""
        return (f'Polyhedron(faces={len(self.triangles)}, '
                f'vertices={len(self.vertices)})')

    def _get_vertices(self):
        raise NotImplementedError()

    def _get_triangles(self):
        raise NotImplementedError()

    def _get_triangle_centers(self):
        centers = numpy.empty_like(self.triangles, dtype=float)
        for i, triangle in enumerate(self.triangles):
            points = [self.vertices[idx] for idx in triangle]
            centers[i] = numpy.mean(points)
        return centers

    def _get_edges(self):
        edges = []
        for triangle in self.triangles:
            i1, i2, i3 = triangle
            edges.append([[i1, i2], [i1, i3], [i2, i3]])
        return numpy.array(edges)

    def _get_edge_centers(self):
        centers = numpy.empty_like(self.edges, dtype=float)
        for i, edge in enumerate(self.edges):
            points = [self.vertices[idx] for idx in edge]
            centers[i] = numpy.mean(points)
        return centers


class Icosahedron(Polyhedron):
    """Contain information about an icosahedron (polyhedron with 20 faces)."""

    def __init__(self):
        """Define a normalized convex regular icosahedron."""
        self.vertices = self._get_vertices()
        self.triangles = self._get_triangles()
        super().__init__()

    def _get_vertices(self):
        # Define vertices based on the golden ratio.
        a = 0.5 * (1 + numpy.sqrt(5))  # golden ratio
        vertices = numpy.array([[a, 0, 1],
                                [-a, 0, 1],
                                [-a, 0, -1],
                                [a, 0, -1],
                                [1, a, 0],
                                [1, -a, 0],
                                [-1, -a, 0],
                                [-1, a, 0],
                                [0, 1, a],
                                [0, 1, -a],
                                [0, -1, -a],
                                [0, -1, a]])
        # Normalize vertices
        # (note that all vertices are equidistant from origin).
        vertices /= numpy.linalg.norm(vertices[0])
        # Rotate vertices so that top point is located on z-axis.
        alpha = numpy.arctan2(vertices[0, 0], vertices[0, 2])
        ca, sa = numpy.cos(alpha), numpy.sin(alpha)
        R = numpy.array([[ca, 0, -sa],
                         [0, 1, 0],
                         [sa, 0, ca]])
        vertices = numpy.inner(R, vertices).transpose()
        # Reorder vertices in a downward-spiral fashion.
        new_order = [0, 3, 4, 8, 11, 5, 10, 9, 7, 1, 6, 2]
        return vertices[new_order]

    def _get_triangles(self):
        indices = numpy.array([[1, 0, 2],
                               [2, 0, 3],
                               [3, 0, 4],
                               [4, 0, 5],
                               [5, 0, 1],
                               [6, 1, 7],
                               [2, 7, 1],
                               [7, 2, 8],
                               [2, 3, 8],
                               [8, 3, 9],
                               [3, 4, 9],
                               [9, 4, 10],
                               [10, 4, 5],
                               [10, 5, 6],
                               [6, 5, 1],
                               [6, 7, 11],
                               [7, 8, 11],
                               [8, 9, 11],
                               [9, 10, 11],
                               [10, 6, 11]])
        return indices


polyhedrons = {'icosahedron': Icosahedron}


class Icosphere(object):
    """Contain information about an icosphere."""

    def __init__(self, n, polyhedron):
        """Create an icosphere."""
        self.n = n
        self.base = polyhedron
        self.vertices, self.triangles, self.edges = self._triangulate()

    def __repr__(self):
        """Return a representation of the object."""
        return (f'Icosphere(faces={len(self.triangles)}, '
                f'vertices={len(self.vertices)})')

    def print_info(self):
        """Print information about the icosphere."""
        print(self)
        min_lengths = numpy.empty(len(self.triangles))
        max_lengths = numpy.empty(len(self.triangles))
        mean_lengths = numpy.empty(len(self.triangles))
        for i, triangle in enumerate(self.triangles):
            a, b, c = [self.vertices[idx] for idx in triangle]
            lengths = [numpy.linalg.norm(a - b),
                       numpy.linalg.norm(a - c),
                       numpy.linalg.norm(b - c)]
            min_lengths[i] = numpy.min(lengths)
            max_lengths[i] = numpy.max(lengths)
            mean_lengths[i] = numpy.mean(lengths)
        print('Min edge length:', numpy.min(min_lengths))
        print('Max edge length:', numpy.max(max_lengths))
        print('Mean edge length:', numpy.mean(mean_lengths))

    def _triangulate(self):
        """Compute the triangulation of a unit sphere.

        The function refines each face of an icosahedron to a n-th order
        barycentric triangle.
        This function addresses two key issues:

        1. calculate the triangles (unique by construction)
        2. remove non-unique nodes and edges

        """
        vertices = numpy.array([self.base.vertices[self.base.triangles[:, 0]],
                                self.base.vertices[self.base.triangles[:, 1]],
                                self.base.vertices[self.base.triangles[:, 2]]])
        M = self._get_barycenter_matrix(self.n + 1)
        vertices = numpy.tensordot(vertices, M,
                                   axes=([0, ], [-1, ])).transpose(0, 2, 1)
        num_vertices = vertices.shape[1]
        assert vertices.size / 3 < 1e6, 'Number of vertices too high!'
        num = 20
        flat_coords = numpy.arange(vertices.size / 3).reshape(num,
                                                              num_vertices)

        edges_, triangles_ = self._triangulate_barycentric(M)

        triangles = numpy.zeros((num, triangles_.shape[0], 3), dtype=int)
        edges = numpy.zeros((num, edges_.shape[0], 2), dtype=int)

        for i in range(num):
            for j in range(3):
                triangles[i, :, j] = flat_coords[i, triangles_[:, j]]
                if j < 2:
                    edges[i, :, j] = flat_coords[i, edges_[:, j]]

        vertices = vertices.reshape(vertices.size // 3, 3)
        triangles = triangles.reshape(triangles.size // 3, 3)
        edges = edges.reshape(edges.size // 2, 2)
        # Normalize vertices.
        scalars = numpy.linalg.norm(vertices, axis=-1)
        vertices = (vertices.T / scalars).T
        # Remove repeated vertices.
        _, iu, irep = numpy.unique(numpy.dot(vertices // 1e-8,
                                             100 * numpy.arange(1, 4, 1)),
                                   return_index=True, return_inverse=True)

        vertices = vertices[iu]
        triangles = irep[triangles]
        edges = irep[edges]
        mid = (vertices[edges[:, 0]] + vertices[edges[:, 1]]) / 2
        _, iu = numpy.unique(numpy.dot(mid // 1e-8,
                                       100 * numpy.arange(1, 4, 1)),
                             return_index=True)
        edges = edges[iu, :]
        return vertices, triangles, edges

    def _get_barycenter_matrix(self, n):
        """Create the matrix that will refine points on a triangle."""
        nrows = n * (n + 1) // 2
        M = numpy.zeros((nrows, 3))
        vals = numpy.arange(n) / (n - 1)
        start = 0
        for i, offset in enumerate(range(n, 0, -1)):
            stop = start + offset
            M[start:stop, 0] = vals[offset - 1::-1]
            M[start:stop, 1] = vals[:offset]
            M[start:stop, 2] = vals[i]
            start = stop
        return M

    def _triangulate_barycentric(self, points):
        """Triangulate a barycentric triangle using Matplotlib tri module."""
        x = (numpy.cos(-numpy.pi / 4) * points[:, 0] +
             numpy.sin(-numpy.pi / 4) * points[:, 1])
        y = points[:, 2]
        triangulation = tri.Triangulation(x, y)
        return triangulation.edges, triangulation.triangles


def create_polyhedron(ptype):
    """Create a polyhedron."""
    ptype = ptype.lower()
    if ptype not in polyhedrons.keys():
        raise ValueError(f'ptype should be one of {list(polyhedrons.keys())}')
    return polyhedrons[ptype]()


def create_icosphere(n, polyhedron='icosahedron'):
    """Create an icosphere by recursively refining faces."""
    polyhedron = create_polyhedron(polyhedron)
    return Icosphere(n, polyhedron)
