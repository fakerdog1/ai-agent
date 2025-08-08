import os
import subprocess
from functions.get_files_info import get_abs_path, path_contains, join_paths, path_exists

def run_python_file(working_directory, file_path, args=[]):
    try:
        work_abs = get_abs_path(working_directory)
        joined = join_paths(work_abs, file_path)
        file_abs = get_abs_path(joined)

        if not path_contains(file_abs, work_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not path_exists(file_abs):
            return f'Error: File "{file_path}" not found.'

        if not file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file.'
        
        completed = subprocess.run(["python", file_abs] + args, timeout=30, capture_output=True, cwd=work_abs)
        if completed.stdout:
            return_str = f"STDOUT: {completed.stdout}, STDERR: {completed.stderr}"
        else:
            return_str = "No output produced."
        if completed.returncode != 0:
            return_str += f"Process exited with code {completed.returncode}"

        return return_str
    except Exception as e:
        return f"Error: {e}"