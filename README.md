# @app.get("/api/products")
# def get_products(response: Response):
#     connect()

#     mycursor.execute('SELECT * FROM `products`')
#     mystringproducts = mycursor.fetchall()

#     mycursor.execute('SELECT * FROM `products_component`')
#     mystringcomponents = mycursor.fetchall()

#     products = []
#     for product in mystringproducts:
#         product_dict = {}
#         product_dict['product_id'] = product['product_id']
#         product_dict['product_name'] = product['product_name']
#         product_dict['product_price'] = product['product_price']
#         product_dict['product_total'] = product['product_total']
#         product_dict['product_total'] = product['product_total']
#         product_dict['product_cost'] = product['product_cost']
#         product_dict['product_detail'] = []

#         for component in mystringcomponents:
#             if component['component_id'] == product['product_id']:
#                 component_dict = {}
#                 component_dict['component_name'] = component['component_name']
#                 component_dict['component_type'] = component['component_type']
#                 product_dict['product_detail'].append(component_dict)
#         products.append(product_dict)
        
#     myconnection.close()
#     mycursor.close()
#     response.status_code = status.HTTP_200_OK
#     return products

# @app.get("/api/products/{id}")
# def get_product(id: int, response: Response):
#     connect()

#     myproducts = 'SELECT * FROM `products` WHERE `product_id` = %s'
#     val = (id, )
#     mycursor.execute(myproducts, val)
#     mystringproducts = mycursor.fetchone()

#     mycomponents = 'SELECT * FROM `products_component` WHERE `component_id` = %s'
#     val = (id, )
#     mycursor.execute(mycomponents, val)
#     mystringcomponents = mycursor.fetchall()

#     if mystringproducts is None:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": "ไม่มีสินค้าชิ้นนี้ในฐานข้อมูล"}
#     else:
#         result = {}
#         result['product_id'] = mystringproducts['product_id']
#         result['product_name'] = mystringproducts['product_name']
#         result['product_price'] = mystringproducts['product_price']
#         result['product_total'] = mystringproducts['product_total']
#         result['product_cost'] = mystringproducts['product_cost']
        
#         if mystringcomponents:
#             component = []
#             for data in mystringcomponents:
#                 components = {}
#                 components['name'] = data['component_name']
#                 components['value'] = data['component_type']
#                 component.append(components)
#             result['product_component'] = component
#         else:
#             result['product_component'] = None
        
#         myconnection.close()
#         mycursor.close()
#         response.status_code = status.HTTP_200_OK
#         return result
    
# @app.post("/api/product/insert")
# async def insert_product(data: dict):
#     product_name = data.get("product_name")
#     product_price = data.get("product_price")
#     product_total = data.get("product_total")

#     component_name = data.get("component_name")
#     component_type = data.get("component_type")

#     if not all([product_name, product_price, product_total]):
#         raise HTTPException(status_code=400, detail="กรุณากรอกข้อมูลให้ครบถ้วนก่อนที่จะบันทึกลงฐานข้อมูล")

#     try:
#         connect()
        
#         # Insert `products` table
#         sql = "INSERT INTO `products` (product_name, product_price, product_total) VALUES (%s, %s, %s)"
#         val = (product_name, product_price, product_total)
#         mycursor.execute(sql, val)

#         # Insert `products_component` table
#         sqlcomponent = "INSERT INTO `products_component` (component_id, component_name, cmoponent_type) VALUES (%d, %s, %d)"
#         val = (component_name, component_type)
#         mycursor.exeute(sqlcomponent, val)

#         # Testing Insert Products_Coponent

#         myconnection.commit()
#         mycursor.close()
#         myconnection.close()

#         return JSONResponse(content=jsonable_encoder({"message": "คุณได้เพิ่มสินค้าลงฐานข้อมูลเรียบร้อยแล้ว"}), status_code=201)
#     except mysql.connector.Error as err:
#         raise HTTPException(status_code=500, detail=str(err))