import os
import csv
import openai
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt4o_response(messages):
    """
    Get a response from GPT-4o based on the conversation history
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return f"Error: {str(e)}"

def main():
    # Initialize conversation DataFrame
    conversation_df = pd.DataFrame(columns=[
        'ConversationID', 
        'QuestionNumber', 
        'Question', 
        'Answer', 
        'Timestamp'
    ])
    
    # Generate a conversation ID (timestamp for simplicity)
    conversation_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Define initial question
    initial_question = "Miten vaihdan älylukkoon? Kuka näitä tekee?"
    
    # Initialize conversation history for OpenAI API
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": initial_question}
    ]
    
    # Get response to initial question
    print(f"Asking initial question: {initial_question}")
    initial_answer = get_gpt4o_response(messages)
    
    # Add assistant's response to conversation history
    messages.append({"role": "assistant", "content": initial_answer})
    
    # Add to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 1,
            'Question': initial_question,
            'Answer': initial_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
    ], ignore_index=True)
    
    # Define follow-up question
    followup_question = "Kerro lisää iLoq-älylukkojen ominaisuuksista ja hinnoista."
    
    # Add follow-up question to conversation history
    messages.append({"role": "user", "content": followup_question})
    
    # Get response to follow-up question
    print(f"Asking follow-up question: {followup_question}")
    followup_answer = get_gpt4o_response(messages)
    
    # Add assistant's response to conversation history
    messages.append({"role": "assistant", "content": followup_answer})
    
    # Add to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 2,
            'Question': followup_question,
            'Answer': followup_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
    ], ignore_index=True)
    
    # Save to CSV
    output_file = "company_mentions.csv"
    conversation_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Conversation saved to {output_file}")
    
    # Print summary
    print("\nConversation Summary:")
    print(f"Question 1: {initial_question}")
    print(f"Answer 1: {initial_answer[:100]}...")
    print(f"Question 2: {followup_question}")
    print(f"Answer 2: {followup_answer[:100]}...")

if __name__ == "__main__":
    main() 