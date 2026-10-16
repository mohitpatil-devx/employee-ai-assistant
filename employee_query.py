import psycopg2


def get_salary_summary():
    connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="employee_analytics",
        user="postgres",
        password="Timo@2222"
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            department,
            COUNT(*) AS employee_count,
            AVG(salary) AS average_salary
        FROM employees
        WHERE active = TRUE
        GROUP BY department;
    """)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results


summary = get_salary_summary()

print("Salary Summary:\n")

for row in summary:
    print(row)