# agents/image_scanner.py
from langchain.agents import tool
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from state import GraphState

@tool
def scan_images(state: GraphState) -> GraphState:
    """Scans a webpage and extracts image URLs into state."""
    try:
        response = requests.get(state.url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        image_tags = soup.find_all("img")

        image_urls = []
        for tag in image_tags:
            src = tag.get("src")
            if not src:
                continue
            full_url = urljoin(state.url, src)
            image_urls.append(full_url)

        state.image_urls = image_urls[:15]  # Limit to 15
    except Exception as e:
        state.image_urls = []
        state.error = str(e)

    return state
