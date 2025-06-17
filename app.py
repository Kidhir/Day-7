import streamlit as st
from agents.image_scanner import scan_images_from_url
from agents.alt_generator import generate_alt
from agents.rag_retriever import fetch_best_practice

st.set_page_config(page_title="Auto Alt Text Generator", layout="wide")
st.title("🧠 Auto Alt Text Generator for Accessibility & SEO")

# --- Step 1: Input website URL ---
url = st.text_input("Enter Website URL to Scan for Images", placeholder="https://unsplash.com/s/photos/nature")

if url:
    with st.spinner("🔍 Scanning images..."):
        images = scan_images_from_url(url)

    if not images:
        st.warning("No images found on the page.")
    else:
        st.subheader("📷 Image Results")

        for idx, img in enumerate(images):
            if img["status"] == "Good":
                continue  # Skip good ones

            st.markdown("---")
            cols = st.columns([2, 3])
            with cols[0]:
                st.image(img["src"], caption=f"Image #{idx + 1}", use_column_width=True)

            with cols[1]:
                st.write(f"**Current Alt Text:** {img['alt'] or '❌ Missing'}")
                st.write(f"**Status:** `{img['status']}`")

                # Generate alt text and fetch best practices
                with st.spinner("⚙️ Generating alt text..."):
                    generated = generate_alt(img["src"])
                    best_practice = fetch_best_practice("How to write best alt text according to WCAG?")

                st.text_area("🔎 Suggested Alt Text", value=generated, height=100, key=f"gen_{idx}")
                edited_alt = st.text_input("✍️ Edit Alt Text (Optional)", value=generated, key=f"edit_{idx}")
                st.markdown(f"📝 **WCAG Tip:** _{best_practice}_")

        st.success("✅ Review complete. Copy your final alt texts as needed!")

else:
    st.info("Please enter a website URL above to begin scanning.")

#----------------------------------------#

# Only proceed if images were found
if url and 'images' in locals() and images:
    import pandas as pd

    # Collect results
    alt_results = []
    for idx, img in enumerate(images):
        gen_key = f"gen_{idx}"
        edit_key = f"edit_{idx}"
        alt_results.append({
            "Image URL": img["src"],
            "Original Alt": img["alt"],
            "Generated Alt": st.session_state.get(gen_key),
            "Final Alt": st.session_state.get(edit_key)
        })

    df = pd.DataFrame(alt_results)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Alt Texts as CSV", data=csv, file_name="alt_texts.csv", mime="text/csv")

