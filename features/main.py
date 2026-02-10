import math
from sympy import symbols, Eq, solve, latex


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
    """計算平行道岔間為滿足轉彎半徑要求所需要經過的距離。"""
    x = symbols('x')
    equation = Eq(x**2 + (spacing)**2, (radius*2)**2)
    solution = solve(equation, x)
    distance = next(float(s) for s in solution if float(s) > 0)
    return {
        "distance": distance,
        "distance_rounded": math.ceil(distance),
        "solution": {
            "raw": [str(s) for s in solution],
            "latex": [latex(s) for s in solution],
            "values": [float(s) for s in solution],
        },
    }
