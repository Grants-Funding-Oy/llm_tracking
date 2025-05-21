# Company LLM Analysis

This script analyzes how companies are mentioned in LLM responses, particularly focusing on smart lock companies in this example.

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
1. Ask questions about smart locks to GPT-4o
2. Record the questions and answers in a CSV file named `company_mentions.csv`
3. You can analyze the CSV to see how companies are mentioned in the responses

## Customization

To add more questions, edit the `questions` list in the `main()` function of `company_llm_analysis.py`. 