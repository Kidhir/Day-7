import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

st.title("Safe Web Image Viewer")

url = st.text_input("Enter a webpage URL:", "https://www.tate.org.uk/art/artworks")

def load_and_validate_image(img_url: str):
    try:
        resp = requests.get(img_url, timeout=5)
        if resp.status_code != 200:
            return None

        content_type = resp.headers.get("Content-Type", "")
        if not content_type.startswith("image/") or "svg" in content_type.lower():
            return None

        img_bytes = BytesIO(resp.content)
        img = Image.open(img_bytes)
        img.verify()

        # Convert to RGB (safe for Streamlit)
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        return img
    except Exception:
        return None

if st.button("Fetch Images"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        image_tags = soup.find_all("img")

        if not image_tags:
            st.info("No images found.")
        else:
            for idx, tag in enumerate(image_tags[:15]):
                src = tag.get("src")
                if not src:
                    continue

                image_url = urljoin(url, src)
                image = load_and_validate_image(image_url)

                if image:
                    st.image(image, caption=f"Image #{idx + 1}", use_container_width=True)
                else:
                    st.warning(f"Skipped invalid image #{idx + 1}")
    except Exception as e:
        st.error(f"Failed to load page: {e}")
