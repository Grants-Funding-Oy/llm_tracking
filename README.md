# Company LLM Analysis

This script analyzes how companies are mentioned in LLM responses, particularly focusing on smart lock companies in this example.

## Features

- Sends questions to both GPT-4o and Gemini 2.0 Flash Lite for comparison
- Maintains conversation context between questions
- Follows up with specific questions about iLoq smart locks
- Records complete conversations with timestamps in CSV format
- Uses pandas DataFrame for flexible data handling and analysis
- Automatically analyzes brand visibility in LLM responses
- Compares how different LLMs (OpenAI vs Google) present company information

## Setup

1. Make sure you have Python installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the same directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

Run the script:
```
python company_llm_analysis.py
```

The script will:
1. Ask the same initial question about smart locks to both GPT-4o and Gemini
2. Ask the same follow-up question about iLoq smart locks to both models
3. Maintain conversation context between questions for GPT-4o
4. Record the complete conversation in a CSV file named `company_mentions.csv`
5. Analyze the collected responses to evaluate how iLoq is presented in both models
6. Compare the differences between GPT-4o and Gemini in representing iLoq
7. Generate suggestions for improving brand visibility
8. Save the analysis to both the CSV file and a separate `iloq_analysis.txt` file
9. Display a summary of the conversation and analysis in the console

## CSV Structure

The output CSV file contains the following columns:
- `ConversationID`: Unique identifier for the conversation
- `QuestionNumber`: Sequential number of the question in the conversation
- `Question`: The question asked
- `GPT4o_Answer`: GPT-4o's response
- `Gemini_Answer`: Gemini 2.0 Flash Lite's response
- `Timestamp`: When the exchange occurred
- `Type`: Indicates whether the row contains a 'question' or 'analysis'

## Analysis Content

The brand visibility analysis evaluates:
- How well iLoq appears in both language models' responses
- How each model presents iLoq's products and brand
- The differences between how OpenAI and Google models represent the company
- Recommendations for improving brand visibility in language models
- 5 potential questions that users might ask about smart locks

## Customization

To modify the conversation:
- Change the `initial_question` variable for a different starting point
- Modify the `followup_question` variable to ask different follow-up questions
- Add more questions by following the pattern in the code
- Adjust the analysis prompt in the `analyze_conversation` function

## Documentation

For more details about the implementation and future development plans, see `conversation_framework.md`.