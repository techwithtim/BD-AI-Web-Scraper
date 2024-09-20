from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated
from datetime import datetime
from bson import ObjectId


class JobModel(BaseModel):
    id: Annotated[str, Field(default_factory=lambda: str(ObjectId()), alias="_id")]
    user_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    result: Optional[dict] = None
    scrape_data: dict

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "user_id": "60d5ec9f1c9d440000d1e2b4",
                "status": "COMPLETED",
                "start_time": "2023-06-01T12:00:00",
                "end_time": "2023-06-01T12:05:00",
                "result": {"data": "Scraped content", "html": "", "text": ""},
                "scrape_data": {
                    "url": "https://example.com",
                    "prompt": "Scrape all headers",
                    "library": "selenium",
                    "language": "Python",
                },
            }
        },
    )
