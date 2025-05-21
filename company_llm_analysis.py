# -*- coding: utf-8 -*-  
import os
import csv
import openai
import google.generativeai as genai
import pandas as pd
import json
from datetime import datetime
from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Google Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gpt4o_response(messages, verbose=True):
    """
    Get a response from GPT-4o based on the conversation history
    """
    try:
        if verbose:
            print("\n" + "="*80)
            print("GPT-4O KYSELY:")
            last_message = messages[-1]['content'] if messages else "Ei viestiä"
            print(f"{last_message}")
            print("="*80)
            
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        content = response.choices[0].message.content
        
        if verbose:
            print("\n" + "-"*80)
            print("GPT-4O VASTAUS:")
            print("-"*80)
            print(content[:1000] + "..." if len(content) > 1000 else content)
            print("-"*80 + "\n")
            
        return content
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return f"Error: {str(e)}"

def get_o3_response(messages, verbose=True):
    """
    Get a response from OpenAI o3 model
    """
    try:
        if verbose:
            print("\n" + "="*80)
            print("O3 ANALYYSI KYSELY:")
            last_message = messages[-1]['content'] if messages else "Ei viestiä"
            print(f"{last_message[:500]}...")
            print("="*80)
            
        response = openai.chat.completions.create(
            model="o3",
            messages=messages
        )
        
        content = response.choices[0].message.content
        
        if verbose:
            print("\n" + "-"*80)
            print("O3 ANALYYSI VASTAUS:")
            print("-"*80)
            print(content[:1000] + "..." if len(content) > 1000 else content)
            print("-"*80 + "\n")
            
        return content
    except Exception as e:
        print(f"Error getting response from OpenAI o3: {e}")
        return f"Error: {str(e)}"

def get_gemini_response(prompt, verbose=True):
    """
    Get a response from Gemini 2.0 Flash Lite
    """
    try:
        if verbose:
            print("\n" + "="*80)
            print("GEMINI KYSELY:")
            print(f"{prompt}")
            print("="*80)
            
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(prompt)
        
        content = response.text
        
        if verbose:
            print("\n" + "-"*80)
            print("GEMINI VASTAUS:")
            print("-"*80)
            print(content[:1000] + "..." if len(content) > 1000 else content)
            print("-"*80 + "\n")
            
        return content
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        return f"Error: {str(e)}"

class WebSearchTracker:
    """Helper class to track web search calls"""
    def __init__(self):
        self.searches = []
        
    def add_search(self, query, results):
        self.searches.append({"query": query, "results": results})
        
    def get_last_search(self):
        return self.searches[-1] if self.searches else None
        
    def get_all_searches(self):
        return self.searches

# Global tracker for web searches
web_search_tracker = WebSearchTracker()

def get_agent_with_websearch_response(query, verbose=True):
    """
    Get a response from OpenAI GPT-4o agent with web search capability
    """
    try:
        # Create a callback to track tool usage
        def tool_callback(run_id, tool_call, chunk=None):
            if tool_call.tool_name == "web_search":
                # This is a web search call
                if verbose:
                    print(f"\n🔍 WEB SEARCH: {tool_call.tool_input}")
                    if chunk:
                        print(f"🌐 HAKUTULOS: {chunk}")

        if verbose:
            print("\n" + "="*80)
            print("AGENTTI + WEB SEARCH KYSELY:")
            print(f"{query}")
            print("="*80)
        
        # Create the agent
        agent = Agent(
            name="SearchAgent",
            model="gpt-4o",
            instructions="Olet avulias asiantuntija, jolla on pääsy verkkohakuun. Käytä verkkohakua etsiäksesi ajantasaista tietoa vastataksesi kysymyksiin. Erityisesti kun kysytään julkisesta rahoituksesta tai konsultointipalveluista, tarkista faktat verkosta.",
            tools=[WebSearchTool()]
        )
        
        # Run the agent
        try:
            # Attempt to run with trace
            result = Runner.run_sync(
                agent, 
                query,
                tool_callback=tool_callback
            )
        except TypeError:
            # Fallback if tool_callback parameter not supported
            print("Callback parametri ei ole tuettu - ajetaan ilman seurantaa")
            result = Runner.run_sync(agent, query)
        
        final_output = result.final_output
        
        if verbose:
            print("\n" + "-"*80)
            print("AGENTTI + WEB SEARCH VASTAUS:")
            print("-"*80)
            print(final_output[:1000] + "..." if len(final_output) > 1000 else final_output)
            print("-"*80 + "\n")
            
            # Try to extract tool usage information from the result
            try:
                # Access trace if available
                if hasattr(result, 'trace') and result.trace:
                    print("\n🛠️ AGENTIN TYÖKALUJEN KÄYTTÖ:")
                    for step in result.trace:
                        if 'tool_calls' in step:
                            for tool_call in step['tool_calls']:
                                if tool_call.get('name') == 'web_search':
                                    print(f"🔍 WEB SEARCH: {tool_call.get('input')}")
                                    print(f"🌐 TULOS: {tool_call.get('output')[:200]}...")
                                    
                                    # Add to our tracker
                                    web_search_tracker.add_search(
                                        tool_call.get('input'), 
                                        tool_call.get('output')
                                    )
            except Exception as extract_error:
                print(f"Huomautus: Työkalujen käytön tarkempi seuranta ei onnistunut: {extract_error}")
                
            # If we don't find explicit tool usage, try to infer from the answer
            if not web_search_tracker.get_all_searches():
                if "hakutulos" in final_output.lower() or "lähde:" in final_output.lower():
                    print("\n🔍 Agentti näyttää käyttäneen web-hakua (pääteltynä vastauksesta)")
        
        return final_output
    except Exception as e:
        print(f"Error getting response from Agent with web search: {e}")
        return f"Error: {str(e)}"

