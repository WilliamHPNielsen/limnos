from limnos.types import Trails, Walls, Route, Wall, subtract_points, add_points


def wall_intersects_route(route: Route, wall: Wall) -> bool:
    """
    Check whether a wall intersects a route. If it does intersect, return
    True.
    """
    wall_delta_coords = subtract_points(*wall)
    route_delta_coords = {(-2, 0): ((1, 1), (1, -1)),
                          (0, -2): ((1, 1), (-1, 1)),
                          (2, 0): ((-1, 1), (-1, -1)),
                          (0, 2): ((1, -1), (-1, -1))}[wall_delta_coords]

    route_p0 = add_points(wall[0], route_delta_coords[0])
    route_p1 = add_points(wall[0], route_delta_coords[1])

    points_in_route = (route_p0 in route) and (route_p1 in route)
    if points_in_route:
        p0_ind = route.index(route_p0)

        # special case: the end of the route
        if p0_ind == len(route) - 1:
            points_neighbours = route[p0_ind - 1] == route_p1
        else:
            points_neighbours = (route[p0_ind + 1] == route_p1 or
                                 route[p0_ind - 1] == route_p1)
    else:
        points_neighbours = False

    return points_in_route and points_neighbours


def _all_potential_walls(trails: Trails) -> Walls:
    """
    Helper function to generate all possible walls in the rectangle
    defined by the extremal points of the highest route in the trails
    """
    x0 = trails.main[0][0] - 1
    x1 = trails.main[-1][0] + 1
    y0 = trails.main[0][1] - 1
    y1 = trails.main[-1][1] + 1

    horiz_walls: Walls = [((x, y), (x + 2, y))
                          for x in range(x0, x1, 2)
                          for y in range(y0, y1 + 2, 2)]
    vert_walls: Walls = [((x, y), (x, y + 2))
                         for x in range(x0, x1 + 2, 2)
                         for y in range(y0, y1, 2)]

    return horiz_walls + vert_walls


def walls_from_trails(trails: Trails) -> Walls:
    """
    Generate the walls that complement all the routes in a Trails collection.
    All possible allowed walls are generated.
    """

    walls = _all_potential_walls(trails)
    forbidden_walls = []

    routes = trails.all_routes()

    for wall in walls:
        w1 = wall
        w2 = (wall[1], wall[0])
        for route in routes:
            intersect1 = wall_intersects_route(route, w1)
            intersect2 = wall_intersects_route(route, w2)
            if intersect1 or intersect2:
                forbidden_walls.append(wall)

    legal_walls = [wall for wall in walls if wall not in forbidden_walls]

    return legal_walls
