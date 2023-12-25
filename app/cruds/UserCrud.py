from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlalchemy.future import select

from app.models.Models import UserModel
from app.schemas.UserSchema import UserInSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(session: AsyncSession, user: UserInSchema):
    new_user = UserModel(username=user.username, email=user.email, password=pwd_context.hash(user.password), is_active=user.is_active, is_admin=user.is_admin)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_id(user_id: int, session: AsyncSession):
    return await session.get(UserModel, user_id)


async def get_user_by_username(username: str, session: AsyncSession):
    statement = select(UserModel).where(UserModel.username == username)
    result = await session.execute(statement)
    return result.scalars().one_or_none()


async def get_user_by_email(email: str, session: AsyncSession):
    statement = select(UserModel).where(UserModel.email == email)
    result = await session.execute(statement)
    return result.scalars().one_or_none()
