import os
import csv
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt4o_response(question):
    """
    Get a response from GPT-4o for the given question
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return f"Error: {str(e)}"

def main():
    # The question about smart locks in Finnish
    questions = [
        "Miten vaihdan älylukkoon? Kuka näitä tekee?"
    ]
    
    # Output file
    output_file = "company_mentions.csv"
    
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.isfile(output_file)
    
    with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Question', 'Answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write headers if file doesn't exist
        if not file_exists:
            writer.writeheader()
        
        # Process each question
        for question in questions:
            print(f"Processing question: {question}")
            answer = get_gpt4o_response(question)
            
            # Write to CSV
            writer.writerow({
                'Question': question,
                'Answer': answer
            })
            
            print(f"Answer written to {output_file}")

if __name__ == "__main__":
    main() 