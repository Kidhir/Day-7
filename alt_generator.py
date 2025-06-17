# agents/alt_generator.py
import google.generativeai as genai

genai.configure(api_key="AIzaSyAmZt-Pa31lf6TAZ_8p3S6qT2L8dNi-S1c")

def generate_alt(image_url, context_text=""):
    model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
    response = model.generate_content([
        image_url,
        f"Generate an accessible alt text for this image considering the following context: {context_text}"
    ])
    return response.text.strip()
