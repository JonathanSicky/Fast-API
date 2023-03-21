from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

myconnection = None
mycursor = None

def connect():
    global myconnection, mycursor
    myconnection = mysql.connector.connect(host="localhost", user="root", password="", database="manageapi")
    mycursor = myconnection.cursor(dictionary=True)

@app.route("/api/products", methods=["GET"])
def get_products():
    connect()
    
    mycursor.execute('SELECT * FROM `products`')
    mystringproducts = mycursor.fetchall()

    mycursor.execute('SELECT * FROM `products_component`')
    mystringcomponents = mycursor.fetchall()

    products = []
    for product in mystringproducts:
        product_dict = {}
        product_dict['product_id'] = product['product_id']
        product_dict['product_name'] = product['product_name']
        product_dict['product_price'] = product['product_price']
        product_dict['product_total'] = product['product_total']
        product_dict['product_detail'] = []

        for component in mystringcomponents:
            if component['component_id'] == product['product_id']:
                component_dict = {}
                component_dict['component_name'] = component['component_name']
                component_dict['component_type'] = component['component_type']
                product_dict['product_detail'].append(component_dict)
        products.append(product_dict)
        
    myconnection.close()
    mycursor.close()
    return make_response(jsonify(products), 200)


@app.route("/api/products/<int:id>", methods=["GET"])
def get_product(id):
    connect()

    myproducts = 'SELECT * FROM `products` WHERE `product_id` = %s'
    val = (id, )
    mycursor.execute(myproducts, val)
    mystringproducts = mycursor.fetchone()

    mycomponents = 'SELECT * FROM `products_component` WHERE `component_id` = %s'
    val = (id, )
    mycursor.execute(mycomponents, val)
    mystringcomponents = mycursor.fetchall()

    if mystringproducts is None:
        return make_response(jsonify({"message": "ไม่มีสินค้าชิ้นนี้ในฐานข้อมูล"}), 404)
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
        
        myconnection.close()
        mycursor.close()
        return make_response(jsonify(result), 200)
    
@app.route("/api/product/insert", methods=["POST"])
def insert_product():
    data = request.get_json()
    product_name = data.get("product_name")
    product_price = data.get("product_price")
    product_total = data.get("product_total")

    component_name = data.get("component_name")
    component_type = data.get("component_type")

    if not all([product_name, product_price, product_total, component_name, component_type]):
        return make_response(jsonify({"message": "กรุณากรอกข้อมูลให้ครบถ้วนก่อนที่จะบันทึกลงฐานข้อมูล"}), 400)
    try :
        connect()
        sql = "INSERT INTO `products` (product_name, product_price, product_total) VALUES (%s, %d, %d)"
        val = (product_name, product_price, product_total)
        mycursor.execute(sql, val)

        #
        # Insert `products_component`
        #

        myconnection.commit()
        mycursor.close()
        myconnection.close()
        return make_response(jsonify({"message": "คุณได้เพิ่มสินค้าลงฐานข้อมูลเรียบร้อยแล้ว"}), 201)
    except mysql.connector.Error as err:
        return make_response(jsonify({"message": str(err)}), 500)
    




# @app.route("/api/products/create", methods=["POST"])
# def create_product():
#     data = request.get_json()
#     product_name = data.get("product_name")
#     product_total = data.get("product_total")
#     if not all([product_name, product_total]):
#         return make_response(jsonify({"message": "กรุณาระบุข้อมูลให้ครบถ้วน"}), 400)
#     try:
#         connect()
        
#         sql = "INSERT INTO products (product_name, product_total) VALUES (%s, %s)"
#         val = (product_name, product_total)
#         mycursor.execute(sql, val)
#         myconnection.commit()
#         mycursor.close()
#         myconnection.close()
#         return make_response(jsonify({"message": "คุณได้เพิ่มสินค้าลงฐานข้อมูลเรียบร้อยแล้ว"}), 201)
#     except mysql.connector.Error as err:
#         return make_response(jsonify({"message": str(err)}), 500)
    
# @app.route("/api/products/<id>", methods=['PUT'])
# def Sicky_Update(id):
#     connect()
    
#     sql = 'UPDATE `products` SET product_name = %s, product_total = %s WHERE product_id = %s'
#     data = request.get_json()
#     val = (data['product_name'], data['product_total'], id)
#     mycursor.execute(sql, val)
#     myconnection.commit()
#     return make_response(jsonify({"message": "คุณได้อัพเดทสินค้าลงฐานข้อมูลเรียบร้อยแล้ว"}), 200)
