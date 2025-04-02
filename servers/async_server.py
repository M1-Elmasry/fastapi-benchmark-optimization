from typing import Coroutine
from fastapi import FastAPI
from aiomysql import create_pool, DictCursor
from pydantic import BaseModel


class Employee(BaseModel):
    id: int
    username: str
    password: str
    email: str
    salary: int
    years_of_experience: int  # between 10 and 20


class dbClient:

    def __init__(self):
        self.pool = None

    async def init_db(self, **kargs):
        self.pool = await create_pool(**kargs)

    async def fetch_one(self, query: str, params: tuple):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                return await cur.fetchone()

    async def fetch_all(self, query: str, params: tuple):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                return await cur.fetchall()

    async def execute(self, query: str, params: tuple):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                await conn.commit()

    async def close(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()


app = FastAPI()

db_client = dbClient()


@app.on_event("startup")
async def startup():
    await db_client.init_db(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="ROOT",
        db="test",
        cursorclass=DictCursor,
        minsize=5,
        maxsize=30,
    )


@app.on_event("shutdown")
async def shutdown():
    await db_client.close()


@app.get("/")
async def root():
    return {"message": "server is up !"}


# io-bound benchmark
@app.get("/employees/{employee_id}", status_code=200)
async def get_employee(employee_id: int):
    emp = await db_client.fetch_one(
        "SELECT * FROM employees WHERE id = %s LIMIT 1", (str(employee_id),)
    )

    if not emp:
        return {"message": "employee not found"}

    return emp


# cpu-bound benchmark
@app.get("/calculate-factorial/{n}", status_code=200)
async def calculate_factorial(n: int):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return {"result": result}


# io-bound with cpu-bound benchmark
@app.get("/employee-exp-factorial/{employee_id}", status_code=200)
async def get_employee_exp_factorial(employee_id: int):
    emp = await db_client.fetch_one(
        "SELECT * FROM employees WHERE id = %s LIMIT 1", (str(employee_id),)
    )

    if not emp:
        return {"message": "employee not found"}

    result = 1
    for i in range(1, emp["years_of_experience"]):
        result *= i
    return {"result": result}
