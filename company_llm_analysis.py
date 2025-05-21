# -*- coding: utf-8 -*-  
import os
import csv
import openai
import google.generativeai as genai
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool

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

def get_agent_with_websearch_response(query):
    """
    Get a response from OpenAI GPT-4o agent with web search capability
    """
    try:
        agent = Agent(
            name="SearchAgent",
            model="gpt-4o",
            instructions="Olet avulias asiantuntija, jolla on pääsy verkkohakuun. Käytä verkkohakua etsiäksesi ajantasaista tietoa vastataksesi kysymyksiin. Erityisesti kun kysytään julkisesta rahoituksesta tai konsultointipalveluista, tarkista faktat verkosta.",
            tools=[WebSearchTool()]
        )
        
        result = Runner.run_sync(agent, query)
        return result.final_output
    except Exception as e:
        print(f"Error getting response from Agent with web search: {e}")
        return f"Error: {str(e)}"

def analyze_conversation(conversation_df):
    """
    Analyze the conversation using OpenAI o3 to evaluate Grants visibility
    """
    # Prepare the conversation data as a formatted string
    conversation_str = ""
    for _, row in conversation_df.iterrows():
        if row['Type'] == 'question':  # Only include question rows in the analysis
            conversation_str += f"Kysymys {row['QuestionNumber']}: {row['Question']}\n"
            conversation_str += f"Vastaus {row['QuestionNumber']} (GPT-4o): {row['GPT4o_Answer'][:500]}...\n"
            conversation_str += f"Vastaus {row['QuestionNumber']} (Gemini): {row['Gemini_Answer'][:500]}...\n"
            conversation_str += f"Vastaus {row['QuestionNumber']} (Agent + WebSearch): {row['Agent_Answer'][:500]}...\n\n"
    
    # Create the prompt for analysis
    analysis_prompt = [
        {"role": "system", "content": "You are an expert in brand analysis and marketing."},
        {"role": "user", "content": f"""Ohessa on käyttäjän kielimallille esittämät kysymykset ja kielimallin antamat vastaukset. Arvioi miten hyvin Grants näkyy vastauksissa ja miten kielimallit esittävät Grantsin suhteessa kilpailijoihin. 

Vertaile erityisesti kolmen eri vastaajamallin eroja:
1. GPT-4o (ei web-hakua)
2. Gemini (ei web-hakua) 
3. Agent + WebSearch (pääsy ajantasaiseen verkkotietoon)

Analysoi miten Grantsin näkyvyys eroaa perustuen siihen, onko mallilla pääsy verkkoon vai ei. Lopuksi ehdota miten näkyvyyttä kielimallien osalta voisi kehittää (huomioi tekniset ja sisällölliset asiat).

{conversation_str}"""}
    ]
    
    # Get the analysis from o3
    print("Analyzing conversation with OpenAI o3...")
    analysis = get_o3_response(analysis_prompt)
    
    # Save the analysis to a text file
    analysis_file = "grants_analysis.txt"
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
        'Agent_Answer',
        'Timestamp',
        'Type'
    ])
    
    # Generate a conversation ID (timestamp for simplicity)
    conversation_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Define initial question (neutral, doesn't mention Grants)
    initial_question = "Miten voin hakea julkista rahoitusta yritykselleni? Kuka tarjoaa konsultointia tähän?"
    
    # Initialize conversation history for OpenAI API
    gpt_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": initial_question}
    ]
    
    # Get responses to initial questions
    print(f"Asking GPT-4o initial question: {initial_question}")
    initial_gpt_answer = get_gpt4o_response(gpt_messages)
    
    print(f"Asking Gemini initial question: {initial_question}")
    initial_gemini_answer = get_gemini_response(initial_question)
    
    print(f"Asking Agent with WebSearch initial question: {initial_question}")
    initial_agent_answer = get_agent_with_websearch_response(initial_question)
    
    # Add assistant's responses to conversation histories
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
            'Agent_Answer': initial_agent_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
        }])
    ], ignore_index=True)
    
    # Define follow-up question (neutral, doesn't mention Grants)
    followup_question = "Kerro lisää julkisen rahoituksen konsultointipalveluiden ominaisuuksista ja hinnoista?"
    
    # Add follow-up questions to conversation histories
    gpt_messages.append({"role": "user", "content": followup_question})
    
    # Get responses to follow-up questions
    print(f"Asking GPT-4o follow-up question: {followup_question}")
    followup_gpt_answer = get_gpt4o_response(gpt_messages)
    
    print(f"Asking Gemini follow-up question: {followup_question}")
    followup_gemini_answer = get_gemini_response(followup_question)
    
    print(f"Asking Agent with WebSearch follow-up question: {followup_question}")
    followup_agent_answer = get_agent_with_websearch_response(followup_question)
    
    # Add assistant's responses to conversation histories
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
            'Agent_Answer': followup_agent_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
        }])
    ], ignore_index=True)
    
    # Define third question (neutral, doesn't mention Grants)
    third_question = "Vertaile eri julkisen rahoituksen konsultointipalveluita ja ehdota paras"
    
    # Add third questions to conversation histories
    gpt_messages.append({"role": "user", "content": third_question})
    
    # Get responses to third questions
    print(f"Asking GPT-4o third question: {third_question}")
    third_gpt_answer = get_gpt4o_response(gpt_messages)
    
    print(f"Asking Gemini third question: {third_question}")
    third_gemini_answer = get_gemini_response(third_question)
    
    print(f"Asking Agent with WebSearch third question: {third_question}")
    third_agent_answer = get_agent_with_websearch_response(third_question)
    
    # Add assistant's responses to conversation histories
    gpt_messages.append({"role": "assistant", "content": third_gpt_answer})
    
    # Add to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 3,
            'Question': third_question,
            'GPT4o_Answer': third_gpt_answer,
            'Gemini_Answer': third_gemini_answer,
            'Agent_Answer': third_agent_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
        }])
    ], ignore_index=True)
    
    # Define fourth question (asked without conversation history)
    fourth_question = "Millä yrityksillä on Suomen paras osaaminen julkisesta rahoituksesta, sen hakemisesta ja rahoitusinstrumenteista?"
    
    # Create a new conversation context without history for the fourth question
    fresh_gpt_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": fourth_question}
    ]
    
    # Get responses to fourth question (without history)
    print(f"Asking GPT-4o fourth question (without history): {fourth_question}")
    fourth_gpt_answer = get_gpt4o_response(fresh_gpt_messages)
    
    print(f"Asking Gemini fourth question: {fourth_question}")
    fourth_gemini_answer = get_gemini_response(fourth_question)
    
    print(f"Asking Agent with WebSearch fourth question: {fourth_question}")
    fourth_agent_answer = get_agent_with_websearch_response(fourth_question)
    
    # Add to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 4,
            'Question': fourth_question,
            'GPT4o_Answer': fourth_gpt_answer,
            'Gemini_Answer': fourth_gemini_answer,
            'Agent_Answer': fourth_agent_answer,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Type': 'question'
        }])
    ], ignore_index=True)
    
    # Analyze the conversation for Grants visibility with o3
    print("\nPerforming Grants brand visibility analysis with OpenAI o3...")
    analysis = analyze_conversation(conversation_df)
    
    # Add analysis to DataFrame
    conversation_df = pd.concat([
        conversation_df,
        pd.DataFrame([{
            'ConversationID': conversation_id,
            'QuestionNumber': 5,
            'Question': "Brändianalyysi: Grants-brändin näkyvyys vastauksissa",
            'GPT4o_Answer': analysis,
            'Gemini_Answer': "Analyysi tehty OpenAI o3-mallilla",
            'Agent_Answer': "Analyysi tehty OpenAI o3-mallilla",
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
    print(f"Agent+WebSearch Answer 1: {initial_agent_answer[:100]}...")
    
    print(f"Question 2: {followup_question}")
    print(f"GPT-4o Answer 2: {followup_gpt_answer[:100]}...")
    print(f"Gemini Answer 2: {followup_gemini_answer[:100]}...")
    print(f"Agent+WebSearch Answer 2: {followup_agent_answer[:100]}...")
    
    print(f"Question 3: {third_question}")
    print(f"GPT-4o Answer 3: {third_gpt_answer[:100]}...")
    print(f"Gemini Answer 3: {third_gemini_answer[:100]}...")
    print(f"Agent+WebSearch Answer 3: {third_agent_answer[:100]}...")
    
    print(f"Question 4 (without history): {fourth_question}")
    print(f"GPT-4o Answer 4: {fourth_gpt_answer[:100]}...")
    print(f"Gemini Answer 4: {fourth_gemini_answer[:100]}...")
    print(f"Agent+WebSearch Answer 4: {fourth_agent_answer[:100]}...")
    
    # Print a snippet of the analysis
    print("\nAnalysis Snippet (by OpenAI o3):")
    print(analysis[:300] + "...")

if __name__ == "__main__":
    main() 
