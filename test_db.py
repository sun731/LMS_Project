import pymysql
from config import *

try:
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    print("✅ Database Connected Successfully!")

    connection.close()

except Exception as e:
    print("❌", e)
