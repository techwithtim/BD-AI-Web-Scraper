import streamlit as st
import requests
import time

st.title("Web Scraping Code Generator")

# Input fields
url = st.text_input("Website URL")
language = st.selectbox("Language", ["Python", "JavaScript"])
library = st.selectbox("Library", ["Selenium", "Playwright", "Pupeteer"])
prompt = st.text_area("Prompt (What data do you want to extract?)")

API_URL = "http://127.0.0.1:8000"
API_KEY = "your_api_token_here"


def send_start_request(url, prompt, language, library):
    api_url = f"{API_URL}/start-ai-scrape"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,  # Replace with your actual API token
    }

    data = {"url": url, "prompt": prompt, "language": language, "library": library}
    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json().get("job_id")
    else:
        st.error("Failed to start the task")
        return None


def poll_status(job_id):
    status_url = f"{API_URL}/get-ai-scrape/{job_id}"
    headers = {"X-API-Key": API_KEY}  # Replace with your actual API token
    while True:
        response = requests.get(status_url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "Completed":
                return result["result"]
            elif result["status"] == "Failed":
                return result["result"]
            else:
                time.sleep(5)  # Poll every 5 seconds
        else:
            st.error("Error fetching the task status")
            return {"error": "error fetching status"}


if st.button("Generate Scraping Code"):
    if url and prompt:
        status_text = st.empty()
        status_text.text("Starting code generation...")

        # Step 1: Send the request to start the scraping task
        job_id = send_start_request(url, prompt, language, library)

        if job_id:
            status_text.text(f"Task started (Job ID: {job_id}). Polling for status...")

            # Step 2: Poll the task status and get the final result
            with st.spinner("Generating code..."):
                parsed_result = poll_status(job_id)

            if "error" in parsed_result:
                st.write(parsed_result.get("error"))
            elif parsed_result:
                st.subheader("Website Preview")
                st.components.v1.html(
                    parsed_result.get("html"), height=500, scrolling=True
                )

                tags = parsed_result.get("tags")
                if len(tags) == 0:
                    st.write(parsed_result.get("text"))

                for key in tags.keys():
                    content = tags.get(key)
                    if key == "SCRAPING_CODE":
                        with st.expander("Generated Code", expanded=True):
                            st.code(content, language=language.lower())
                        status_text.text("Done!")
                    else:
                        st.subheader(key)
                        st.write(content)

    else:
        st.warning("Please enter a URL and prompt before generating code.")
