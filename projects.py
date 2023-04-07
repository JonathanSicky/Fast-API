import mysql.connector


def mySQL_Connection():
    mySQL = mysql.connector.connect(
        host="localhost", user="root", password="", database="manageapi")
    myCursor = mySQL.cursor(dictionary=True)
    return mySQL, myCursor


def get_projects():
    mySQL, myCursor = mySQL_Connection()

    myCursor.execute('SELECT * FROM `projects`')
    stringprojects = myCursor.fetchall()

    projects = []
    for project in stringprojects:
        project_dict = {}
        project_dict['project_id'] = project['project_id']
        project_dict['project_name'] = project['project_name']
        project_dict['project_url'] = project['project_url']
        project_dict['project_key'] = project['project_key']
        project_dict['project_section'] = project['project_section']
        projects.append(project_dict)
    mySQL.close()
    myCursor.close()
    return projects

# def get_products():
#     mySQL, myCursor = mySQL_Connection()

#     myCursor.execute('SELECT * FROM `products`')
#     mystringproducts = myCursor.fetchall()

#     myCursor.execute('SELECT * FROM `products_component`')
#     mystringcomponents = myCursor.fetchall()

#     products = []
#     for product in mystringproducts:
#         product_dict = {}
#         product_dict['product_id'] = product['product_id']
#         product_dict['product_name'] = product['product_name']
#         product_dict['product_price'] = product['product_price']
#         product_dict['product_cost'] = product['product_cost']
#         product_dict['product_total'] = product['product_total']
#         product_dict['product_detail'] = []

#         for component in mystringcomponents:
#             if component['component_id'] == product['product_id']:
#                 component_dict = {}
#                 component_dict['component_name'] = component['component_name']
#                 component_dict['component_type'] = component['component_type']
#                 product_dict['product_detail'].append(component_dict)
#         products.append(product_dict)

#     mySQL.close()
#     myCursor.close()

#     return products
