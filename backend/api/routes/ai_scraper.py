from api.routes.scrape_logic import scrape_with_ai
from fastapi import Depends, BackgroundTasks, HTTPException, APIRouter
from api.models.ai_scraper import AIScrapeData
from api.models.user import UserOut
from api.db.user import update_user_credits, get_current_user
from api.db.job import create_job, delete_job, get_job, get_user_jobs
from api.models.job import JobModel
import time
from datetime import datetime

router = APIRouter()


async def check_user_credits(user: UserOut = Depends(get_current_user)):
    if user.credits <= 0:
        raise HTTPException(status_code=403, detail="Insufficient credits")
    return user


@router.post("/start-ai-scrape")
async def start_ai_scrape(
    data: AIScrapeData,
    background_tasks: BackgroundTasks,
    user: UserOut = Depends(check_user_credits),
):
    # Access the data fields
    url = data.url
    prompt = data.prompt
    language = data.language
    library = data.library

    # Deduct one credit
    updated_user = await update_user_credits(user.email, -1)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user credits")

    job = JobModel(
        user_id=user.id,
        status="STARTED",
        start_time=datetime.now(),
        scrape_data=data.dict(),
    )
    job_id = str(await create_job(job))

    background_tasks.add_task(scrape_with_ai, job_id, url, prompt, language, library)

    return {
        "job_id": job_id,
        "message": "Task started. Poll /get-ai-scrape/{job_id} for updates.",
        "credits_remaining": updated_user.credits,
    }


@router.get("/get-ai-scrape/{job_id}")
async def get_ai_scrape(job_id: str, current_user: UserOut = Depends(get_current_user)):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if str(job.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this job")
    return job


@router.get("/user-jobs")
async def get_user_jobs_route(current_user: UserOut = Depends(get_current_user)):
    jobs = await get_user_jobs(str(current_user.id))
    return jobs


@router.delete("/delete-job/{job_id}")
async def delete_user_job(
    job_id: str, current_user: UserOut = Depends(get_current_user)
):
    deleted = await delete_job(job_id, str(current_user.id))
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job not found or you don't have permission to delete it",
        )
    return {"message": "Job deleted successfully"}
