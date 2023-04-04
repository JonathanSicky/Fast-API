# Config FastAPI
from fastapi import FastAPI, Response, status, HTTPException

# Request API
import requests

# Share Port
from fastapi.middleware.cors import CORSMiddleware

# Config Json 
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# Connection MySQL
import mysql.connector

from product import get_projects, mySQL_Connection
from productid import get_productid

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/projects")
def read_products():
    products = get_projects()
    return JSONResponse(content=jsonable_encoder(products))

# @app.get("/api/products/{id}")
# def read_product(id: int, response: Response):
#     return get_productid(id, response)

@app.post("/api/projects/post")
async def insert_user(data: dict):
    Project_name = data.get("PROJECT_NAME")
    Project_api = data.get("API_URL")
    Project_key = data.get("API_KEY")
    Project_section = data.get("PROJECT_SECTION")

    if not all ([Project_name, Project_api, Project_key, Project_section]):
        raise HTTPException(status_code=400, detail="กรุณากรอกข้อมูลให้ครบถ้วนก่อนที่จะบันทึกลงฐานข้อมูล")
    try:
        mySQL, myCursor = mySQL_Connection()

        Database = "INSERT INTO `projects` (`project_name`, `project_url`, `project_key`, `project_section`) VALUES (%s, %s, %s, %s)"
        Variable = (Project_name, Project_api, Project_key, Project_section)
        myCursor.execute(Database, Variable)

        mySQL.commit()
        mySQL.close()
        myCursor.close()
        return JSONResponse(content=jsonable_encoder({"message" : "คุณได้บันทึกลงฐานข้อมูลเรียบร้อยแล้ว"}))
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
