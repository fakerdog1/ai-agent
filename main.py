import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_files_contents import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_file, run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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

def call_function(function_call, verbose=False):
    try:
        func = function_call.name
        arguments = function_call.args
        arguments['working_directory'] = './calculator'

        if (verbose):
            print(f"Calling function: {function_call.name}({function_call.args})")
        else:
            print(f" - Calling function: {function_call.name}")

        mappedFuncs = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "write_file": write_file,
            "run_python_file": run_python_file,
        }

        result = mappedFuncs[func](**arguments)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func,
                    response={"result": result},
                )
            ],
        )

    except:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func,
                    response={"error": f"Unknown function: {func}"},
                )
            ],
        )

        

user_prompt, optional_arguments = get_user_args()

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = init_client()
res = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[
            available_functions
        ], system_instruction=system_prompt
    ),
)

f_calls = res.function_calls
if f_calls:
    for call in f_calls:
        called = call_function(call, print_verbose)
        try: 
            function_call_result = called.parts[0].function_response.response
            if print_verbose:
                print(f"-> {function_call_result}")
        except:
            raise Exception("No response from the function")

def main():
    print("Hello world")

if __name__ == "__main__":
    main()
