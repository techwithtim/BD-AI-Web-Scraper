from pydantic import BaseModel, HttpUrl, constr, validator, EmailStr


class AIScrapeData(BaseModel):
    url: HttpUrl  # Ensures the URL is valid
    prompt: constr(min_length=1, max_length=100)
    language: str
    library: str
    performance: int
    with_bd: bool

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["url"] = str(d["url"])  # Convert URL to string
        return d

    def model_dump(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        d["url"] = str(d["url"])  # Convert URL to string
        return d

    # Validate language to be either "python" or "javascript"
    @validator("language")
    def validate_language(cls, value):
        if value.lower() not in {"python", "javascript", "c#"}:
            raise ValueError("Language must be either 'python', 'javascript' or 'c#' ")
        return value

    # Validate library to be either "playwright", "puppeteer", or "selenium"
    @validator("library")
    def validate_library(cls, value):
        if value.lower() not in {"playwright", "puppeteer", "selenium"}:
            raise ValueError(
                "Library must be either 'playwright', 'puppeteer', or 'selenium'"
            )
        return value

    @validator("performance")
    def validate_performance(cls, value):
        if not isinstance(value, int) or value < 1 or value > 4:
            raise ValueError("Performance must be a whole number between 1 and 4")
        return value