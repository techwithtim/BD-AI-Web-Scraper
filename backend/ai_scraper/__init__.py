from .chunking import chunk_dom_sections
from .claude import send_dom_chunks_to_claude
from .openai import send_dom_chunks_to_openai
from .filtering import prune_dom, extract_relevant_dom
from .scraping import scrape_website


def parse_output(output):
    tags = [
        "SETUP_INSTRUCTIONS",
        "SCRAPING_CODE",
    ]
    results = {}

    for tag in tags:
        start_tag = output.find(f"[{tag}]")
        end_tag = output.find(f"[/{tag}]")
        if start_tag != -1 and end_tag != -1:
            content = output[start_tag + len(tag) + 2 : end_tag]
            results[tag] = content

    return results
