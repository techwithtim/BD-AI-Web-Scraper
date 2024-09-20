import os
from typing import Iterable
from dotenv import load_dotenv
from ai_scraper import (
    send_dom_chunks_to_claude,
    send_dom_chunks_to_openai,
    chunk_dom_sections,
    prune_dom,
    parse_output,
    extract_relevant_dom,
    scrape_website,
)
from api.db.job import update_job
from datetime import datetime

load_dotenv()
MODEL = os.getenv("MODEL", "openai")


async def scrape_with_ai(job_id, url, prompt, language, library):
    job = {
        "result": {"tags": {}, "text": None, "html": None},
        "status": "In Progress",
    }
    await update_job(job_id, job)

    try:
        html_content = scrape_website(str(url))
        job["result"]["html"] = html_content
        job["status"] = "In Progress"
        pruned_html = prune_dom(html_content)
        relevant_dom = extract_relevant_dom(pruned_html, prompt)
        dom_chunks = chunk_dom_sections(relevant_dom)
        if MODEL == "openai":
            result = send_dom_chunks_to_openai(
                dom_chunks, prompt, library, language, url
            )
        else:
            result = send_dom_chunks_to_claude(
                dom_chunks, prompt, library, language, url
            )
    except Exception as e:
        job["status"] = "Failed"
        job["error"] = str(e)
        job["end_time"] = datetime.now()
        await update_job(job_id, job)
        return job

    result_dict = {}
    if result and isinstance(result, Iterable):
        result_dict = parse_output(result)

    job["status"] = "Completed"
    job["end_time"] = datetime.now()
    job["result"] = {
        "tags": result_dict,
        "text": result,
        "html": html_content,
    }
    await update_job(job_id, job)
    return job
