from z3 import *

# Parameters for the problem: number of disks, number of towers, and classes
def moving_bricks_with_classes(num_bricks, num_pos, classes):
    # Create Z3 optimization solver
    opt = Optimize()

    # Maximum possible steps is arbitrary, just needs to be large enough
    max_steps = 200  # Max possible steps as an upper bound (arbitrary large enough)

    # Create a mapping of disks to their classes (e.g., disks 0-1 are in class 0, disks 2-3 are in class 1)
    brick_class = classes  # A list of length num_disks that assigns each disk to a class
    num_classes = len(set(classes))
    class_indices = {c: [] for c in range(num_classes)}

    # Variables: on(d, tw, t), obj(d, t), from(tw, t), to(tw, t)
    obj_class = [[Bool(f'obj_class_{c}_{t}') for t in range(max_steps)] for c in range(num_classes)]

    on = [[[Bool(f"on_{d}_{tw}_{t}") for t in range(max_steps + 1)] for tw in range(num_pos)] for d in range(num_classes)]
    from_pos = [[Bool(f"from_{tw}_{t}") for t in range(max_steps)] for tw in range(num_pos)]
    to_pos = [[Bool(f"to_{tw}_{t}") for t in range(max_steps)] for tw in range(num_pos)]

    # Variable to count the steps
    steps = Int('steps')
    opt.add(steps >= 0)
    opt.add(steps <= max_steps)

    # Initial condition: All class are on the first pos at step 0
    for c in range(num_classes):
        opt.add(on[c][0][0])  # class c is on the first pos at time 0
        for tw in range(1, num_pos):
            opt.add(Not(on[c][tw][0]))  # class c is not on other pos at time 0

    # Final condition: All class are on the last pos at the final step
    for c in range(num_classes):
        for t in range(max_steps + 1):
            # Disk d must be on the last pos if t is equal to steps
            opt.add(Implies(steps == t, on[c][num_pos - 1][t]))
            # Disk d must NOT be on any other pos at step t
            for tw in range(num_pos - 1):
                opt.add(Implies(steps == t, Not(on[c][tw][t])))

    # Precondition I: No disk can be moved if a smaller disk from the same class is on the same pos
    # for d in range(1, num_bricks):
    for c in range(num_classes):
        for tw in range(num_pos):
            for t in range(max_steps):
                smaller_on_same_pos = Or([on[sd][tw][t] for sd in range(c) if brick_class[sd] == brick_class[c]])
                opt.add(Implies(And(on[c][tw][t], smaller_on_same_pos), Not(obj_class[c][t])))

    # Precondition II: No disk can be moved to a pos with a smaller disk from the same class already there
    # for d in range(1, num_bricks):
    for c in range(num_classes):
        for tw in range(num_pos):
            for t in range(max_steps):
                smaller_on_target_pos = Or([on[sd][tw][t] for sd in range(c) if brick_class[sd] == brick_class[c]])
                opt.add(Implies(And(obj_class[c][t], to_pos[tw][t]), Not(smaller_on_target_pos)))

    # Uniqueness of from and to variables (one move per time step)
    for t in range(max_steps):
        opt.add(Or([from_pos[tw][t] for tw in range(num_pos)]))  # At least one pos is the from pos
        opt.add(Or([to_pos[tw][t] for tw in range(num_pos)]))  # At least one pos is the to pos
        for tw in range(num_pos):
            # From one pos only at each step
            opt.add(Implies(from_pos[tw][t], And([Not(from_pos[tw2][t]) for tw2 in range(num_pos) if tw2 != tw])))
            # To one pos only at each step
            opt.add(Implies(to_pos[tw][t], And([Not(to_pos[tw2][t]) for tw2 in range(num_pos) if tw2 != tw])))

    #only move 1 category at each timestep
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

    # Ensure valid movements between start and end pos
    for c in range(num_classes):
        for tw in range(num_pos):
            for tw2 in range(num_pos):
                if tw != tw2:
                    for t in range(max_steps - 1):
                        opt.add(Implies(
                            And(obj_class[c][t], from_pos[tw][t], to_pos[tw2][t]),
                            And(
                                on[c][tw2][t + 1],  # Ensure brick is on the target pos
                                And([Not(on[c][tw3][t + 1]) for tw3 in range(num_pos) if tw3 != tw2])  # Ensure not on other pos
                            )
                        ))

    # Optimize the step count
    opt.minimize(steps)

    # Check if the solution is feasible
    if opt.check() == sat:
        model = opt.model()
        print(f"Solved in {model[steps]} steps")
        # print("\nMovement log:")
        # for t in range(max_steps + 1):
        #     print(f"At time {t}:")
        #     for b in range(num_bricks):
        #         for p in range(num_pos):
        #             if model.eval(on[b][p][t]) == True:
        #                 print(f"  Brick {b} is at position {p}")
    else:
        print("No solution found")

# Example usage: Solve pos of bricks categories with 4 bricks, 3 pos, and bricks grouped by 2 class
# Classes: bricks 0-1 are in class 0, bricks 2-3 are in class 1
# moving_bricks_with_classes(4, 3, [0, 0, 1, 1])
# 5 bricks, 3 positions, divided into 3 classes
moving_bricks_with_classes(5, 3, [0, 0, 2, 1, 1])
