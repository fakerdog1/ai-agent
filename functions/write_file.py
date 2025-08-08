import os
from functions.get_files_info import get_abs_path, path_contains, join_paths, path_exists
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content in a file, constrained to the working directory. If the file doesn't exists along with any intermediate directories, creates them",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be read, relative to the working directory. If not provided, throws an error",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written in the file. If not provided, writes an empty string.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        work_abs_path = get_abs_path(working_directory)
        joined = join_paths(work_abs_path, file_path)
        file_abs_path = get_abs_path(joined)

        if not path_contains(file_abs_path, work_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not path_exists(file_abs_path):
            dirs = os.path.dirname(file_path)
            if dirs and not os.path.exists(dirs):
                os.makedirs(dirs)

        with open(file_abs_path, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'