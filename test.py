import random
from quadtree import Quadtree


def rand_qt():
    '''
    Constructs a random quadtree.
    '''
    N = random.randint(1, 1000)
    nodes = set((random.randint(-N, N), random.randint(-N, N))
                for _ in range(N))
    qt = Quadtree()
    for node in nodes:
        qt.add(node[0], node[1])
    return qt


def qt_test(qt):
    '''
    Check that the quadtree has 
    the defining property.  
    '''
    if not hasattr(qt, 'root'):
        return

    def test(root):

        if hasattr(root, 'NE'):
            child = getattr(root, 'NE')
            assert (root.x <= child.x and
                    root.y < child.y)
            test(child)

        if hasattr(root, 'NW'):
            child = getattr(root, 'NW')
            assert (root.x > child.x and
                    root.y <= child.y)
            test(child)

        if hasattr(root, 'SW'):
            child = getattr(root, 'SW')
            assert (root.x >= child.x and
                    root.y > child.y)
            test(child)

        if hasattr(root, 'SE'):
            child = getattr(root, 'SE')
            assert (root.x < child.x and
                    root.y >= child.y)
            test(child)

    test(qt.root)


# Test that the constructed trees have the
# requireed property.
for _ in range(100):
    qt = rand_qt()
    qt_test(qt)


# Testing the return value of ``search``.
for _ in range(1000):

    N = random.randint(1, 1000)
    nodes = set((random.randint(-N, N), random.randint(-N, N))
                for _ in range(N))
    qt = Quadtree()
    for node in nodes:
        qt.add(node[0], node[1])
    for node in nodes:
        assert qt.search(node[0], node[1])

    for _ in range(100):
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        assert ((x, y) in nodes) == qt.search(x, y)


# Test ``quary_range``.

def set_query(s, min_x, max_x,
              min_y, max_y):
    res = []
    for x, y in s:
        if (min_x <= x <= max_x and
                min_y <= y <= max_y):
            res.append((x, y))
    return res


# Test ``quary_range``.

for _ in range(1000):

    N = random.randint(1, 1000)
    nodes = set((random.randint(-N, N), random.randint(-N, N))
                for _ in range(N))

    qt = Quadtree()
    for node in nodes:
        qt.add(node[0], node[1])

    min_x = random.randint(-N, N)
    max_x = random.randint(min_x, N+1)
    min_y = random.randint(-N, N)
    max_y = random.randint(min_y, N+1)

    intersection = set_query(nodes, min_x, max_x,
                             min_y, max_y)

    assert sorted(intersection) == sorted(qt.query_range(min_x, max_x,
                                                         min_y, max_y))
