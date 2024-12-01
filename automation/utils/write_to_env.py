from pathlib import Path

def write_to_env(key: str, value: str, file_path: Path = Path('.env')):
    """
    Writes a key-value pair to a .env file.
    If the file does not exist, it is created.
    """
    if not file_path.exists():
        file_path.touch()

    env_lines = file_path.read_text().splitlines()

    key_value_pair = f'{key}="{value}"'
    updated = False
    for i, line in enumerate(env_lines):
        if line.startswith(f"{key}="):
            env_lines[i] = key_value_pair  # Update the existing line
            updated = True
            break

    if not updated:
        env_lines.append(key_value_pair)

    file_path.write_text("\n".join(env_lines) + "\n")
