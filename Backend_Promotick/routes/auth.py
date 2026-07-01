from fastapi import APIRouter, HTTPException
from models.user import UserRegister, UserLogin
from services.storage_service import get_connection

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register")
def register(user: UserRegister):

    conn = get_connection()

    try:
        conn.execute(
            "INSERT INTO users(username,password) VALUES (?,?)",
            (user.username, user.password)
        )

        conn.commit()

        return {
            "message": "Usuario registrado correctamente"
        }

    except:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    finally:
        conn.close()


@router.post("/login")
def login(user: UserLogin):

    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (user.username, user.password)
    )

    data = cursor.fetchone()

    conn.close()

    if not data:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    return {
        "success": True,
        "user": user.username
    }