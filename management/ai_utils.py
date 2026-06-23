import os
import google.generativeai as genai
from django.conf import settings

# Configure the API key using the environment variable
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# We use the recommended gemini-1.5-flash for general fast text generation
def get_model():
    # Only return the model if API key is configured, else return None
    if not os.getenv("GEMINI_API_KEY"):
        return None
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_worksheet(topic, level, questions_count):
    model = get_model()
    if not model:
        return "Error: GEMINI_API_KEY is not configured in the .env file."
        
    prompt = f"""
    Act as an expert English language teacher.
    Create an English worksheet for students at the {level} level.
    The topic of the worksheet is: {topic}.
    Please generate exactly {questions_count} questions.
    
    Format the output in clear Markdown. 
    Include two sections:
    1. **Worksheet** (the questions with spaces for answers if appropriate)
    2. **Answer Key** (the correct answers)
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the worksheet: {str(e)}"

def generate_lesson_plan(topic, level, duration):
    model = get_model()
    if not model:
        return "Error: GEMINI_API_KEY is not configured in the .env file."
        
    prompt = f"""
    Act as an expert English language teacher and curriculum designer.
    Create a detailed lesson plan.
    Topic: {topic}
    Level: {level}
    Class Duration: {duration} minutes
    
    Format the output in clear Markdown.
    Include the following sections:
    - **Objectives**
    - **Warm-up**
    - **Presentation** (teaching the new concept)
    - **Practice** (controlled practice)
    - **Production** (freer practice)
    - **Cool-down / Wrap-up**
    
    Allocate specific time estimates (in minutes) to each section so it totals {duration} minutes.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the lesson plan: {str(e)}"

def generate_test(test_type, topics, level):
    model = get_model()
    if not model:
        return "Error: GEMINI_API_KEY is not configured in the .env file."
        
    prompt = f"""
    Act as an expert English language assessor.
    Create a {test_type} for English students.
    The students are at the {level} level.
    The test should cover the following topics: {topics}.
    
    Format the output in clear Markdown.
    Include a variety of question types (e.g., multiple choice, fill in the blanks, short answer).
    
    Include two sections:
    1. **The Test** (student-facing)
    2. **Marking Scheme / Answer Key** (teacher-facing, including how many points each question is worth)
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the test: {str(e)}"
