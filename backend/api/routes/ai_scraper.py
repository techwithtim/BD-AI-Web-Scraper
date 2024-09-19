import os
from typing import Iterable
from fastapi import Depends, BackgroundTasks, HTTPException, APIRouter
from api.models.ai_scraper import AIScrapeData
from api.models.custom_types import TaskStatus
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
import time

load_dotenv()

MODEL = os.getenv("MODEL", "openai")

job_status = {}
job_results = {}

router = APIRouter()


def scrape_with_ai(job_id, url, prompt, language, library):
    job_results[job_id] = {"tags": {}, "text": None, "html": None}

    try:
        job_status[job_id] = TaskStatus.IN_PROGRESS
        html_content = scrape_website(str(url))
        job_results[job_id]["html"] = html_content
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
        job_status[job_id] = TaskStatus.FAILED
        job_results[job_id]["error"] = str(e)
        return job_results[job_id]

    result_dict = {}
    if not result:
        job_status[job_id] = TaskStatus.FAILED
    else:
        job_status[job_id] = TaskStatus.COMPLETED
        if result and isinstance(result, Iterable):
            result_dict = parse_output(result)

    job_results[job_id] = {
        "tags": result_dict,
        "text": result,
        "html": html_content,
    }
    return job_results[job_id]


@router.post("/start-ai-scrape")
async def start_ai_scrape(
    data: AIScrapeData,
    background_tasks: BackgroundTasks,
):
    # Access the data fields
    url = data.url
    prompt = data.prompt
    language = data.language
    library = data.library

    job_id = f"job-{int(time.time())}"

    # Add the task to background tasks
    background_tasks.add_task(scrape_with_ai, job_id, url, prompt, language, library)

    # Initially set status to 'Started'
    job_status[job_id] = TaskStatus.STARTED

    return {
        "job_id": job_id,
        "message": "Task started. Poll /get-ai-scrape/{job_id} for updates.",
    }


@router.get("/get-ai-scrape/{job_id}")
async def get_ai_scrape(job_id: str):
    if job_id in job_status:
        return {
            "job_id": job_id,
            "status": job_status[job_id],
            "result": job_results[job_id],
        }
    else:
        raise HTTPException(status_code=404, detail="Job not found")
