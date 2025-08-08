import os
from functions.get_files_info import get_abs_path, path_contains, join_paths, path_exists

def write_file(working_dir, file_path, content):
    try:
        work_abs_path = get_abs_path(working_dir)
        joined = join_paths(work_abs_path, file_path)
        file_abs_path = get_abs_path(joined)

        if not path_contains(file_abs_path, work_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not path_exists(file_abs_path):
            dirs = os.path.dirname(file_path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)

        with open(file_abs_path, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'