import requests
import re
from datetime import datetime
import pytz


def get_quote():
    """Fetch quote of the day from ZenQuotes API."""
    try:
        resp = requests.get("https://zenquotes.io/api/today", timeout=10)
        data = resp.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f"> 💬 **Frase del día:** _{quote}_ — **{author}**"
    except Exception:
        return "> 💬 **Frase del día:** _No se pudo obtener la frase hoy._"


def get_timestamp():
    """Get current datetime in Argentina timezone."""
    tz = pytz.timezone("America/Argentina/Buenos_Aires")
    now = datetime.now(tz)
    formatted = now.strftime("%d/%m/%Y %H:%M (UTC-3)")
    return f"🕐 **Última actualización:** {formatted}"


def update_readme(quote_text, updated_text):
    """Replace placeholder sections in README.md."""
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r"<!-- QUOTE_START -->.*?<!-- QUOTE_END -->",
        f"<!-- QUOTE_START -->
{quote_text}
<!-- QUOTE_END -->",
        content,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"<!-- LAST_UPDATED_START -->.*?<!-- LAST_UPDATED_END -->",
        f"<!-- LAST_UPDATED_START -->
{updated_text}
<!-- LAST_UPDATED_END -->",
        content,
        flags=re.DOTALL,
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    quote = get_quote()
    timestamp = get_timestamp()
    update_readme(quote, timestamp)
    print("README updated successfully!")
    print(f"Quote: {quote}")
    print(f"Timestamp: {timestamp}")
