# Config FastAPI
from fastapi import FastAPI, Response, status, HTTPException

# Request API
import requests

# Share Port
from fastapi.middleware.cors import CORSMiddleware

# Config Json 
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# CreatedAt / UpdatedAt
from datetime import datetime

# Connection MySQL
import mysql.connector

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mySQL = None
myCursor = None

# Function Connect MySQL
def mySQL_Connection():
    global mySQL, myCursor
    mySQL = mysql.connector.connect(host = "localhost", user = "root", password = "", database = "manageapi")
    myCursor = mySQL.cursor(dictionary = True)

@app.get("/api/products")
def get_products(response: Response):
    mySQL_Connection()

    myCursor.execute('SELECT * FROM `products`')
    mystringproducts = myCursor.fetchall()

    myCursor.execute('SELECT * FROM `products_component`')
    mystringcomponents = myCursor.fetchall()

    products = []
    for product in mystringproducts:
        product_dict = {}
        product_dict['product_id'] = product['product_id']
        product_dict['product_name'] = product['product_name']
        product_dict['product_price'] = product['product_price']
        product_dict['product_cost'] = product['product_cost']
        product_dict['product_total'] = product['product_total']
        product_dict['product_detail'] = []

        for component in mystringcomponents:
            if component['component_id'] == product['product_id']:
                component_dict = {}
                component_dict['component_name'] = component['component_name']
                component_dict['component_type'] = component['component_type']
                product_dict['product_detail'].append(component_dict)
        products.append(product_dict)
        
    mySQL.close()
    myCursor.close()
    response.status_code = status.HTTP_200_OK
    return products

@app.get("/api/products/{id}")
def get_product(id: int, response: Response):
    mySQL_Connection()

    myproducts = 'SELECT * FROM `products` WHERE `product_id` = %s'
    val = (id, )
    myCursor.execute(myproducts, val)
    mystringproducts = myCursor.fetchone()

    mycomponents = 'SELECT * FROM `products_component` WHERE `component_id` = %s'
    val = (id, )
    myCursor.execute(mycomponents, val)
    mystringcomponents = myCursor.fetchall()

    if mystringproducts is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "ไม่มีสินค้าชิ้นนี้ในฐานข้อมูล"}
    else:
        result = {}
        result['product_id'] = mystringproducts['product_id']
        result['product_name'] = mystringproducts['product_name']
        result['product_price'] = mystringproducts['product_price']
        result['product_total'] = mystringproducts['product_total']
        
        if mystringcomponents:
            component = []
            for data in mystringcomponents:
                components = {}
                components['name'] = data['component_name']
                components['value'] = data['component_type']
                component.append(components)
            result['product_component'] = component
        else:
            result['product_component'] = None
        
        mySQL.close()
        myCursor.close()
        response.status_code = status.HTTP_200_OK
        return result
    
@app.post("/api/product/post")
async def insert_product(data: dict):
    product_name = data.get("product_name")
    product_price = data.get("product_price")
    product_total = data.get("product_total")

    component_name = data.get("component_name")
    component_type = data.get("component_type")

    if not all([product_name, product_price, product_total]):
        raise HTTPException(status_code=400, detail="กรุณากรอกข้อมูลให้ครบถ้วนก่อนที่จะบันทึกลงฐานข้อมูล")

    try:
        # Connect to database
        mySQL_Connection()
        
        # Insert `products` table
        sql = "INSERT INTO `products` (product_name, product_price, product_total) VALUES (%s, %s, %s)"
        val = (product_name, product_price, product_total)
        myCursor.execute(sql, val)

        # Insert `products_component` table

        # Commit changes and close connections
        mySQL.commit()
        myCursor.close()
        mySQL.close()

        return JSONResponse(content=jsonable_encoder({"message": "คุณได้เพิ่มสินค้าลงฐานข้อมูลเรียบร้อยแล้ว"}), status_code=201)
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))