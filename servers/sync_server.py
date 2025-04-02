from fastapi import FastAPI
from pydantic import BaseModel
from mysql.connector import pooling


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

    def init_db(self, **kargs):
        self.pool = pooling.MySQLConnectionPool(
            pool_size=30,
            **kargs,
        )

    def fetch_one(self, query: str, params: tuple):
        with self.pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, params)
                result = cur.fetchone()
        return result

    def fetch_all(self, query: str, params: tuple):
        with self.pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, params)
                result = cur.fetchone()
        return result

    def execute(self, query: str, params: tuple):
        with self.pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(query, params)
                conn.commit()


app = FastAPI()

db_client = dbClient()


@app.on_event("startup")
def startup():
    db_client.init_db(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="ROOT",
        database="test",
    )


@app.get("/")
def root():
    return {"message": "server is up !"}


# io-bound benchmark
@app.get("/employees/{employee_id}", status_code=200)
def get_employee(employee_id: int):
    emp = db_client.fetch_one(
        "SELECT * FROM employees WHERE id = %s LIMIT 1", (employee_id,)
    )

    if not emp:
        return {"message": "employee not found"}

    return emp


# cpu-bound benchmark
@app.get("/calculate-factorial/{n}", status_code=200)
def calculate_factorial(n: int):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return {"result": result}


# io-bound with cpu-bound benchmark
@app.get("/employee-exp-factorial/{employee_id}", status_code=200)
def get_employee_exp_factorial(employee_id: int):
    emp = db_client.fetch_one(
        "SELECT * FROM employees WHERE id = %s LIMIT 1", (employee_id,)
    )

    if not emp:
        return {"message": "employee not found"}

    result = 1
    for i in range(1, emp["years_of_experience"]):
        result *= i
    return {"result": result}
