from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from api.core.security import create_tokens, verify_password
from api.models.user import UserIn, UserOut, Token, VerificationRequest
from api.db.user import get_user, create_user, get_current_user, verify_user, get_user_by_verification_token
from api.core.config import settings
from jose import jwt, JWTError
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, select_autoescape, PackageLoader

router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
    MAIL_STARTTLS= True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS = True,
    TEMPLATE_FOLDER = 'api/templates'
)

# Jinja2 template environment
env = Environment(
    loader=PackageLoader('api', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

async def send_verification_email(email: str, verification_token: str):
    # Create FastMail instance
    fm = FastMail(conf)
    
    # Render email template
    template = env.get_template('verification_email.html')
    html = template.render(
        verification_url=f"{settings.FRONTEND_URL}/?token={verification_token}"
    )
    
    # Create message
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=html,
        subtype="html"
    )
    
    # Send email
    await fm.send_message(message)

@router.post("/verify-email")
async def verify_email(verification_data: VerificationRequest):
    user = await get_user_by_verification_token(verification_data.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
    
    if user.is_active:
        return {"message": "Email already verified"}
    
    await verify_user(user.email)
    return {"message": "Email verified successfully", **create_tokens(user.email)}

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        token_type = payload.get("type")
        if email is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        user = await get_user(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return create_tokens(email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


@router.post("/register", response_model=UserOut)
async def register(user: UserIn, background_tasks: BackgroundTasks):
    db_user = await get_user(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    verification_token = str(uuid4())
    
    new_user = await create_user(
        UserIn(
            email=user.email,
            password=user.password,
            is_active=False
        ),  
        verification_token=verification_token,
    )
    
    background_tasks.add_task(send_verification_email, user.email, verification_token)
    
    return UserOut(
        email=new_user.email, 
        is_active=new_user.is_active, 
        credits=new_user.credits, 
        last_credit_reset=new_user.last_credit_reset
    )


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not verified",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return create_tokens(user.email)


@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user

