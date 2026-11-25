from pydantic import BaseModel, Field



class GoogleUserType(BaseModel):
    email: str = Field(..., description="The user's email address")
    name: str = Field(..., description="The user's full name")
    picture: str = Field(..., description="URL to the user's profile picture")
    provider: str = Field(..., description="The authentication provider (e.g., Google)")
    family_name: str = Field(description="The user's family name")
    phone_number: str = Field(description="The user's phone number")
    photos: list[str] = Field(..., description="List of URLs to the user's photos")

