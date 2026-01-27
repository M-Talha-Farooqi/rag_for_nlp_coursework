import os
from dotenv import load_dotenv

def save_key(key_name: str, key_value: str):
    """
    Saves a new API key to the .env file and reloads the environment.
    """
    env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
    
    # 1. Read existing lines
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    # 2. Update or Append
    key_found = False
    new_line = f"{key_name}={key_value}\n"
    
    updated_lines = []
    for line in lines:
        if line.startswith(f"{key_name}="):
            updated_lines.append(new_line)
            key_found = True
        else:
            updated_lines.append(line)
    
    if not key_found:
        if updated_lines and not updated_lines[-1].endswith('\n'):
            updated_lines.append('\n')
        updated_lines.append(new_line)

    # 3. Write back
    with open(env_path, "w") as f:
        f.writelines(updated_lines)

    # 4. Reload immediately
    load_dotenv(override=True)