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
# import mysql.connector

from product import get_products
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

@app.get("/api/products")
def read_products():
    products = get_products()
    return JSONResponse(content=jsonable_encoder(products))

@app.get("/api/products/{id}")
def read_product(id: int, response: Response):
    return get_productid(id, response)
    
# @app.post("/api/product/post")
# async def insert_product(data: dict):
#     product_name = data.get("product_name")
#     product_price = data.get("product_price")
#     product_total = data.get("product_total")
#     product_cost = data.get("product_cost")

#     # component_name = data.get("component_name")
#     # component_type = data.get("component_type")

#     if not all([product_name, product_price, product_total, product_cost]):
#         raise HTTPException(status_code=400, detail="กรุณากรอกข้อมูลให้ครบถ้วนก่อนที่จะบันทึกลงฐานข้อมูล")

#     try:
#         # Connect to database
#         mySQL_Connection()
        
#         # Insert `products` table
#         insertproducts = "INSERT INTO `products` (product_name, product_price, product_total, product_cost) VALUES (%s, %s, %s, %d)"
#         val = (product_name, product_price, product_total)
#         myCursor.execute(insertproducts, val)

#         # Insert `products_component` table
#         # insertcomponents = "INSERT INTO `products_component` (component_name, component_type) VALUES (%s, %d)"
#         # val = (component_name, component_type)
#         # myCursor.execute(insertcomponents, val)

#         # Commit changes and close connections
#         mySQL.commit()
#         myCursor.close()
#         mySQL.close()

#         return JSONResponse(content=jsonable_encoder({"message": "คุณได้เพิ่มสินค้าลงฐานข้อมูลเรียบร้อยแล้ว"}), status_code=201)
#     except mysql.connector.Error as err:
#         raise HTTPException(status_code=500, detail=str(err))