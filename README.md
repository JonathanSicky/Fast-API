# FastAPI

@app.get("/EditFroms/{id}")
def get_product(id: int, response: Response):
    mySQL_Connection()

    myproducts = 'SELECT * FROM `projects` WHERE `project_id` = %s'
    val = (id, )
    myCursor.execute(myproducts, val)
    mystringprojects = myCursor.fetchall()

    if mystringprojects is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "ไม่มีสินค้าชิ้นนี้ในฐานข้อมูล"}
    else:
        result = {}
        result['project_id'] = mystringprojects['project_id']
        result['project_name'] = mystringprojects['project_name']
        result['project_url'] = mystringprojects['project_url']
        result['project_key'] = mystringprojects['project_key']
        result['project_section'] = mystringprojects['project_section']
        
        mySQL.close()
        myCursor.close()
        response.status_code = status.HTTP_200_OK
        return result