from sqlmodel import SQLModel, create_engine

from api.config import CONFIG

engine = create_engine(f"sqlite:///./{CONFIG['DB']['db_filename']}")


def create_tables():
    SQLModel.metadata.create_all(engine)
