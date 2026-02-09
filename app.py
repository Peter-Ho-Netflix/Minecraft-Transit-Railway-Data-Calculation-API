from fastapi import FastAPI
from fastapi.params import Query
from sympy import symbols, Eq, solve, latex
import math

app = FastAPI()

@app.get("/", tags=["根"])
def read_root():
    return {"message": "Hello, World!"}

@app.get(
    "/calculate-distance", 
    description="计算在固定坡度要求下，升起对应高度所需的距离",
    tags=["计算"],
    responses={
        200: {
            "description": "成功",
            "content": {
                "application/json": {
                    "example": {
                        "distance": 10.0,
                        "distance_rounded": 10,
                        "slope_length": 20.0,
                        "solution": {"distance": {
                            "raw": ["10.0", "10.0"],
                            "latex": ["10.0", "10.0"],
                            "values": [10.0, 10.0],
                        }, "radius": {
                            "raw": ["10.0", "10.0"],
                            "latex": ["10.0", "10.0"],
                            "values": [10.0, 10.0],
                        }},
                    },
                },
            },
        },
    },)
def calculate_distance(slope: float = Query(..., description="坡度，以斜率表示", ge=0), height: float = Query(..., description="高度，单位：米", ge=0)):
    x = symbols('x')
    slope_inverse = 1/slope
    equation0 = Eq(x**2 + (slope_inverse*x)**2, (slope_inverse*x+height/2)**2)
    solution0 = solve(equation0, x)
    distance = next(float(s) for s in solution0 if float(s) > 0) * 2
    r = symbols('r')
    equation1 = Eq((r/(2*math.tan(slope)) - height/2)/(r/(2*math.tan(slope))), math.cos(slope))
    solution1 = solve(equation1, r)
    slope_length = [float(s) for s in solution1]
    radius = [float(s) for s in solution1]
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

@app.get("/calculate_parallel_turnout_distance", description="计算平行道岔间为了满足转弯半径要求所需要经过的距离", tags=["计算"], responses={
    200: {
        "description": "成功",
        "content": {
            "application/json": {
                "example": {
                    "distance": 10.0,
                    "distance_rounded": 10,
                    "solution": {
                        "raw": ["10.0"],
                        "latex": ["10.0"],
                        "values": [10.0],
                    },
                },
            },
        },
    },
    },)
def calculate_parallel_turnout_distance(radius: float = Query(..., description="转弯半径，单位：米", ge=0), spacing: float = Query(..., description="平行道岔间距，单位：米", ge=0)):
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
