import math
from sympy import symbols, Eq, solve, latex, sqrt


def calculate_distance(slope: float, height: float) -> dict:
    """計算在固定坡度要求下，升起對應高度所需的距離。"""
    x = symbols('x')
    slope_inverse = 1 / slope
    equation0 = Eq(x**2 + (slope_inverse*x)**2, (slope_inverse*x+height/2)**2)
    solution0 = solve(equation0, x)
    distance = next(float(s) for s in solution0 if float(s) > 0) * 2
    r = symbols('r')
    equation1 = Eq((r/(2*math.tan(slope)) - height/2)/(r/(2*math.tan(slope))), math.cos(slope))
    solution1 = solve(equation1, r)
    slope_length = [float(s) for s in solution1]
    return {
        "distance": distance,
        "distance_rounded": math.ceil(distance),
        "slope_length": slope_length,
        "solutions": {
            "distance": {
                "raw": [str(s) for s in solution0],
                "latex": [latex(s) for s in solution0],
                "values": [float(s) for s in solution0],
            },
            "radius": {
                "raw": [str(s) for s in solution1],
                "latex": [latex(s) for s in solution1],
                "values": [float(s) for s in solution1],
            },
        },
    }


def calculate_parallel_turnout_distance(radius: float, spacing: float) -> dict:
    """計算平行道岔間為滿足轉彎半徑要求所需要經過的距離。
    幾何關係：r² = (r - spacing/2)² + (x/2)²，約束條件 r >= radius（如中國高鐵 r≥600m）
    """
    x = symbols('x')
    r = symbols('r')
    # 從 r² = (r - spacing/2)² + (x/2)² 解出 r 關於 x 的表達式
    equation = Eq(r**2, (r - spacing/2)**2 + (x/2)**2)
    r_expr = solve(equation, r)[0]  # r = (spacing²/4 + x²/4) / spacing
    # 代入 r >= radius，解出 x 的範圍
    # r_expr >= radius  =>  x >= sqrt(4*radius*spacing - spacing²)
    constraint = Eq(r_expr, radius)
    x_solutions = solve(constraint, x)
    # 取正實數解作為最小間距
    distance = next(
        float(s) for s in x_solutions * 2
        if s.is_real and float(s) > 0
    )
    # 并求出取最小整数情况下线路的实际转弯半径和线路长度
    distance_rounded = math.ceil(distance)
    equation2 = Eq(r**2, (r - spacing/2)**2 + (distance_rounded/2)**2)
    r_solutions = solve(equation2, r)
    radius_rounded = next(float(s) for s in r_solutions if float(s) > 0)
    length = math.sin((distance_rounded/2)/radius_rounded) * radius_rounded * 2
    return {
        "distance": distance,
        "distance_rounded": distance_rounded,
        "radius_rounded": radius_rounded,
        "length": length,
        "solution": {
            "raw": [str(s) for s in x_solutions],
            "latex": [latex(s) for s in x_solutions],
            "values": [float(s) for s in x_solutions],
        },
    }
