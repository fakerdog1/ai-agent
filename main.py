import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, available_functions

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

if len(sys.argv) < 2:
    print("You need to provide a single prompt eclosed in single or double quotes for the AI")
    sys.exit(1)

def get_api_key():
    load_dotenv()
    return os.environ.get("GEMINI_API_KEY")

def init_client():
    api_key = get_api_key()
    return genai.Client(api_key=api_key)

def get_user_args():
    user_prompt = sys.argv[1]
    optional_arguments = sys.argv[2:]
    return user_prompt, optional_arguments

def print_verbose(optional_arguments = []):
    print_verbose = False
    if (len(optional_arguments) <= 0):
        return print_verbose
    
    for argument in optional_arguments:
        match (argument):
            case "--verbose":
                print_verbose = True

    return print_verbose
                

user_prompt, optional_arguments = get_user_args()

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = init_client()
res = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

text = res.text
f_calls = res.function_calls
if f_calls:
    for call in f_calls:
        print(f"Calling function: {call.name}({call.args})")
print(text)

if print_verbose(optional_arguments):
    prompt_tokens = res.usage_metadata.prompt_token_count
    res_tokens = res.usage_metadata.candidates_token_count
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {res_tokens}")

def main():
    pass

if __name__ == "__main__":
    main()
