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

def analyze_conversation(conversation_df):
    """
    Analyze the conversation using GPT-4o to evaluate iLoq's visibility
    """
    # Prepare the conversation data as a formatted string
    conversation_str = ""
    for _, row in conversation_df.iterrows():
        conversation_str += f"Kysymys {row['QuestionNumber']}: {row['Question']}\n"
        conversation_str += f"Vastaus {row['QuestionNumber']}: {row['Answer']}\n\n"
    
    # Create the prompt for analysis
    analysis_prompt = [
        {"role": "system", "content": "You are an expert in brand analysis and marketing."},
        {"role": "user", "content": f"""Ohessa on käyttäjän kielimallille esittämät kysymykset ja kielimallin antamat vastaukset. Arvioi miten hyvin iloq näkyy vastauksissa ja miten kielimalli esittää iLoqin. Lopuksi ehdota miten näkyvyyttä kielimallien osalta voisi kehittää ja 5 kysymystä, joilla käyttäjä ehkä hakee tietoa aiheesta.

{conversation_str}"""}
    ]
    
    # Get the analysis from GPT-4o
    print("Analyzing conversation for iLoq visibility...")
    analysis = get_gpt4o_response(analysis_prompt)
    
    # Save the analysis to a text file
    analysis_file = "iloq_analysis.txt"
    with open(analysis_file, "w", encoding="utf-8") as f:
        f.write(analysis)
    
    print(f"Analysis saved to {analysis_file}")
    return analysis

def main():
    # Initialize conversation DataFrame
    conversation_df = pd.DataFrame(columns=[
        'ConversationID', 
        'QuestionNumber', 
        'Question', 
        'Answer', 
        'Timestamp',
        'Type'
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
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
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
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
        }])
    ], ignore_index=True)
    
    # Analyze the conversation for iLoq visibility
    print("\nPerforming iLoq brand visibility analysis...")
    analysis = analyze_conversation(conversation_df)
    
    # Add analysis to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 3,
            'Question': "Brändianalyysi: iLoq-brändin näkyvyys vastauksissa",
            'Answer': analysis,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'analysis'
        }])
    ], ignore_index=True)
    
    # Save to CSV
    output_file = "company_mentions.csv"
    conversation_df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Conversation and analysis saved to {output_file}")
    
    # Print summary
    print("\nConversation Summary:")
    print(f"Question 1: {initial_question}")
    print(f"Answer 1: {initial_answer[:100]}...")
    print(f"Question 2: {followup_question}")
    print(f"Answer 2: {followup_answer[:100]}...")
    
    # Print a snippet of the analysis
    print("\nAnalysis Snippet:")
    print(analysis[:300] + "...")

if __name__ == "__main__":
    main() 