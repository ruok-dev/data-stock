from sqlmodel import Session, create_engine, SQLModel
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)


def init_db() -> None:
    # This will be replaced by Alembic in a real production environment
    # But for initialization/dev, it's useful.
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
