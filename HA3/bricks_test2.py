from z3 import *

# Parameters for the problem: number of bricks, number of positions, and classes
def moving_bricks_with_classes(num_bricks, num_pos, classes):
    opt = Optimize()
    max_steps = 200

    # Mapping bricks to classes
    brick_class = classes
    num_classes = len(set(classes))

    # Variables: on(b, p, t), obj_class(c, t), from(p, t), to(p, t)
    obj_class = [[Bool(f'obj_class_{c}_{t}') for t in range(max_steps)] for c in range(num_classes)]
    on = [[[Bool(f"on_{b}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_pos)] for b in range(num_bricks)]
    from_pos = [[Bool(f"from_{p}_{t}") for t in range(max_steps)] for p in range(num_pos)]
    to_pos = [[Bool(f"to_{p}_{t}") for t in range(max_steps)] for p in range(num_pos)]

    steps = Int('steps')
    opt.add(steps >= 0)
    opt.add(steps <= max_steps)
    opt.minimize(steps)

    # Initial condition: All bricks start at their initial positions
    for b in range(num_bricks):
        opt.add(on[b][0][0])  # Each brick starts at the initial position (adjust to reflect categories)
        for p in range(1, num_pos):
            opt.add(Not(on[b][p][0]))

    # Final condition: Bricks reach the goal position
    for b in range(num_bricks):
        for t in range(max_steps + 1):
            opt.add(Implies(steps == t, on[b][num_pos - 1][t]))
            for p in range(num_pos - 1):
                opt.add(Implies(steps == t, Not(on[b][p][t])))

    # Class-based movement constraints
    for t in range(max_steps):
        opt.add(Or([obj_class[c][t] for c in range(num_classes)]))  # At least one class is moving
        for c in range(num_classes):
            # Each time step, only one brick from each class can move
            opt.add(Implies(obj_class[c][t], And([Not(obj_class[c2][t]) for c2 in range(num_classes) if c2 != c])))

    # Ensure no two objects from the same class are on the same position
    # Ensure no two objects from the same class are on the same position at the same time
    for b1 in range(num_bricks):
        for b2 in range(b1 + 1, num_bricks):
            if brick_class[b1] == brick_class[b2]:  # Only apply to bricks from the same class
                for t in range(max_steps + 1):
                    for p in range(num_pos):
                        # Ensure that bricks b1 and b2, if in the same class, are not at the same position at the same time
                        opt.add(Implies(on[b1][p][t], Not(on[b2][p][t])))

    # for b1 in range(num_bricks):
    #     for b2 in range(b1 + 1, num_bricks):
    #         for t in range(max_steps + 1):
    #             for p in range(num_pos):
    #                 opt.add(Implies(Or(Not(on[b1][p][steps])), Not(on[b2][p][steps])))
    # Uniqueness of from and to variables (one move per time step)
    for t in range(max_steps):
        opt.add(Or([from_pos[tw][t] for tw in range(num_pos)]))  # At least one pos is the from pos
        opt.add(Or([to_pos[tw][t] for tw in range(num_pos)]))  # At least one pos is the to pos
        for tw in range(num_pos):
            # From one pos only at each step
            opt.add(Implies(from_pos[tw][t], And([Not(from_pos[tw2][t]) for tw2 in range(num_pos) if tw2 != tw])))
            # To one pos only at each step
            opt.add(Implies(to_pos[tw][t], And([Not(to_pos[tw2][t]) for tw2 in range(num_pos) if tw2 != tw])))

    # only move 1 category at each timestep
    for t in range(max_steps):
        # Ensure only one category of bricks is moving at each time step
        opt.add(Or([obj_class[c][t] for c in range(num_classes)]))  # At least one disk is moving
        for c in range(num_classes):
            opt.add(Implies(obj_class[c][t], And([Not(obj_class[c2][t]) for c2 in range(num_classes) if c2 != c])))

    # Non-moving disks
    for c in range(num_classes):
        for tw in range(num_pos):
            for t in range(max_steps - 1):
                # If disk d is not moving and is on pos tw, it should remain on tw in the next step
                opt.add(Implies(And(Not(obj_class[c][t]), on[c][tw][t]), on[c][tw][t + 1]))

    # Ensure from_pos and to_pos are distinct
    for t in range(max_steps):
        for tw in range(num_pos):
            opt.add(Not(And(from_pos[tw][t], to_pos[tw][t])))

    # Ensure valid brick movements between positions
    for b in range(num_bricks):
        for p in range(num_pos):
            for p2 in range(num_pos):
                if p != p2:
                    for t in range(max_steps - 1):
                        opt.add(Implies(
                            And(obj_class[brick_class[b]][t], from_pos[p][t], to_pos[p2][t]),
                            And(on[b][p2][t + 1], Not(on[b][p][t + 1]))
                        ))

    if opt.check() == sat:
        model = opt.model()
        print(f"Solved in {model[steps]} steps")
        for t in range(max_steps + 1):
            print(f"At time {t}:")
            for b in range(num_bricks):
                for p in range(num_pos):
                    if model.eval(on[b][p][t]) == True:
                        print(f"  Brick {b} is at position {p}")
    else:
        print("No solution found")


# Example usage
moving_bricks_with_classes(4, 3, [0, 0, 1, 1])
