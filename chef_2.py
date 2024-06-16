import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_ai_response(messages):
    model = "gpt-4o"
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message['content']

def chef_response(messages, request_type, user_input):
    if request_type == "recipe":
        user_message = {
            "role": "user",
            "content": f"Give me a detailed recipe for {user_input}"
        }
    elif request_type == "ingredients":
        user_message = {
            "role": "user",
            "content": f"Suggest a dish based on these ingredients: {user_input}"
        }
    elif request_type == "criticize":
        user_message = {
            "role": "user",
            "content": f"Criticize this recipe: {user_input}"
        }
    elif request_type == "ask something":
        user_message = {
            "role": "user",
            "content": f"Answer questions about previous responses: {user_input}"
        }
    else:
        return "I can only help with suggesting dishes based on ingredients, giving recipes, or criticizing recipes. Please try again with one of these requests."

    messages.append(user_message)
    response_content = get_ai_response(messages)
    messages.append({
        "role": "assistant",
        "content": response_content
    })
    return response_content

if __name__ == "__main__":
    personality = "Wise and experienced Italian chef that loves to make pasta"
    messages = [
        {
            "role": "system",
            "content": personality,
        },
        {
            "role": "system",
            "content": "You should respond to four different inputs: suggesting dishes based on ingredients, giving recipes to dishes, criticizing the recipes given by the user input or asking more questions about previous responses. If the user input does not match any of these scenarios, deny the request and ask to try again."
        }
    ]

    print("Choose the type of request:")
    print("1. Recipe")
    print("2. Suggest a dish based on ingredients")
    print("3. Criticize a recipe")
    request_type_choice = input("\033[1;34mEnter the number of your choice:\033[0m ")

    request_type_mapping = {
        "1": "recipe",
        "2": "ingredients",
        "3": "criticize",
        "4": "ask something"
    }

    request_type = request_type_mapping.get(request_type_choice)
    if not request_type:
        print("\033[1;31mInvalid choice. Please try again and choose a valid option.\033[0m")
    else:
        user_input = input("\033[1;34mEnter details for your request:\033[0m ")
        response = chef_response(messages, request_type, user_input)
        print(f"\033[1;32m{response}\033[0m")

        while True:
            print("\nWould you like to continue the conversation?")
            print("Choose the type of request:")
            print("1. Recipe")
            print("2. Suggest a dish based on ingredients")
            print("3. Criticize a recipe")
            print("4. Ask me something")
            print("5. Exit")
            request_type_choice = input("\033[1;34mEnter the number of your choice:\033[0m ")

            if request_type_choice == "5":
                break

            request_type = request_type_mapping.get(request_type_choice)
            if not request_type:
                print("\033[1;31mInvalid choice. Please run the script again and choose a valid option.\033[0m")
                continue

            user_input = input("\033[1;34mEnter details for your request:\033[0m ")
            response = chef_response(messages, request_type, user_input)
            print(f"\033[1;32m{response}\033[0m")