def analyze_conversation(conversation_df, verbose=True):
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
    print("\nAnalyzing conversation with OpenAI o3...")
    analysis = get_o3_response(analysis_prompt, verbose=verbose)
    
    # Save the analysis to a text file
    analysis_file = "grants_analysis.txt"
    with open(analysis_file, "w", encoding="utf-8") as f:
        f.write(analysis)
    
    # Save web search information to a JSON file
    searches = web_search_tracker.get_all_searches()
    if searches:
        websearch_file = "websearch_data.json"
        with open(websearch_file, "w", encoding="utf-8") as f:
            json.dump(searches, f, ensure_ascii=False, indent=2)
        print(f"Web search data saved to {websearch_file}")
    
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
    
    # Print header with style
    print("\n" + "*"*100)
    print("*" + " "*38 + "GRANTS LLM ANALYYSI" + " "*38 + "*")
    print("*" + " "*98 + "*")
    print("*  Tässä analyysissä vertaillaan kolmea eri mallia:                                        *")
    print("*  1. GPT-4o (ei web-hakua)                                                               *")
    print("*  2. Gemini (ei web-hakua)                                                               *")
    print("*  3. Agent + WebSearch (pääsy verkkoon)                                                  *")
    print("*" + " "*98 + "*")
    print("*  Seuraa terminaalista, käyttääkö agentti web-hakua vastatessaan kysymyksiin             *")
    print("*" + " "*98 + "*")
    print("*"*100 + "\n")
    
    # Define initial question (neutral, doesn't mention Grants)
    initial_question = "Miten voin hakea julkista rahoitusta yritykselleni? Kuka tarjoaa konsultointia tähän?"
    
    # Initialize conversation history for OpenAI API
    gpt_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": initial_question}
    ]
    
    # Get responses to initial questions
    print(f"\n🔵 KYSYMYS 1: {initial_question}")
    
    initial_gpt_answer = get_gpt4o_response(gpt_messages)
    initial_gemini_answer = get_gemini_response(initial_question)
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
    print(f"\n🔵 KYSYMYS 2: {followup_question}")
    
    followup_gpt_answer = get_gpt4o_response(gpt_messages)
    followup_gemini_answer = get_gemini_response(followup_question)
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
    print(f"\n🔵 KYSYMYS 3: {third_question}")
    
    third_gpt_answer = get_gpt4o_response(gpt_messages)
    third_gemini_answer = get_gemini_response(third_question)
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
    print(f"\n🔵 KYSYMYS 4 (ilman keskusteluhistoriaa): {fourth_question}")
    
    fourth_gpt_answer = get_gpt4o_response(fresh_gpt_messages)
    fourth_gemini_answer = get_gemini_response(fourth_question)
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
    print("\n🔍 ANALYYSI: Grants-brändin näkyvyys vastauksissa")
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
    
    # Print summary of web search usage
    all_searches = web_search_tracker.get_all_searches()
    if all_searches:
        print("\n" + "="*80)
        print(f"WEB SEARCH YHTEENVETO: Hakuja tehty yhteensä {len(all_searches)}")
        print("="*80)
        for i, search in enumerate(all_searches, 1):
            print(f"Haku {i}: {search['query']}")
        print("="*80)
    else:
        print("\nAgentti ei käyttänyt web-hakua vastatessaan kysymyksiin.")
    
    # Print closing message
    print("\n" + "*"*100)
    print("*" + " "*38 + "ANALYYSI VALMIS" + " "*39 + "*")
    print("*" + " "*98 + "*")
    print("*  Tiedostot:                                                                              *")
    print(f"*  - {output_file:<92}*")
    print(f"*  - grants_analysis.txt{' '*77}*")
    if all_searches:
        print(f"*  - websearch_data.json{' '*76}*")
    print("*"*100 + "\n")

if __name__ == "__main__":
    main() 
