from collections import namedtuple


class Node:
    pass
# Attributes used:
# x, y, NE, NW, SW, SE.
# Directions point to other nodes.


class Quadtree:
    '''
    Quadtree for efficient querying of 2-dimensional points.

    Methods:
    add(x,y)
    search(x,y)
    query_range(min_x,max_x,
                min_y,max_y)

    Example usage:
    >>> qt = Quadtree()
    >>> qt.add(1,2)
    True
    >>> qt.add(3,4)
    True
    >>> qt.add(1,2)
    False
    >>> qt.search(1,2)
    True
    >>> qt.search(1,0)
    False
    >> qt.query_range(-10,10,-10,10)
    [(1,2), (3,4)]
    '''

    # Convention for dealing with ties.
    # (-1, 0) means that the new point has smaller
    # x-coordinate than the parent (the -1) and
    # equal y-coordiante to the parent.
    _comparison_directions = {(1, 1):   'NE', (1, -1): 'SE',
                              (1, 0):   'SE', (-1, 1): 'NW',
                              (-1, -1): 'SW', (-1, 0): 'NW',
                              (0, 1):   'NE', (0, -1): 'SW',
                              (0, 0):   'EQ'}

    def _get_direction(parent_x, parent_y,
                       new_x, new_y):
        '''
        Compares (parent_x,parent_y) with
        (new_x,new_y) and returns the relationship.  
        '''
        x_coor = 0
        if parent_x < new_x:
            x_coor += 1
        elif parent_x > new_x:
            x_coor -= 1

        y_coor = 0
        if parent_y < new_y:
            y_coor += 1
        elif parent_y > new_y:
            y_coor -= 1

        return Quadtree._comparison_directions[(x_coor, y_coor)]

    def add(self, x, y):
        '''
        Return if the point was added to the tree.  
        'False' if (x,y) was already in the tree.  
        '''
        # Initialize if not initialized.
        if not hasattr(self, 'root'):
            root = Node()
            root.x, root.y = x, y
            self.root = root
            return True

        # Search for the final node.
        root = self.root
        while True:
            direction = Quadtree._get_direction(root.x, root.y,
                                                x, y)
            if direction == 'EQ':
                return False
            if hasattr(root, direction):
                root = getattr(root, direction)
            else:
                break

        # Update last node, create new leaf.
        leaf = Node()
        leaf.x, leaf.y = x, y
        setattr(root, direction, leaf)
        return True

    def search(self, x, y):
        '''
        Returns 'True' if (x,y) is in the tree.
        Otherwise, returns 'False'.  
        '''
        if not hasattr(self, 'root'):
            return False

        root = self.root
        while True:
            direction = Quadtree._get_direction(root.x, root.y,
                                                x, y)
            if direction == 'EQ':
                return True
            if hasattr(root, direction):
                root = getattr(root, direction)
            else:
                return False

    def _interval_comp(x, lb, ub):
        '''
        Returns:
            x < lb        ---> -1
            lb <= x <= ub ----> 0
            ub < x        ----> 1
        '''
        if x < lb:
            return -1
        if x <= ub:
            return 0
        return 1

    # Directions that must be tested if the
    # comparison of the root to the bounds is the
    # given value.
    _interval_comp_directions = {(0, 0): ['NE', 'NW', 'SW', 'SE'],
                                 (1, 1): ['SW'],
                                 (-1, 1): ['SE'],
                                 (-1, -1): ['NE'],
                                 (1, -1): ['NW'],
                                 (0, 1): ['SW', 'SE'],
                                 (0, -1): ['NE', 'NW'],
                                 (-1, 0): ['NE', 'SE'],
                                 (1, 0): ['NW', 'SW']}

    def query_range(self, min_x, max_x,
                    min_y, max_y):
        '''
        Returns a list of all of the points (x,y)
        in the tree with min_x <= x <= max_x and 
        min_y <= y <= max_y.

        Points are returned as tuples.  
        '''

        if min_x > max_x or min_y > max_y:
            raise Exception("Invalid input.")

        if not hasattr(self, 'root'):
            return []

        res = []

        def traverse(root):
            x_comp = Quadtree._interval_comp(root.x, min_x, max_x)
            y_comp = Quadtree._interval_comp(root.y, min_y, max_y)
            comp = (x_comp, y_comp)

            if comp == (0, 0):
                res.append((root.x, root.y))

            for d in Quadtree._interval_comp_directions[comp]:
                if hasattr(root, d):
                    traverse(getattr(root, d))

        root = self.root
        traverse(root)
        return res
