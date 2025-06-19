import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image, UnidentifiedImageError
from io import BytesIO

st.title("Generic Image Viewer")

# Get URL input from user
url = st.text_input("Enter a webpage URL:", "https://www.tate.org.uk/art/artworks")

if st.button("Fetch Images"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        image_tags = soup.find_all("img")

        if not image_tags:
            st.info("No images found.")
        else:
            for idx, tag in enumerate(image_tags[:15]):  # limit to 15 images
                src = tag.get("src")
                if not src:
                    continue

                image_url = urljoin(url, src)
                try:
                    img_response = requests.get(image_url, timeout=5)
                    if img_response.status_code == 200 and img_response.headers["Content-Type"].startswith("image/"):
                        image_data = BytesIO(img_response.content)
                        try:
                            image = Image.open(image_data)
                            st.image(image, caption=f"Image #{idx + 1}", use_container_width=True)
                        except UnidentifiedImageError:
                            st.warning(f"Image #{idx + 1} could not be identified as a valid image format.")
                except Exception as e:
                    st.warning(f"Error loading image #{idx + 1}: {e}")
    except Exception as e:
        st.error(f"Failed to load page: {e}")
