from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    fullName: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str

class MessageResponse(BaseModel):
    message: str

class UserDataRequest(BaseModel):
    token: str

class UserDataResponse(BaseModel):
    fullName: str
    email: str
    id: int