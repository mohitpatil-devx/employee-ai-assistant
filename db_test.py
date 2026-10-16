import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="employee_analytics",
    user="postgres",
    password="Timo@2222"
)

cursor = connection.cursor()

cursor.execute("SELECT version();")

result = cursor.fetchone()

print("Connected to PostgreSQL!")
print(result[0])

cursor.close()
connection.close()