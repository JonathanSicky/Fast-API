from fastapi import status, Response
import mysql.connector


def mySQL_Connection():
    mySQL = mysql.connector.connect(
        host="localhost", user="root", password="", database="manageapi")
    myCursor = mySQL.cursor(dictionary=True)
    return mySQL, myCursor


def get_projectid(id: int, response: Response):
    mySQL, myCursor = mySQL_Connection()

    # myproducts = 'SELECT * FROM `products` WHERE `product_id` = %s'
    # val = (id, )
    # myCursor.execute(myproducts, val)
    # mystringproducts = myCursor.fetchone()

    # mycomponents = 'SELECT * FROM `products_component` WHERE `component_id` = %s'
    # val = (id, )
    # myCursor.execute(mycomponents, val)
    # mystringcomponents = myCursor.fetchall()

    # if mystringproducts is None:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": "ไม่มีสินค้าชิ้นนี้ในฐานข้อมูล"}
    # else:
    #     result = {}
    #     result['product_id'] = mystringproducts['product_id']
    #     result['product_name'] = mystringproducts['product_name']
    #     result['product_price'] = mystringproducts['product_price']
    #     result['product_total'] = mystringproducts['product_total']

    #     if mystringcomponents:
    #         component = []
    #         for data in mystringcomponents:
    #             components = {}
    #             components['name'] = data['component_name']
    #             components['value'] = data['component_type']
    #             component.append(components)
    #         result['product_component'] = component
    #     else:
    #         result['product_component'] = None

    #     mySQL.close()
    #     myCursor.close()
    #     response.status_code = status.HTTP_200_OK
    #     return result
