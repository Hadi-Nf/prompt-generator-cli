import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def load_prompts():
    try:
        with open("prompts.json", "r") as file:
            prompts = json.load(file)
            return prompts
    except FileNotFoundError:
        print("Prompt file not found! making new prompt file.")
        prompts = []
        return prompts
def save_prompts(prompts_list):
    with open("prompts.json", "w") as file:
        json.dump(prompts_list, file, indent= 4)

prompts = load_prompts()
def create_prompt(text):    
    new_id = len(prompts) + 1
    new_prompt = {'id' : new_id, 'text' : text }
    prompts.append(new_prompt)
    print("added new prompt!")
    save_prompts(prompts)

def read_prompt():
    if len(prompts) == 0:
        print("\nYou don't have any prompts saved yet!\n")
        return
    print("Prompts:\n")
    for prompt in prompts:
        print(f"ID = {prompt['id']}, Prompt: {prompt['text']}\n")

def update_prompt(target_id, new_text):
    for prompt in prompts:
        if prompt['id'] == target_id:
            prompt['text'] = new_text
            print(f"the prompt in prompt ID '{prompt['id']}' has been updated to the following:\n {prompt['text']}")
            save_prompts(prompts)
            return
    print(f"Prompt with an ID of '{target_id}' could not be found")
def delete_prompt(target_id):
    for prompt in prompts:
        if prompt['id'] == target_id:
            prompts.remove(prompt)
            print(f"Prompt with ID '{prompt['id']}' and text '{prompt['text']}' has been removed")
            for remaining_prompt in prompts:
                if remaining_prompt['id'] > target_id:
                    remaining_prompt['id'] -= 1
            save_prompts(prompts)
            return
    print(f"Prompt with an ID of '{target_id}' could not be found")
def run_prompt_with_ai(target_id):
    for prompt in prompts:
        if prompt['id'] == target_id:
            prompt_text = prompt['text']
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"
            headers = {'Content-Type': 'application/json'}
            data = {"contents": [{"parts":[{"text": prompt_text}]}]}
            try:
                response = requests.post(url, headers= headers, json=data)
                response.raise_for_status()
                full_response = response.json()
                AI_response = full_response['candidates'][0]['content']['parts'][0]['text']
                print("\n--- AI Response ---")
                print(AI_response)
                print("-------------------\n")
            
            except requests.exceptions.RequestException as e:
                print(f"\n[!] Connection or API Error: {e}\n")
            except (KeyError, IndexError): 
                print("\n[!] Error: The AI returned an unexpected format. It may have been blocked by safety filters.")
                print("Raw response for debugging:", full_response, "\n")
            return
    print(f"Prompt with an ID of '{target_id}' could not be found")

def display_menu():
    print("\n--- Main Menu ---")
    print("1. Input a new prompt")
    print("2. View All of your prompts")
    print("3. Update a previous prompt")
    print("4. Delete a previous prompt")
    print("5. Run a prompt with AI")
    print("6. Quit")
    print("0. Show this menu again")
    print("-----------------\n")

display_menu()

while True:
    while True:
        try:
            user_input = int(input("\nEnter an option from 0 to 6 (0 shows the Menu of options): "))
            if 0 <= user_input <= 6:
                break
            else:
                print("Out of range! Please enter a number between 0 and 6.")
        except ValueError:
            print("Invalid Input. You must enter a number!")
    if user_input == 0:
        display_menu()
    elif user_input == 1:
        prompt_text = input("Please enter your new prompt here:\n")
        create_prompt(prompt_text)
    elif user_input == 2:
        read_prompt()
    elif user_input == 3:
        try:
            updated_prompt_id = int(input("Please input the ID of the prompt you would like to modify: "))
            updated_prompt = input("Please enter the updated version of your prompt:\n")
            update_prompt(updated_prompt_id, updated_prompt)
        except ValueError:
            print("Invalid input! Please enter an integer value belonging to an ID")
    elif user_input == 4:
        try:
            deletion_prompt_id = int(input("Please input the ID of the prompt you would like to delete!: "))
            delete_prompt(deletion_prompt_id)
        except ValueError:
            print("Invalid input! Please enter an integer value belonging to an ID")
    elif user_input == 5:
        try:
            AI_prompt_id = int(input("Please input the ID of the prompt you would like to run by in the AI: "))
            run_prompt_with_ai(AI_prompt_id)
        except ValueError:
            print("Invalid input! Please enter an integer value belonging to an ID")
    elif user_input == 6:
        print("\nExiting Prompt Manager. GoodBye!")
        break
