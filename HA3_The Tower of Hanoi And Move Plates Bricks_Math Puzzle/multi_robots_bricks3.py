from z3 import *


def moving_bricks_with_solver(num_bricks, num_pos, classes, num_robots, max_steps):
    # Create Z3 solver
    s = Solver()

    # Create mapping of bricks to their classes
    brick_class = classes
    num_classes = len(set(classes))

    # Decision variables
    robot_on = [[[Bool(f"robot_on_{r}_{p}_{t}") for t in range(max_steps)] for p in range(num_pos)] for r in
                range(num_robots)]
    obj_robot = [[[Bool(f"obj_robot_{r}_{b}_{t}") for t in range(max_steps)] for b in range(num_bricks)] for r in
                 range(num_robots)]

    on = [[[Bool(f"on_{b}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_pos)] for b in range(num_bricks)]
    from_pos = [[Bool(f"from_{p}_{t}") for t in range(max_steps)] for p in range(num_pos)]
    to_pos = [[Bool(f"to_{p}_{t}") for t in range(max_steps)] for p in range(num_pos)]

    # Initial conditions: all bricks start on their initial positions
    for b in range(num_bricks):
        s.add(on[b][0][0])  # Brick b is at the first position at time 0
        for p in range(1, num_pos):
            s.add(Not(on[b][p][0]))  # Not in any other position

    # Final conditions: all bricks must be at the final position by `max_steps`
    for b in range(num_bricks):
        s.add(on[b][num_pos - 1][max_steps])
        for p in range(num_pos - 1):
            s.add(Not(on[b][p][max_steps]))  # Not in any other position at final step

    # Ensure that each robot can only move one brick at a time and no more than one robot is on the same platform at the same time
    for t in range(max_steps):
        for r in range(num_robots):
            s.add(Or([obj_robot[r][b][t] for b in range(num_bricks)]))  # At least one robot is moving a brick
            for b in range(num_bricks):
                s.add(Implies(obj_robot[r][b][t], And([Not(obj_robot[r][b2][t]) for b2 in range(num_bricks) if
                                                       b2 != b])))  # Only one brick moved by one robot
        for p in range(num_pos):
            s.add(Or([robot_on[r][p][t] for r in range(num_robots)]))  # At least one robot is on each platform

    # Ensure that no two bricks from the same category are on the same platform
    for c in range(num_classes):
        for t in range(max_steps):
            for p in range(num_pos):
                s.add(Or([Not(on[b][p][t]) for b in range(num_bricks) if
                          brick_class[b] == c]))  # No two bricks of the same class on the same platform

    # Ensure from and to positions are distinct for each move
    for t in range(max_steps):
        for p in range(num_pos):
            s.add(Not(And(from_pos[p][t], to_pos[p][t])))  # From and to positions cannot be the same

    # Ensure valid movements between start and end positions
    for b in range(num_bricks):
        for p in range(num_pos):
            for t in range(max_steps):
                for p2 in range(num_pos):
                    if p != p2:
                        s.add(Implies(And(from_pos[p][t], to_pos[p2][t]),
                                      And(on[b][p2][t + 1], Not(on[b][p][t + 1]))))  # Move to new position

    # Non-moving bricks remain on the same position
    for b in range(num_bricks):
        for p in range(num_pos):
            for t in range(max_steps - 1):
                s.add(Implies(Not(Or([from_pos[p][t] for p in range(num_pos)])),
                              on[b][p][t + 1]))  # Stay at the same place if not moving

    # Check the solution
    if s.check() == sat:
        model = s.model()
        print("Solution found")
        # Extract solution from model
        for t in range(max_steps + 1):
            for b in range(num_bricks):
                for p in range(num_pos):
                    if model.eval(on[b][p][t]):
                        print(f"At time {t}, brick {b} is at position {p}")
    else:
        print("No solution found")


# Example usage:
num_bricks = 5
num_pos = 3
num_robots = 2
classes = [0, 0, 1, 1, 2]
max_steps = 10

moving_bricks_with_solver(num_bricks, num_pos, classes, num_robots, max_steps)
