import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_path_files(basepath):
    dir_list = os.listdir(basepath)
    item_info = []
    for item in dir_list:
        abs_path = os.path.join(basepath, item)
        if os.path.isfile(abs_path):
            item_info.append({
                "name": item,
                "size": os.path.getsize(abs_path),
                "is_dir": False
            })
        else: 
            item_info.append({
                "name": item,
                "size": get_dir_size(abs_path),
                "is_dir": True
            })
        
    return item_info

def get_dir_size(path):
    total = 0
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path):
            total += os.path.getsize(entry_path)
        else : 
            total += get_dir_size(entry_path)

    return total

def get_abs_path(dir):
    return os.path.abspath(dir)

def path_contains(path, contains):
    return path.startswith(contains)

def join_paths(base, sub):
    return os.path.join(base, sub)

def path_exists(path):
    return os.path.exists(path)

def get_files_info(working_directory, directory="."):
    try:
        working_abs_path = get_abs_path(working_directory)
        joined_path = join_paths(working_directory, directory)
        abs_path = get_abs_path(joined_path)

        directory = "current" if directory == "." else f"'{directory}'"
        out_str = f"Resul for {directory} directory\n"

        if not path_contains(abs_path, working_abs_path):
            error_msg = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            out_str += error_msg
            return out_str
        
        if not os.path.isdir(abs_path):
            error_msg = f'Error: "{directory}" is not a directory'
            out_str += error_msg
            return out_str
        
        item_info = get_path_files(abs_path)
        
        for item in item_info:
            out_str += f"- {item['name']}: file_size={item['size']} bytes, is_dir={item['is_dir']}\n"
        
        return out_str
    except Exception as e:
        return e
    
