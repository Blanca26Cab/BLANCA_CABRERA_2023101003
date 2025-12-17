import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host='db', 
        user='db_user',  
        password='1234',  
        database='tienda_pod',  
        auth_plugin_map={
        "caching_sha2_password": "pymysql.auth.caching_sha2_password"
    }

    )
    return conn