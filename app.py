import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
from io import BytesIO

st.title("Web Page Image Viewer")

# User input for the URL
url = st.text_input("Enter a webpage URL to extract and view images:", "https://www.tate.org.uk/art/artworks")

if st.button("Scan Images"):
    if not url:
        st.warning("Please enter a valid URL.")
    else:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise if 4xx or 5xx
            soup = BeautifulSoup(response.content, "html.parser")
            image_tags = soup.find_all("img")

            if not image_tags:
                st.info("No images found on the page.")
            else:
                for idx, img in enumerate(image_tags[:15]):  # Limit to avoid overload
                    src = img.get("src")
                    if not src:
                        continue

                    # Handle relative image paths
                    full_img_url = urljoin(url, src)

                    try:
                        img_response = requests.get(full_img_url, timeout=5)
                        if img_response.status_code == 200:
                            image_data = Image.open(BytesIO(img_response.content))
                            st.image(image_data, caption=f"Image #{idx + 1}", use_container_width=True)
                    except Exception as e:
                        st.warning(f"Skipping image #{idx + 1}: {e}")

        except Exception as e:
            st.error(f"Failed to fetch or parse the URL: {e}")
