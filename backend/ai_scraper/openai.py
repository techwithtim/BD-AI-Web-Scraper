import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from .chunking import estimate_tokens
from .prompts import SYSTEM

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def send_dom_chunks_to_openai(dom_chunks, prompt, library, language, url):
    final_messages = [{"role": "system", "content": SYSTEM}]
    total_tokens = estimate_tokens(SYSTEM)

    # Combine all DOM chunks into a single user message
    combined_dom = "Relevant DOM Sections:\n\n"
    for i, chunk in enumerate(dom_chunks):
        chunk_content = f"Chunk {i+1}:\n{chunk}\n\n"
        if total_tokens + estimate_tokens(chunk_content) > 30000:
            break
        combined_dom += chunk_content
        total_tokens += estimate_tokens(chunk_content)

    final_messages.append({"role": "user", "content": combined_dom})

    # Add the user prompt
    user_prompt = f"Write scraping code that extracts {prompt} from {url} using {library} in {language}. "
    final_messages.append({"role": "user", "content": user_prompt})

    with open("test.json", "w") as f:
        json.dump({"messages": final_messages}, f)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=final_messages,
            max_tokens=4096,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise e
