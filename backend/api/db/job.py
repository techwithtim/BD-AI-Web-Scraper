from api.db.mongodb import database
from api.models.job import JobModel


async def create_job(job: JobModel):
    job_dict = job.model_dump(by_alias=True)
    result = await database.jobs.insert_one(job_dict)
    return str(result.inserted_id)


async def get_job(job_id: str):
    job = await database.jobs.find_one({"_id": job_id})
    if job:
        return JobModel(**job)


async def update_job(job_id: str, update_data: dict):
    result = await database.jobs.update_one({"_id": job_id}, {"$set": update_data})
    if result.modified_count == 1:
        return True
    return False


async def get_user_jobs(user_id: str):
    cursor = database.jobs.find({"user_id": user_id})
    jobs = await cursor.to_list(length=100)  # Limit to 100 most recent jobs
    return [JobModel(**job) for job in jobs]


async def delete_job(job_id: str, user_id: str):
    result = await database.jobs.delete_one({"_id": job_id, "user_id": user_id})
    return result.deleted_count > 0
