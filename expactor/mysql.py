import pymysql


#### 지움 ###

# sql1 = """
#     CREATE TABLE CATEGORY(
#         id int,
#         category varchar(20),
#         segment varchar(20),
#         subsegment varchar(20),
#     )
# """
# cursor.execute(sql1)

# sql2 = """
#     CREATE TABLE PRODUCT (
#         SEGMENT VARCHAR(20),
#         PRODUCT_NAME VARCHAR(100),
#         PRODUCT_CODE VARCHAR(20),
#         ORG_PRICE INT,
#         DISCOUNT_PCT INT,
#         DISCOUNT_PRICE INT
#     );
# """
# cursor.execute(sql2)
#
# sql3 = """
#     CREATE TABLE REVIEW(
#         ID INT PRIMARY KEY AUTO_INCREMENT,
#         PRODUCT_CODE VARCHAR(20),
#         TITLE VARCHAR(100),
#         CONTENT VARCHAR(100)
#     );
# """
# cursor.execute(sql3)
# conn.commit()



def insert_category_tbl(tbl_dict):
    sql = """
        INSERT CATEGORY VALUES(
        '"""+tbl_dict['category']+"""',
        '"""+tbl_dict['segment']+"""',
        '"""+tbl_dict['subsegment']+"""'
        );
    """
    cursor.execute(sql)
    conn.commit()

def insert_product_tbl(tbl_dict):
    sql = """
        INSERT INTO PRODUCT2 VALUES(
            '"""+tbl_dict['category']+"""',
            '"""+tbl_dict['segment']+"""',
            '"""+tbl_dict['subsegment']+"""',
            '"""+tbl_dict['product_name']+"""',
            '"""+tbl_dict['product_code']+"""',            
            """+str(tbl_dict['org_price'])+""",
            """+str(tbl_dict['discount_price'])+""",
            """+str(tbl_dict['discount_pct'])+""",
            """+str(tbl_dict['review_num'])+""",
            '"""+tbl_dict['url']+"""'
        )
    """
    cursor.execute(sql)
    conn.commit()


def read_url(sql):
    cursor.execute(sql)
    result = cursor.fetchall()

    return result


def insert_review_tbl(tbl_dict):
    sql = """
        INSERT INTO REVIEW(PRODUCT_CODE, TOTAL_RATE, WRITER, WRITER_RATE, TITLE, CONTENT, WRITER_OPTION) VALUES(
                '"""+tbl_dict['code']+"""',
                """+tbl_dict['total_rate']+""",
                '"""+tbl_dict['writer']+"""',
                """+tbl_dict['writer_rate']+""",
                '"""+tbl_dict['title']+"""',
                '"""+tbl_dict['content']+"""',
                '"""+tbl_dict['writer_option']+"""'
                );
    """
    cursor.execute(sql)
    conn.commit()







