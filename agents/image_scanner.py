# agents/image_scanner.py
from bs4 import BeautifulSoup
import requests

def scan_images_from_url(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    images = soup.find_all('img')

    result = []
    for img in images:
        alt = img.get('alt', '').strip()
        status = "Missing" if not alt else "Generic" if len(alt.split()) <= 2 else "Good"

        # NEW: extract context from parent
        context = ""
        parent = img.find_parent()
        if parent:
            context = parent.get_text(strip=True)

        result.append({
            'src': img.get('src'),
            'alt': alt,
            'status': status,
            'context': context  # include the surrounding context for further processing
        })

    return result
