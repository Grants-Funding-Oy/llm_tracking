import os
import csv
import openai
import google.generativeai as genai
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Google Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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

def get_o3_response(messages):
    """
    Get a response from OpenAI o3 model
    """
    try:
        response = openai.chat.completions.create(
            model="o3",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting response from OpenAI o3: {e}")
        return f"Error: {str(e)}"

def get_gemini_response(prompt):
    """
    Get a response from Gemini 2.0 Flash Lite
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return f"Error: {str(e)}"

def analyze_conversation(conversation_df):
    """
    Analyze the conversation using OpenAI o3 to evaluate iLoq's visibility
    """
    # Prepare the conversation data as a formatted string
    conversation_str = ""
    for _, row in conversation_df.iterrows():
        if row['Type'] == 'question':  # Only include question rows in the analysis
            conversation_str += f"Kysymys {row['QuestionNumber']}: {row['Question']}\n"
            conversation_str += f"Vastaus {row['QuestionNumber']} (GPT-4o): {row['GPT4o_Answer']}\n"
            conversation_str += f"Vastaus {row['QuestionNumber']} (Gemini): {row['Gemini_Answer']}\n\n"
    
    # Create the prompt for analysis
    analysis_prompt = [
        {"role": "system", "content": "You are an expert in brand analysis and marketing."},
        {"role": "user", "content": f"""Ohessa on käyttäjän kielimallille esittämät kysymykset ja kielimallin antamat vastaukset. Arvioi miten hyvin iloq näkyy vastauksissa ja miten kielimalli esittää iLoqin. Vertaile myös eroja GPT-4o:n ja Geminin vastausten välillä. Lopuksi ehdota miten näkyvyyttä kielimallien osalta voisi kehittää ja 5 kysymystä, joilla käyttäjä ehkä hakee tietoa aiheesta.

{conversation_str}"""}
    ]
    
    # Get the analysis from o3
    print("Analyzing conversation with OpenAI o3...")
    analysis = get_o3_response(analysis_prompt)
    
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
        'GPT4o_Answer',
        'Gemini_Answer',
        'Timestamp',
        'Type'
    ])
    
    # Generate a conversation ID (timestamp for simplicity)
    conversation_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Define initial question
    initial_question = "Miten vaihdan älylukkoon? Kuka näitä tekee?"
    
    # Initialize conversation history for OpenAI API
    gpt_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": initial_question}
    ]
    
    # Get response to initial question from GPT-4o
    print(f"Asking GPT-4o initial question: {initial_question}")
    initial_gpt_answer = get_gpt4o_response(gpt_messages)
    
    # Get response to initial question from Gemini
    print(f"Asking Gemini initial question: {initial_question}")
    initial_gemini_answer = get_gemini_response(initial_question)
    
    # Add assistant's response to conversation history
    gpt_messages.append({"role": "assistant", "content": initial_gpt_answer})
    
    # Add to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 1,
            'Question': initial_question,
            'GPT4o_Answer': initial_gpt_answer,
            'Gemini_Answer': initial_gemini_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
        }])
    ], ignore_index=True)
    
    # Define follow-up question
    followup_question = "Kerro lisää iLoq-älylukkojen ominaisuuksista ja hinnoista."
    
    # Add follow-up question to conversation history
    gpt_messages.append({"role": "user", "content": followup_question})
    
    # Get response to follow-up question from GPT-4o
    print(f"Asking GPT-4o follow-up question: {followup_question}")
    followup_gpt_answer = get_gpt4o_response(gpt_messages)
    
    # Get response to follow-up question from Gemini
    print(f"Asking Gemini follow-up question: {followup_question}")
    followup_gemini_answer = get_gemini_response(followup_question)
    
    # Add assistant's response to conversation history
    gpt_messages.append({"role": "assistant", "content": followup_gpt_answer})
    
    # Add to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 2,
            'Question': followup_question,
            'GPT4o_Answer': followup_gpt_answer,
            'Gemini_Answer': followup_gemini_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
        }])
    ], ignore_index=True)
    
    # Analyze the conversation for iLoq visibility with o3
    print("\nPerforming iLoq brand visibility analysis with OpenAI o3...")
    analysis = analyze_conversation(conversation_df)
    
    # Add analysis to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 3,
            'Question': "Brändianalyysi: iLoq-brändin näkyvyys vastauksissa",
            'GPT4o_Answer': analysis,
            'Gemini_Answer': "Analyysi tehty OpenAI o3-mallilla",
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
    print(f"GPT-4o Answer 1: {initial_gpt_answer[:100]}...")
    print(f"Gemini Answer 1: {initial_gemini_answer[:100]}...")
    print(f"Question 2: {followup_question}")
    print(f"GPT-4o Answer 2: {followup_gpt_answer[:100]}...")
    print(f"Gemini Answer 2: {followup_gemini_answer[:100]}...")
    
    # Print a snippet of the analysis
    print("\nAnalysis Snippet (by OpenAI o3):")
    print(analysis[:300] + "...")

if __name__ == "__main__":
    main() 