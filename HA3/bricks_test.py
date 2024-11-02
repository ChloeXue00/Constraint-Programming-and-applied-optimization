from z3 import *

def robot_move_min_moves_by_classes(num_bricks, num_positions, max_steps, init, goal, brick_classes):
    # 创建 Z3 优化器
    opt = Optimize()

    # 定义砖块类别数量
    num_classes = len(set(brick_classes))  # 自动从类别列表中推导类别数量
    class_indices = {c: [] for c in range(num_classes)}

    # 将砖块按类别分类
    for i, c in enumerate(brick_classes):
        class_indices[c].append(i)

    # 定义状态变量: on(b, p, t), 表示类别 c 的砖块是否在位置 p, 时间步 t
    # on = [[[Bool(f"on_class_{c}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_positions)] for c in range(num_classes)]
        # 定义状态变量: on(b, p, t), 表示砖块 b 是否在位置 p, 时间步 t
    on = [[[Bool(f"on_brick_{b}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_positions)] for b in
              range(num_bricks)]
    # 定义 obj_class[c][t]: 类别 c 在时间步 t 是否被移动
    obj_class = [[Bool(f"obj_class_{c}_{t}") for t in range(max_steps)] for c in range(num_classes)]

    # 定义 from_pos[p][t] 和 to_pos[p][t]: 表示砖块从和到的位置
    from_pos = [[Bool(f"from_{p}_{t}") for t in range(max_steps)] for p in range(num_positions)]
    to_pos = [[Bool(f"to_{p}_{t}") for t in range(max_steps)] for p in range(num_positions)]

    # 定义变量：steps 表示总的移动步数
    steps = Int('steps')
    opt.add(steps >= 0)
    opt.add(steps <= max_steps)

    # 目标函数：最小化移动次数
    opt.minimize(steps)

    # 约束 1: 起始条件，每个砖块在 t = 0 时位于初始位置
    for c in range(num_classes):
        print("category:",c)
        for b in class_indices[c]:
            print("brick{0}，position{1}:".format(b,on[c][init[b]][0]))
            opt.add(on[c][init[b]][0])  # 砖块 b (类别 c) 在位置 init[b] 上
            for p in range(num_positions):
                if p != init[b]:
                    opt.add(Not(on[c][p][0]))  # 确保砖块 b 仅在初始位置上

    for b in range(num_bricks):
        # 砖块 b 必须在 steps 步时到达目标位置 goal[b]
        for t in range(max_steps + 1):
            opt.add(Implies(steps == t, on[b][goal[b]][t]))  # 每个砖块 b 都有自己的目标位置
            # 确保砖块 b 在 steps 步时不在其他位置
            for p in range(num_positions):
                if p != goal[b]:
                    opt.add(Implies(steps == t, Not(on[b][p][t])))

    # 约束 3: 每次只能移动一个类别中的一个砖块

    for c in range(num_classes):
        # print("category:",c)
        # 确保某个类别只有一个砖块移动
        for t in range(max_steps - 1):
            opt.add(Or([obj_class[c][t] for b in class_indices[c]]))
            print("is moving:",[obj_class[c][t]])# 至少有一个类别的一个砖块移动
            for b in class_indices[c]:
                for t in range(max_steps):
                    print("at time t:", t)
                # 每个时间步只能有一个类别的一个砖块移动
            # 确保同一个类别中的其他砖块不移动
            opt.add(Implies(obj_class[c][t], And([Not(obj_class[c2][t]) for c2 in range(num_classes) if c2 != c])))
            # 每次只能移动一个砖块
            opt.add(Implies(obj_class[c][t], And([Not(obj_class[c][t]) for b2 in class_indices[c] if b2 != b])))
    # 约束 4: 砖块只能移动到一个新的位置
    for b in range(num_bricks):
        for t in range(max_steps):
            for p in range(num_positions):
                for p2 in range(num_positions):
                    if p != p2:
                        # 确保砖块只能从 p 移动到 p2
                        opt.add(Implies(from_pos[p][t] & to_pos[p2][t], And(on[b][p2][t + 1], Not(on[b][p][t + 1]))))
    # 约束 5: 如果砖块没有移动，下一个时间步也不会移动
    for b in range(num_bricks):
        for t in range(max_steps - 1):  # 确保范围在 max_steps - 1 内
            # 如果在时间 t 没有移动，则在时间 t + 1 也不会移动
            opt.add(Implies(Not(obj_class[brick_classes[b]][t]), Not(obj_class[brick_classes[b]][t + 1])))

    # 约束 4: 首尾不同
    for t in range(max_steps):
        for p in range(num_positions):
            opt.add(Implies(from_pos[p][t], Not(to_pos[p][t])))


    for b in range(num_bricks):
        for p in range(num_positions):
            for t in range(max_steps - 1):
                for p2 in range(num_positions):
                    if p != p2:
                        opt.add(Implies(And(from_pos[p][t], to_pos[p2][t]),
                                        And(on[b][p2][t + 1], Not(on[b][p][t + 1]))))

    # 求解
    if opt.check() == sat:
        model = opt.model()
        print(f"Solution found in {model[steps]} steps.")
        for t in range(max_steps + 1):
            for b in range(num_bricks):
                for p in range(num_positions):
                    if model.eval(on[b][p][t]) == True:
                        print(f"Brick {b} is at position {p} at time {t}")
    else:
        print("No solution found.")



# 示例使用: 7个砖块，5个位置，初始和目标位置, 以及类别信息
num_bricks = 7
num_positions = 5
max_steps = 200 # 最大步数
init = [0, 1, 2, 0, 1, 2, 3]  # 初始位置
goal = [4, 3, 1, 4, 2, 0, 3]  # 目标位置
brick_classes = [0, 0, 1, 1, 2, 2, 2]  # 砖块的类别

robot_move_min_moves_by_classes(num_bricks, num_positions, max_steps, init, goal, brick_classes)
