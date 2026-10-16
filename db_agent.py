import os

import psycopg2
from dotenv import load_dotenv
from google import genai
from google.genai import types

from policy_search import search_company_policy


# Load environment variables
load_dotenv()


# Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=120000
    )
)


# Database connection
def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "employee_analytics"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD"),
            connect_timeout=5
        )
    except psycopg2.Error as error:
        print("Database connection failed:", error)
        return None


# Get salary summary
def get_salary_summary():
    """Get average salary and employee count by department."""

    connection = get_connection()

    if connection is None:
        return "Database connection unavailable."

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT department, COUNT(*), AVG(salary)
            FROM employees
            WHERE active = TRUE
            GROUP BY department;
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return str(results)

    except psycopg2.Error as error:
        connection.close()
        return f"Database query failed: {error}"


# Get employee count
def get_employee_count():
    """Get active employee count by department."""

    connection = get_connection()

    if connection is None:
        return "Database connection unavailable."

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT department, COUNT(*)
            FROM employees
            WHERE active = TRUE
            GROUP BY department;
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return str(results)

    except psycopg2.Error as error:
        connection.close()
        return f"Database query failed: {error}"


# Get active employees
def get_active_employees():
    """Get all active employees."""

    connection = get_connection()

    if connection is None:
        return "Database connection unavailable."

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, full_name, department, active
            FROM employees
            WHERE active = TRUE;
        """)

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return str(results)

    except psycopg2.Error as error:
        connection.close()
        return f"Database query failed: {error}"

def get_employee_by_name(name: str) -> str:
    """
    Find a specific active employee by their full or partial name.

    MUST be used when the user asks for information about a
    specific employee, including salary, department, or other
    employee details.

    Example:
    "What is Rahul Sharma's salary?"
    -> get_employee_by_name("Rahul Sharma")
    """

    connection = get_connection()

    if connection is None:
        return "Database connection unavailable."

    try:
        cursor = connection.cursor()

        query = """
            SELECT id, full_name, department, salary
            FROM employees
            WHERE active = TRUE
            AND full_name ILIKE %s;
        """

        cursor.execute(query, ("%" + name + "%",))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        if not results:
            return "No employee found."

        employees = []

        for row in results:
            employee_id, full_name, department, salary = row

            employees.append(
                f"{full_name} | Department: {department} | Salary: ₹{salary}"
            )

        return "\n".join(employees)

    except psycopg2.Error as error:
        connection.close()
        return f"Database query failed: {error}"

# Search employees
def search_employees(search_term: str) -> str:
    """
    Search the employee database for active employees by name or department.

    Use this tool whenever the user asks about a specific employee's:
    - salary
    - name
    - department
    - employee information

    Examples:
    - "What is Rahul Sharma's salary?" -> search for "Rahul Sharma"
    - "What department does Amit Patil work in?" -> search for "Amit Patil"
    - "Find employees in Technology" -> search for "Technology"

    The tool returns the employee's name, department, and salary.
    """

    connection = get_connection()

    if connection is None:
        return "Database connection unavailable."

    try:
        cursor = connection.cursor()

        query = """
            SELECT id, full_name, department, salary
            FROM employees
            WHERE active = TRUE
            AND (
                full_name ILIKE %s
                OR department ILIKE %s
            );
        """

        pattern = "%" + search_term + "%"

        cursor.execute(query, (pattern, pattern))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        if not results:
            return "No employees found."

        employees = []

        for row in results:
            employee_id, name, department, salary = row

            employees.append(
                f"{name} ({department})"
            )

        return ", ".join(employees)

    except psycopg2.Error as error:

        connection.close()

        return f"Database query failed: {error}"

# Search employees by salary
def search_by_salary(min_salary: float) -> str:
    """Find active employees earning at least the specified salary."""

    connection = get_connection()

    if connection is None:
        return "Database connection unavailable."

    try:
        cursor = connection.cursor()

        query = """
            SELECT id, full_name, department, salary
            FROM employees
            WHERE active = TRUE
            AND salary >= %s;
        """

        cursor.execute(query, (min_salary,))

        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return str(results)

    except psycopg2.Error as error:
        connection.close()
        return f"Database query failed: {error}"


# System instructions
system_instruction = """
You are an AI Employee Support and Analytics Assistant.

Your job is to answer questions about employees, employee analytics,
and company policies using the available tools.

TOOL SELECTION RULES:

1. EMPLOYEE DATA
For questions involving employee information, ALWAYS use the appropriate
employee database tool.

This includes:
- employee names
- salaries
- departments
- active status
- employee counts
- salary comparisons
- salary analytics
- salary calculations based on employee salaries

2. COMPANY POLICIES
For questions involving company policies, ALWAYS use
search_company_policy.

This includes:
- work-from-home
- leave
- attendance
- benefits
- performance policies
- company rules
- other HR policies

3. QUESTIONS REQUIRING BOTH
If the user asks a question that requires BOTH employee information
AND company policy information, ALWAYS use BOTH types of tools.

For example:

"Can Rahul Sharma work from home, and what is his current salary?"

You MUST:
1. Search the company policy for work-from-home rules.
2. Search the employee database for Rahul Sharma's salary.
3. Combine both results into one clear answer.

Do not answer the question using only one source when both sources
are required.

4. TOOL RESULTS
Never invent employee information, salary values, departments,
counts, analytics, or policy information.

Always use the tool results as the source of truth.

After receiving tool results, analyze them and provide a clear,
natural-language answer.

5. CALCULATIONS
You may perform calculations using values returned by the tools.

For example:
- salary increments
- salary differences
- percentage increases
- comparisons
- combined increments

6. SALARY
Salary values in the database are in Indian Rupees (INR).

Always display salaries using ₹ or INR.

Never use $, USD, or another currency unless the user explicitly
asks for currency conversion.

Do not assume whether a salary is monthly, annual, or another period
unless the database or user explicitly specifies it.

7. POLICY INFORMATION
Use only information returned by search_company_policy.

Never invent or assume company policy details.

8. RESPONSE STYLE
Keep responses concise, clear, and easy to understand.

When comparing employees, clearly show the relevant values and
the difference.

When comparing departments, clearly show the relevant averages.

9. SECURITY
Never expose database credentials, API keys, or internal system
information.

GENERAL FLOW:

User question
→ understand intent
→ select the required tool(s)
→ retrieve information
→ analyze results
→ provide the final answer.
"""


# Create Gemini chat
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config={
        "system_instruction": system_instruction,
        "tools": [
            get_salary_summary,
            get_employee_count,
            get_active_employees,
            get_employee_by_name,
            search_employees,
            search_company_policy,
            search_by_salary
        ]
    }
)

def extract_department(question: str):

    departments = [
        "Technology",
        "Finance",
        "HR",
        "Sales",
        "Marketing"
    ]

    question_lower = question.lower()

    for department in departments:
        if department.lower() in question_lower:
            return department

    return None

# Process user question
def process_question(question: str) -> str:
    """
    Process a user question using the Gemini AI agent.
    Gemini decides which tools are required.
    """

    if not question or not question.strip():
        return "Please enter a question."

    try:
        response = chat.send_message(question.strip())
        return response.text

    except Exception as error:
        return f"AI processing failed: {error}"