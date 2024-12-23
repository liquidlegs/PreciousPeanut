import yaml
from dataclasses import dataclass

CONFIG_PATH = "../config.yaml"

@dataclass
class ConfigFile():
    display: str
    bg_colour: str
    fg_colour: str
    text_size: int
    font_fam: str
    cursor_colour: str
    highlight_colour: str
    word_wrap: bool
    xor_key: str
    toolbar_colour: str


def load_config_file() -> ConfigFile:
    content = read_file(CONFIG_PATH)
    dict = load_yaml(content)

    output = ConfigFile(
        display=catch_key_exception(dict, "display"),
        bg_colour=catch_key_exception(dict, "bg_colour"),
        fg_colour=catch_key_exception(dict, "fg_colour"),
        text_size=catch_key_exception(dict, "text_size"),
        font_fam=catch_key_exception(dict, "font_fam"),
        cursor_colour=catch_key_exception(dict, "cursor_colour"),
        highlight_colour=catch_key_exception(dict, "highlight_colour"),
        word_wrap=catch_key_exception(dict, "word_wrap"),
        xor_key=catch_key_exception(dict, "xor_key"),
        toolbar_colour=catch_key_exception(dict, "toolbar_colour"),
    )

    return output


def catch_key_exception(data: dict[str], key: str) -> str:
    output = None

    try:
        output = data[key]
        return output
    except KeyError as e:
        print(f"Error: unable find key in python dictonary - {e}")
        return None


def update_config_file(config: ConfigFile) -> bool:
    if config == None:
        return False
    
    output = config.__dict__
    content = yaml.dump(output)

    write_file(CONFIG_PATH, content)
    return True


def load_yaml(content: str) -> str:
    data = None

    try:
        data = yaml.safe_load(content)
        return data
    except KeyError as e:
        print(f"Error: unable to parse yaml - {e}")
        return None


def read_file(file_name: str) -> str:
    buffer = ""

    with open(file_name, "r") as f:
        buffer = f.read()

    return buffer


def write_file(file_name: str, content: str) -> bool:
    if content == None:
        return None
    
    with open(file_name, "w") as f:
        size = f.write(content)

        if size > 0:
            print(f"Successfully wrote {size} bytes to {file_name}")
            return True
        else:
            print(f"Failed to write content to {file_name}")
            return False
        
    return False