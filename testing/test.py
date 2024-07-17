import requests
import re

def get_title_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            return title
        else:
            return "No title found"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

web_url = "http://localhost:5004"
title = get_title_from_web(web_url)

assert title == "rcofwork | Homepage"
print("Testing success")