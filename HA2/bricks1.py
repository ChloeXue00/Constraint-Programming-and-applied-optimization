from z3 import *


def robot_move_min_moves(num_bricks, num_positions, max_steps, init, goal):
    #
    opt = Optimize()

    # on(b, p, t), if brick b at p, at timestep t
    on = [[[Bool(f"on_{b}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_positions)] for b in
          range(num_bricks)]

    #  obj[b][t]: brick b at timestep t is moved
    obj = [[Bool(f"obj_{b}_{t}") for t in range(max_steps)] for b in range(num_bricks)]

    #  from_pos[p][t]: brick b is moved from p at timestep
    from_pos = [[Bool(f"from_{p}_{t}") for t in range(max_steps)] for p in range(num_positions)]

    # to_pos[p][t]: brick b move to p at timestep t
    to_pos = [[Bool(f"to_{p}_{t}") for t in range(max_steps)] for p in range(num_positions)]

    # steps =total steps
    steps = Int('steps')
    opt.add(steps >= 0)
    opt.add(steps <= max_steps)

    # obj：min movements
    opt.minimize(steps)

    # constraint 1: init position at t=0
    for b in range(num_bricks):
        opt.add(on[b][init[b]][0])  # brick b on position init[b]
        for p in range(num_positions):
            if p != init[b]:
                opt.add(Not(on[b][p][0]))  #

    # constraint 2: end position at t = steps
    for b in range(num_bricks):
        # force brick b to be at end pos at final timestep
        for t in range(max_steps + 1):
            opt.add(Implies(steps == t, on[b][goal[b]][t]))  # b reach end pos at final t
            # not at other pos at final t
            for p in range(num_positions):
                if p != goal[b]:
                    opt.add(Implies(steps == t, Not(on[b][p][t])))


    # constraint 3: only one brick can move at each timestep
    for t in range(max_steps):
        opt.add(Or([obj[b][t] for b in range(num_bricks)]))  #  least 1 brick move at each time step
        for b in range(num_bricks):
            opt.add(Implies(obj[b][t], And([Not(obj[b2][t]) for b2 in range(num_bricks) if b2 != b])))  # only 1 brick move

    # constraint 4: 2 brick cannot at the same pos
    for t in range(max_steps + 1):
        for p in range(num_positions):
            for b1 in range(num_bricks):
                for b2 in range(b1 + 1, num_bricks):
                    opt.add(Or(Not(on[b1][p][t]), Not(on[b2][p][t])))

    # constraint 5: start pos != end pos
    for t in range(max_steps):
        for p in range(num_positions):
            opt.add(Implies(from_pos[p][t], Not(to_pos[p][t])))

    # constraint 6: if not moving, then stay at current pos
    for b in range(num_bricks):
        for p in range(num_positions):
            for t in range(max_steps):
                opt.add(Implies(Not(obj[b][t]), on[b][p][t] == on[b][p][t + 1]))  # no moving at t and t+1

    # constraint 7: if move, next position different with current position
    for b in range(num_bricks):
        for p in range(num_positions):
            for t in range(max_steps - 1):
                for p2 in range(num_positions):
                    if p != p2:
                        opt.add(Implies(And(obj[b][t], from_pos[p][t], to_pos[p2][t]),
                                        And(on[b][p2][t + 1], Not(on[b][p][t + 1]))))  # move to different pos

    # constraint 8: cannot move to 3rd position when moving to 2nd position
    for b in range(num_bricks):
        for t in range(max_steps):
            for p1 in range(num_positions):
                for p2 in range(num_positions):
                    for p3 in range(num_positions):
                        if p1 != p2 and p2 != p3:
                            opt.add(Not(And(on[b][p1][t], obj[b][t], from_pos[p1][t], to_pos[p2][t], on[b][p3][t + 1])))

    # # constraint 9: only 1 step everytime(only move to neighbor)
    # for b in range(num_bricks):
    #     for t in range(max_steps):
    #         for p in range(num_positions):
    #             for p2 in range(num_positions):
    #                 if abs(p - p2) != 1:  # only neighbor
    #                     opt.add(Implies(And(from_pos[p][t], to_pos[p2][t]), False))
    # solve
    if opt.check() == sat:
        model = opt.model()
        print(f"Solution found in {model[steps]} steps.")
        for t in range(max_steps + 1):
            for b in range(num_bricks):
                for p in range(num_positions):
                    if model.eval(on[b][p][t]):
                        print(f"Brick {b} is at position {p} at time {t}")
    else:
        print("No solution found.")


#
num_bricks = 3
num_positions = 5
max_steps = 20
init = [0, 1, 2]  # init position
goal = [4, 3, 1]  # target position

robot_move_min_moves(num_bricks, num_positions, max_steps, init, goal)
