from pydantic import BaseModel, HttpUrl, constr, validator, EmailStr


class AIScrapeData(BaseModel):
    url: HttpUrl  # Ensures the URL is valid
    prompt: constr(min_length=1, max_length=100)
    language: str
    library: str

    # Validate language to be either "python" or "javascript"
    @validator("language")
    def validate_language(cls, value):
        if value.lower() not in {"python", "javascript"}:
            raise ValueError("Language must be either 'python' or 'javascript'")
        return value

    # Validate library to be either "playwright", "puppeteer", or "selenium"
    @validator("library")
    def validate_library(cls, value):
        if value.lower() not in {"playwright", "puppeteer", "selenium"}:
            raise ValueError(
                "Library must be either 'playwright', 'puppeteer', or 'selenium'"
            )
        return value