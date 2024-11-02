from z3 import *


def robot_move_min_moves(num_bricks, num_positions, max_steps, init, goal):
    # 创建 Z3 优化器
    opt = Optimize()

    # 定义状态变量: on(b, p, t), 表示砖块 b 是否在位置 p, 时间步 t
    on = [[[Bool(f"on_{b}_{p}_{t}") for t in range(max_steps + 1)] for p in range(num_positions)] for b in
          range(num_bricks)]

    # 定义 obj[b][t]: 砖块 b 在时间步 t 是否被移动
    obj = [[Bool(f"obj_{b}_{t}") for t in range(max_steps)] for b in range(num_bricks)]

    # 定义 from_pos[p][t]: 表示砖块在时间步 t 从位置 p 开始移动
    from_pos = [[Bool(f"from_{p}_{t}") for t in range(max_steps)] for p in range(num_positions)]

    # 定义 to_pos[p][t]: 表示砖块在时间步 t 移动到位置 p
    to_pos = [[Bool(f"to_{p}_{t}") for t in range(max_steps)] for p in range(num_positions)]

    # 定义变量：steps 表示总的移动步数
    steps = Int('steps')
    opt.add(steps >= 0)
    opt.add(steps <= max_steps)

    # 目标函数：最小化移动次数
    opt.minimize(steps)

    # 约束 1: 起始条件，每个砖块在 t = 0 时位于初始位置
    for b in range(num_bricks):
        opt.add(on[b][init[b]][0])  # 砖块 b 在位置 init[b] 上
        for p in range(num_positions):
            if p != init[b]:
                opt.add(Not(on[b][p][0]))  # 确保砖块 b 仅在初始位置上

    # 约束 2: 终止条件，每个砖块必须在某一时间步内到达目标位置
    for b in range(num_bricks):
        # 强制砖块 b 在 steps 步时到达目标位置
        for t in range(max_steps + 1):
            opt.add(Implies(steps == t, on[b][goal[b]][t]))  # 砖块 b 必须在 steps 步时到达目标位置
            # 强制砖块 b 在 steps 步时不在其他位置
            for p in range(num_positions):
                if p != goal[b]:
                    opt.add(Implies(steps == t, Not(on[b][p][t])))

    # 约束 3: 只有一个砖块可以在同一时间移动
    for t in range(max_steps):
        opt.add(Or([obj[b][t] for b in range(num_bricks)]))  # 至少有一个砖块移动
        for b in range(num_bricks):
            opt.add(Implies(obj[b][t], And([Not(obj[b2][t]) for b2 in range(num_bricks) if b2 != b])))  # 只能一个砖块移动

    # 约束 4: 两个砖块不能占据相同的位置
    for t in range(max_steps + 1):
        for p in range(num_positions):
            for b1 in range(num_bricks):
                for b2 in range(b1 + 1, num_bricks):
                    opt.add(Or(Not(on[b1][p][t]), Not(on[b2][p][t])))  # 不能有两个砖块占据同一位置

    # 约束 5: 起点和终点不能相同
    for t in range(max_steps):
        for p in range(num_positions):
            opt.add(Implies(from_pos[p][t], Not(to_pos[p][t])))

    # 约束 6: 如果砖块没有在当前时间步移动，它将保持在同一个位置
    for b in range(num_bricks):
        for p in range(num_positions):
            for t in range(max_steps):
                opt.add(Implies(Not(obj[b][t]), on[b][p][t] == on[b][p][t + 1]))  # 砖块在 t 时刻不移动

    # 约束 7: 如果砖块移动，它的下一个位置必须和当前的位置不同
    for b in range(num_bricks):
        for p in range(num_positions):
            for t in range(max_steps - 1):
                for p2 in range(num_positions):
                    if p != p2:
                        opt.add(Implies(And(obj[b][t], from_pos[p][t], to_pos[p2][t]),
                                        And(on[b][p2][t + 1], Not(on[b][p][t + 1]))))  # 砖块移动到不同的位置

    # 约束 8: 砖块不能移动到一个第三个位置
    for b in range(num_bricks):
        for t in range(max_steps):
            for p1 in range(num_positions):
                for p2 in range(num_positions):
                    for p3 in range(num_positions):
                        if p1 != p2 and p2 != p3:
                            opt.add(Not(And(on[b][p1][t], obj[b][t], from_pos[p1][t], to_pos[p2][t], on[b][p3][t + 1])))

    # 约束 9: 砖块每次移动只能移动一步 (相邻位置)
    for b in range(num_bricks):
        for t in range(max_steps):
            for p in range(num_positions):
                for p2 in range(num_positions):
                    if abs(p - p2) != 1:  # 只有相邻的位置才能被移动
                        opt.add(Implies(And(from_pos[p][t], to_pos[p2][t]), False))  # 确保每次只能移动一步

    # 求解
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


# 示例使用: 3个砖块，5个位置，初始和目标位置
num_bricks = 3
num_positions = 5
max_steps = 10  # 最大步数
init = [0, 1, 2]  # 初始位置
goal = [4, 3, 1]  # 目标位置

robot_move_min_moves(num_bricks, num_positions, max_steps, init, goal)
