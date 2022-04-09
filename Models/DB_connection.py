import psycopg2
import Users
import Products
import Mapping


ENDPOINT = "agoradb.cqg31s3ekxny.us-east-1.rds.amazonaws.com"
PORT = "5432"
USER = "postgres"
REGION = "us-east-1f"
DBNAME = "postgres"
PASSWORD = "236371Aa!"

try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD)
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)

    print(Users.session.query(Users.User).filter(Users.User.PhoneNum == "0526866526").first().Name)


except Exception as e:
    print("Database connection failed due to {}".format(e))


