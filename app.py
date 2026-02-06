from fastapi import FastAPI
import math

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/calculate", description="计算在固定坡度要求下，升起对应高度所需的距离")
def calculate(slope: float, height: float):
    distance = height / slope
    return {"distance": distance}
