# Prompt-Engineering with Google Gemini API

This is a repo for training task on Prompt Engineering given to me at iCog-Labs. This project demonstrates advanced prompt engineering techniques using LangChain and the Google Gemini API. The code leverages five different prompting methods to show how you can build creative AI applications using various real-world use cases.

## Features

1. **_Few-Shot Learning_**  
   **Usecase used:** Classify the type of job interview question as Behavioral, Technical, Motivational.

2. **_Chain-of-Thought (CoT) Prompting_**  
   **Usecase used:** Debugs a Python function (calculating factorial) step by step by prompting the model to reason through the error.

3. **_Self-Consistency_**  
   **Usecase used:** Runs multiple passes to classify a legal document and check for consistency in results.

4. **_Generate Knowledge Prompting_**  
   **Usecase used:** Generates background knowledge before answering a question—in this case, explaining what the Turing test is used for.

5. **Program-aided Language Model (PAL)**
   **Usecase used:** Generates Python code to perform a data analysis task (calculating the average temperature) and then executes the code after cleaning any Markdown formatting.

### Note

    Since I was facing a 429:ResourceExhausted error, I included a helper function `safe_invoke` which catches quota errors (ResourceExhausted) and waits for 30 seconds before retrying.

## Setup Instructions

1. **Clone the Repository**  
   Clone this repository to your local machine.

   ```bash
    git clone https://github.com/Musiemhy/Prompt-Engineering.git
   ```

2. **Install Dependencies**
   Install the required packages using:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   Create a .env file in the project root with the following content:

   ```bash
   GOOGLE_API_KEY=your-google-api-key-here
   ```

4. **Run the Application**
   Execute the script with:

   ```bash
   python app.py
   ```
