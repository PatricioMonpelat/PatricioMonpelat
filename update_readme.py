import requests
import re
from datetime import datetime
import pytz


def get_quote():
    try:
        resp = requests.get("https://zenquotes.io/api/today", timeout=10)
        data = resp.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return "> **Frase del dia:** _" + quote + "_ - **" + author + "**"
    except Exception:
        return "> **Frase del dia:** _No se pudo obtener la frase hoy._"


def get_timestamp():
    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    now = datetime.now(tz)
    formatted = now.strftime("%d/%m/%Y %H:%M (UTC-3)")
    return "Ultima actualizacion: " + formatted


def replace_section(content, start_tag, end_tag, new_content):
    nl = "\n"
    replacement = start_tag + nl + new_content + nl + end_tag
    pattern = start_tag + ".*?" + end_tag
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def update_readme(quote_text, updated_text):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    content = replace_section(content, "<!-- QUOTE_START -->", "<!-- QUOTE_END -->", quote_text)
    content = replace_section(content, "<!-- LAST_UPDATED_START -->", "<!-- LAST_UPDATED_END -->", updated_text)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    quote = get_quote()
    timestamp = get_timestamp()
    update_readme(quote, timestamp)
    print("README updated!")
    print(quote)
    print(timestamp)
