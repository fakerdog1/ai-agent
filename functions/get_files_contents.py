import os
from functions.get_files_info import get_abs_path, path_contains, join_paths
import config
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file's content up to 10000 characters, constrained to the working directory, file must exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be read, relative to the working directory. If not provided, returns and error for non-existing file.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_abs_path = get_abs_path(working_directory)
        joined_path = join_paths(working_abs_path, file_path)
        abs_path = get_abs_path(joined_path)

        if not path_contains(abs_path, working_abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_path, "r") as f:
            file_content_string = f.read()
            
            if len(file_content_string) > config.MAX_CHARS:
                file_content_string = file_content_string[:config.MAX_CHARS]
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    except Exception as e:
        return f"Error: {e}"