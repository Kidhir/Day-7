import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.title("Safe Web Image Viewer (No PIL)")

url = st.text_input("Enter a webpage URL:", "https://www.tate.org.uk/art/artworks")

def is_valid_image_response(resp):
    """Checks if the HTTP response is a valid image Streamlit can handle."""
    content_type = resp.headers.get("Content-Type", "")
    return (
        resp.status_code == 200
        and content_type.startswith("image/")
        and "svg" not in content_type.lower()
    )

if st.button("Fetch Images"):
    try:
        page = requests.get(url, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
        img_tags = soup.find_all("img")

        if not img_tags:
            st.info("No images found.")
        else:
            for idx, tag in enumerate(img_tags[:15]):
                src = tag.get("src")
                if not src:
                    continue

                image_url = urljoin(url, src)
                try:
                    img_resp = requests.get(image_url, timeout=5)
                    if is_valid_image_response(img_resp):
                        st.image(img_resp.content, caption=f"Image #{idx + 1}", use_container_width=True)
                    else:
                        st.warning(f"Skipped invalid image #{idx + 1}: {image_url}")
                except Exception as e:
                    st.warning(f"Error fetching image #{idx + 1}: {e}")
    except Exception as e:
        st.error(f"Failed to fetch page: {e}")
