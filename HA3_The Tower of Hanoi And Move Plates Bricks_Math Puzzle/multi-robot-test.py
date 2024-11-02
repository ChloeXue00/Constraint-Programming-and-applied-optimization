from jinja2.optimizer import Optimizer
from z3 import *
def multi_robot_moving_bricks(num_bricks, num_platforms, num_robots, categories, max_steps, init_positions,
                              final_positions):
    # Variables:
    # - robot_on[r][p][t]: whether robot r is on platform p at time step t
    # - brick_on[b][p][t]: whether brick b is on platform p at time step t
    # - robot_move[r][b][t]: whether robot r is moving brick b at time step t
    # - from_pos[p][t], to_pos[p][t]: platform position variables (from and to positions)
    s = Solver()
    opt=Optimize()
    # Initialize decision variables
    robot_on = [[[Bool(f"robot_on_{r}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_platforms)] for r in
                range(num_robots)]
    brick_on = [[[Bool(f"brick_on_{b}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_platforms)] for b in
                range(num_bricks)]
    robot_move = [[[Bool(f"robot_move_{r}_{b}_{t}") for t in range(max_steps)] for b in range(num_bricks)] for r in
                  range(num_robots)]

    from_pos = [[Bool(f"from_{p}_{t}") for t in range(max_steps)] for p in range(num_platforms)]
    to_pos = [[Bool(f"to_{p}_{t}") for t in range(max_steps)] for p in range(num_platforms)]

    # Initial conditions: all bricks start on their initial positions
    # Initial conditions: all bricks start on their initial positions
    for b in range(num_bricks):
        initial_platform = init_positions[b]  # Ensure valid platform index
        if initial_platform < num_platforms:
            opt.add(brick_on[b][initial_platform][0])  # Initial position at t=0
            for p in range(num_platforms):
                if p != initial_platform:
                    opt.add(Not(brick_on[b][p][0]))  # Ensure not on other platforms
        else:
            raise IndexError(f"Initial position for brick {b} is out of range for the available platforms.")

    # Final conditions: all bricks must be at the final position by `max_steps`
    for b in range(num_bricks):
        opt.add(brick_on[b][final_positions[b]][max_steps])
        for p in range(num_platforms):
            if p != final_positions[b]:
                opt.add(Not(brick_on[b][p][max_steps]))

    # Ensure that each robot can only move one brick at a time and no more than one robot is on the same platform at the same time
    for t in range(max_steps):
        for r in range(num_robots):
            opt.add(Or([robot_move[r][b][t] for b in range(num_bricks)]))
            for b in range(num_bricks):
                opt.add(Implies(robot_move[r][b][t],
                            And([Not(robot_move[r][b2][t]) for b2 in range(num_bricks) if b2 != b])))

    # Ensure no two robots are on the same platform
    for p in range(num_platforms):
        opt.add(AtMost(*[robot_on[r][p][t] for r in range(num_robots)], 1))

    # Ensure that no two bricks from the same category are on the same platform at any given time
    for t in range(max_steps):
        for c in range(len(categories)):
            for p in range(num_platforms):
                bricks_of_same_category = [b for b in range(num_bricks) if categories[b] == c]
                opt.add(AtMost(*[brick_on[b][p][t] for b in bricks_of_same_category], 1))

    # Ensure from and to positions are distinct for each move
    for t in range(max_steps):
        for p in range(num_platforms):
            opt.add(Not(And(from_pos[p][t], to_pos[p][t])))

    # Uniqueness of from and to variables (one move per time step)
    for t in range(max_steps):
        opt.add(Or([from_pos[p][t] for p in range(num_platforms)]))
        opt.add(Or([to_pos[p][t] for p in range(num_platforms)]))
        for p in range(num_platforms):
            opt.add(Implies(from_pos[p][t], And([Not(from_pos[p2][t]) for p2 in range(num_platforms) if p2 != p])))
            opt.add(Implies(to_pos[p][t], And([Not(to_pos[p2][t]) for p2 in range(num_platforms) if p2 != p])))

    # Moving bricks: if a brick is moving, its next position must be different from the current one
    for b in range(num_bricks):
        for t in range(max_steps - 1):
            for p in range(num_platforms):
                opt.add(Implies(brick_on[b][p][t], Or([from_pos[p2][t] for p2 in range(num_platforms) if p2 != p])))

    # Non-moving bricks: if a brick is not moving, it stays on the same platform
    for b in range(num_bricks):
        for t in range(max_steps - 1):
            for p in range(num_platforms):
                opt.add(Implies(Not(Or([robot_move[r][b][t] for r in range(num_robots)])),
                            brick_on[b][p][t + 1] == brick_on[b][p][t]))

    # Example of cost function (for demonstration): Minimize the number of total movements
    cost = Sum(
        [If(robot_move[r][b][t], 1, 0) for r in range(num_robots) for b in range(num_bricks) for t in range(max_steps)])
    opt.minimize(cost)

    # Solve the problem
    if opt.check() == sat:
        model = opt.model()
        # Output the solution
        for t in range(max_steps + 1):
            for r in range(num_robots):
                for p in range(num_platforms):
                    if model.eval(robot_on[r][p][t]):
                        print(f"At time {t}, robot {r} is on platform {p}")
            for b in range(num_bricks):
                for p in range(num_platforms):
                    if model.eval(brick_on[b][p][t]):
                        print(f"At time {t}, brick {b} is on platform {p}")
    else:
        print("No solution found.")
num_platforms = 1  # Ensure this is correct
num_bricks = 4
init_positions = [0, 1, 2, 3]
multi_robot_moving_bricks(4,1,3,1,10,[1,0,2,3],[4,5,6,7])