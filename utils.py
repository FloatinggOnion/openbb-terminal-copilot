import re
import time

def sanitize_message(message: str) -> str:
    """Sanitize a message by escaping forbidden characters."""
    cleaned_message = re.sub(r"(?<!\{)\{(?!{)", "{{", message)
    cleaned_message = re.sub(r"(?<!\})\}(?!})", "}}", cleaned_message)
    return cleaned_message


def create_message_stream(message: str):
    """Stream a message word by word to the console."""
    words = message.split()
    for word in words:
        yield f"data: {word}"
        time.sleep(0.5)  # Adjust the delay as needed
        