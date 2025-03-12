import os
import time
import re
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize LLM with reduced max_tokens
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    max_tokens=300,
    google_api_key=api_key
)

# Helper function to safely call the API with error handling for quota exhaustion
def safe_invoke(prompt_str, retry_delay=30):
    try:
        response = llm.invoke(prompt_str)
        return response.content
    except ResourceExhausted as e:
        print("Resource exhausted. Waiting for quota reset...")
        time.sleep(retry_delay)
        return safe_invoke(prompt_str, retry_delay)
    except Exception as e:
        print("Error:", e)
        return "Error"

# 1. Few-Shot Learning - Job Interview Question Classification
few_shot_prompt = PromptTemplate(
    template="""Classify the type of job interview question:

Question: "Can you tell me about a time when you had to resolve a conflict at work?"
Type: Behavioral

Question: "What is the time complexity of a binary search algorithm?"
Type: Technical

Question: "Why do you want to work for our company?"
Type: Motivational

Question: "{question}"
Type:""",
    input_variables=["question"]
)

question_input = {"question": "How would you design a scalable database system?"}
print("3.1, Few-Shot Learning Response:", safe_invoke(few_shot_prompt.format(**question_input)))

# 2. Chain-of-Thought (CoT) Prompting - Debugging a Python script
cot_prompt = PromptTemplate(
    template="""A developer wrote a Python function to calculate the factorial of a number:
```python
def factorial(n):
    if n == 0:
        return 0
    else:
        return n * factorial(n-1)
```
However, the function is not returning the correct output for factorial(0). Identify the mistake and suggest a fix.

Let's think step by step.""",
)

print("3.2, Chain-of-Thought Response: \n", safe_invoke(cot_prompt.format()))

# 3. Self-Consistency (Multiple Runs) - Legal Document Classification
sc_prompt = PromptTemplate(
    template="""Classify the following legal document as CONTRACT, POLICY, or AGREEMENT.

Document: "This document outlines the responsibilities of both parties in the sale of a property, including payment terms, obligations, and legal recourse."

Classification:""",
)

responses = []
for _ in range(2):
    responses.append(safe_invoke(sc_prompt.format()))
    time.sleep(10) # Delay between multiple runs to avoid quota exhaustion
print("3.3, Self-Consistency Responses:", responses)

# 4. Generate Knowledge Prompting - Turing Test
knowledge_prompt = PromptTemplate(
    template="""Generate background knowledge before answering.

Question: What is the Turing test used for?
Background Knowledge:""",
)

knowledge = safe_invoke(knowledge_prompt.format())

final_prompt = PromptTemplate(
    template="""Using the following background knowledge, answer the question.

Background Knowledge: {knowledge}

Question: What is the Turing test used for?
Answer:""",
    input_variables=["knowledge"]
)

print("3.4, Generate Knowledge Response:", safe_invoke(final_prompt.format(knowledge=knowledge)))

# 5. Program-aided Language Model (PAL) - Data Analysis
pal_prompt = PromptTemplate(
    template="""Solve the following problem by generating Python code.

Problem: "Find the average temperature from the list [23, 27, 21, 26, 30, 28]."

Python Code:""",
)

code_response = safe_invoke(pal_prompt.format())
print("3.5, PAL Generated Code: \n", code_response)

# Extract and execute the Python code safely
cleaned_code = re.sub(r"```python|```", "", code_response).strip()
exec_globals = {}
try:
    exec(cleaned_code, {}, exec_globals)
    print("PAL Computation Result:", exec_globals.get("average_temperature", "No result variable found"))
except Exception as e:
    print("Error executing PAL code:", e)
