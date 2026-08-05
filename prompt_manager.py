import json

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
            save_prompts(prompts)
            return
    print(f"Prompt with an ID of '{target_id}' could not be found")