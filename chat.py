import streamlit as st
import google.generativeai as genai  # Using Gemini API
import mysql.connector
import json
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "info",
    "auth_plugin": "mysql_native_password"
}

def store_candidate_data(full_name, email, phone, experience, position, location, tech_stack):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO candidates (full_name, email, phone, experience, position, location, tech_stack)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (full_name, email, phone, experience, position, location, tech_stack)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Database error: {e}")

def generate_questions(tech_stack):
    prompt = f"Generate 3-5 technical interview questions for a candidate skilled in {', '.join(tech_stack)}. Return each question on a new line."
    model = genai.GenerativeModel(MODEL_NAME)
    try:
        response = model.generate_content(prompt)
        questions = [line.strip() for line in response.text.split('\n') if line.strip()]
        return questions
    except Exception as e:
        st.error(f"An error occurred while generating questions: {e}")
        return []

def main():
    st.title("TalentScout Hiring Assistant Chatbot")
    st.write("Welcome! I will help you with the initial screening process.")
    
    # Collect candidate details
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
    position = st.text_input("Desired Position(s)")
    location = st.text_input("Current Location")
    tech_stack = st.text_area("Enter your tech stack (comma-separated)")
    
    if st.button("Generate Questions"):
        if full_name and email and phone and tech_stack:
            store_candidate_data(full_name, email, phone, experience, position, location, tech_stack)
            tech_list = [tech.strip() for tech in tech_stack.split(',')]
            questions = generate_questions(tech_list)
            if questions:
                st.write("### Here are your technical questions:")
                for i, question in enumerate(questions, 1):
                    st.write(f"{i}. {question}")
                st.write("Thank you for your time! Our team will review your responses and contact you shortly.")
        else:
            st.warning("Please fill in all required fields.")

if __name__ == "__main__":
    main()



























