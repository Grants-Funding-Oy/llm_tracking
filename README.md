# Company LLM Analysis

This script analyzes how companies are mentioned in LLM responses, particularly focusing on smart lock companies in this example.

## Features

- Sends questions to GPT-4o about smart locks in Finnish
- Maintains conversation context between questions
- Follows up with specific questions about iLoq smart locks
- Records complete conversations with timestamps in CSV format
- Uses pandas DataFrame for flexible data handling and analysis
- **NEW**: Automatically analyzes brand visibility in LLM responses

## Setup

1. Make sure you have Python installed
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the same directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the script:
```
python company_llm_analysis.py
```

The script will:
1. Ask an initial question about smart locks to GPT-4o
2. Ask a follow-up question about iLoq smart locks
3. Maintain conversation context between questions
4. Record the complete conversation in a CSV file named `company_mentions.csv`
5. **NEW**: Analyze the collected responses to evaluate how iLoq is presented
6. **NEW**: Generate suggestions for improving brand visibility
7. **NEW**: Save the analysis to a file named `iloq_analysis.txt`
8. Display a summary of the conversation and analysis in the console

## CSV Structure

The output CSV file contains the following columns:
- `ConversationID`: Unique identifier for the conversation
- `QuestionNumber`: Sequential number of the question in the conversation
- `Question`: The question asked
- `Answer`: GPT-4o's response
- `Timestamp`: When the exchange occurred

## Analysis Content

The brand visibility analysis evaluates:
- How well iLoq appears in the language model's responses
- How the language model presents iLoq's products and brand
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