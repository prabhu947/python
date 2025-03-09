from dotenv import load_dotenv
import os
import sqlite3
from groq import Groq

load_dotenv()

# Configure Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
DB_PATH = os.path.join(os.path.dirname(__file__), 'student.db')

def get_groq_response(question, prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt[0]
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1000
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def read_sql_query(sql, db):
    try:
        print(f"Executing SQL Query: {sql}")
        
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            
            print(f"Number of rows returned: {len(rows)}")
            return rows
    except sqlite3.Error as e:
        print(f"Database error: {str(e)}")
        return []
    except Exception as e:
        print(f"General error: {str(e)}")
        return []

prompt = [
    """
    You are an SQL expert. Convert English questions to SQL queries for a STUDENT database.
    Table structure: STUDENT(NAME TEXT, CLASS TEXT, SECTION TEXT)
    
    Rules:
    1. Return ONLY the  single SQL query, no explanations
    2. Use double quotes for string literals
    3. Do not include backticks or 'sql' keyword
    4. Keep queries simple and direct
    
    Examples:
    Question: How many students are there?
    SELECT COUNT(*) FROM STUDENT;
    
    Question: Show students in Data Science class
    SELECT * FROM STUDENT WHERE CLASS="Data Science";
    
    Question: List all sections
    SELECT DISTINCT SECTION FROM STUDENT ORDER BY SECTION;
    """
]
def main():
    print("SQL Query Assistant with Groq")
    print("Type 'exit' to quit the program")
    print("-" * 50)

    while True:
        question = input("\nEnter your question: ").strip()
        
        if question.lower() == 'exit':
            print("Goodbye!")
            break
            
        if question:
            print("\nGenerating SQL query...")
            sql_query = get_groq_response(question, prompt)
            
            if sql_query:
                print(f"\nGenerated SQL Query:\n{sql_query}\n")
                
                print("Executing query...")
                results = read_sql_query(sql_query, DB_PATH)
                
                if results:
                    print("\nResults:")
                    print("-" * 50)
                    for row in results:
                        print(row)
                    print("-" * 50)
                else:
                    print("No results found")
        else:
            print("Please enter a valid question")

if __name__ == "__main__":
    main()

















# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# import os
# import sqlite3
# from groq import Groq


# DB_PATH = os.path.join(os.path.dirname(__file__), 'student.db')


# # Configure Groq
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def get_groq_response(question, prompt):
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "system",
#                     "content": prompt[0]
#                 },
#                 {
#                     "role": "user",
#                     "content": question
#                 }
#             ],
#             model="mixtral-8x7b-32768",
#             temperature=0.7,
#             max_tokens=1000
#         )
#         return chat_completion.choices[0].message.content
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return None
# # ...existing code...

# def read_sql_query(sql, db):
#     try:
#         # Print the SQL query for debugging
#         st.write("Executing SQL Query:", sql)
        
#         with sqlite3.connect(db) as conn:
#             cur = conn.cursor()
#             cur.execute(sql)
#             rows = cur.fetchall()
            
#             # Print the number of rows returned
#             st.write(f"Number of rows returned: {len(rows)}")
            
#             return rows
#     except sqlite3.Error as e:
#         st.error(f"Database error: {str(e)}")
#         return []
#     except Exception as e:
#         st.error(f"General error: {str(e)}")
#         return []

# # ...rest of the existing code...

# # Define Your Prompt

# prompt = [
#     """
#     You are an SQL expert. Convert English questions to SQL queries for a STUDENT database.
#     Table structure: STUDENT(NAME TEXT, CLASS TEXT, SECTION TEXT)
    
#     Rules:
#     1. Return ONLY the SQL query, no explanations
#     2. Use double quotes for string literals
#     3. Do not include backticks or 'sql' keyword
#     4. Keep queries simple and direct
    
#     Examples:
#     Question: How many students are there?
#     SELECT COUNT(*) FROM STUDENT;
    
#     Question: Show students in Data Science class
#     SELECT * FROM STUDENT WHERE CLASS="Data Science";
    
#     Question: List all sections
#     SELECT DISTINCT SECTION FROM STUDENT ORDER BY SECTION;
#     """
# ]


# # Streamlit App
# st.set_page_config(page_title="SQL Query Assistant with Groq")
# st.header("Groq-Powered SQL Query Assistant")
# st.subheader("Ask questions about student data in natural language")

# question = st.text_input("Ask your question:", key="input")
# submit = st.button("Generate SQL Query")

# # if submit is clicked
# if submit:
#     st.write("Database path:", DB_PATH)
#     st.write("Database exists:", os.path.exists(DB_PATH))
#     if question:
#         with st.spinner("Generating SQL query..."):
#             sql_query = get_groq_response(question, prompt)
#             if sql_query:
#                 st.code(sql_query, language="sql")
                
#                 with st.spinner("Executing query..."):
#                     results = read_sql_query(sql_query, DB_PATH)
#                     if results:
#                         st.success("Query Results:")
#                         for row in results:
#                             st.write(row)
#                     else:
#                         st.info("No results found")
#     else:
#         st.warning("Please enter a question")