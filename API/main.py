from fastapi.routing import APIRouter
from fastapi.params import Query

from features import calculate_distance as calc_distance
from features import calculate_parallel_turnout_distance as calc_parallel_turnout_distance

root = APIRouter()


@root.get("/", tags=["根"])
def read_root():
    return {"message": "Hello, World!"}


@root.get(
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
    },
)
def calculate_distance(
    slope: float = Query(..., description="坡度，以斜率表示", ge=0),
    height: float = Query(..., description="高度，单位：米", ge=0),
):
    return calc_distance(slope, height)


@root.get(
    "/calculate_parallel_turnout_distance",
    description="计算平行道岔间为了满足转弯半径要求所需要经过的距离",
    tags=["计算"],
    responses={
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
    },
)
def calculate_parallel_turnout_distance(
    radius: float = Query(..., description="转弯半径，单位：米", ge=0),
    spacing: float = Query(..., description="平行道岔间距，单位：米", ge=0),
):
    return calc_parallel_turnout_distance(radius, spacing)
