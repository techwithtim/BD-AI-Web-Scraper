import os
import json
import anthropic
from dotenv import load_dotenv
from .chunking import estimate_tokens
from .prompts import get_prompt

load_dotenv()

CLAUDE_API_TOKEN = os.getenv("CLAUDE_API_TOKEN")
client = anthropic.Client(api_key=CLAUDE_API_TOKEN)


def send_dom_chunks_to_claude(dom_chunks, prompt, library, language, url, with_bd=False):
    final_messages = []
    sys_prompt = get_prompt(language, library, with_bd)
    total_tokens = estimate_tokens(sys_prompt)

    # Combine all DOM chunks into a single user message
    combined_dom = "Relevant DOM Sections:\n\n"
    for i, chunk in enumerate(dom_chunks):
        chunk_content = f"Chunk {i+1}:\n{chunk}\n\n"
        if (
            total_tokens + estimate_tokens(chunk_content) > 150000
        ):  # Safe limit to avoid exceeding 200k
            break
        combined_dom += chunk_content
        total_tokens += estimate_tokens(chunk_content)

    final_messages.append({"role": "user", "content": combined_dom})

    # Add the user prompt
    user_prompt = f"Write scraping code that extracts data from {url} using {library} in {language}. {prompt}"
    final_messages.append(
        {
            "role": "assistant",
            "content": "Understood.",
        }
    )
    final_messages.append({"role": "user", "content": user_prompt})

    with open("test.json", "w") as f:
        json.dump({"messages": final_messages}, f)

    total_tokens += estimate_tokens(user_prompt)

    if total_tokens > 200000:
        raise Exception("Token size exceeded.")

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=final_messages,
            system=sys_prompt,
        )
        return response.content
    except anthropic.APIError as e:
        raise e
