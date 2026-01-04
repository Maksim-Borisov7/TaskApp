from fastapi import HTTPException
from backend.app.core.jwt_utils import encode_jwt
from backend.app.dependencies.auth import validate_auth_user
from backend.app.repositories.users import UserRepository
from backend.app.schemas.user_schemas import TokenInfo


class AuthUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, username, password) -> TokenInfo:
        """
        Генерирует JWT токен для пользователя после успешной авторизации.
        Проверка пользователя и пароля проводится в Depends(validate_auth_user).
        """
        user = await validate_auth_user(self.repo, username, password)

        if not user.username or not user.email:
            raise HTTPException(status_code=400, detail="Невалидные данные пользователя")

        jwt_payload = {
            "sub": str(user.id),
            "username": user.username,
        }
        token = encode_jwt(jwt_payload)

        return TokenInfo(
            access_token=token,
            token_type="Bearer",
        )

