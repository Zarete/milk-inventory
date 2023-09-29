from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select

from api.db import create_tables, engine
from api.models.inventory import Container, Label, ContainerCreate, ContainerRead, ContainerStatus

app = FastAPI()


@app.on_event('startup')
def on_startup():
    create_tables()


@app.get('/container/{container_id}', response_model=ContainerRead)
async def get_container(container_id):
    with Session(engine) as session:
        container = session.exec(
            select(
                Container
            ).where(
                Container.id == container_id,
                Container.status != ContainerStatus.removed
            )
        ).first()

    if container is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Container not found')

    return container


@app.post('/container/add', status_code=status.HTTP_201_CREATED)
async def add_container(container: ContainerCreate):
    label = Label()
    label.create_qrcode()
    container_db = Container.from_orm(container)
    container_db.label = label

    with Session(engine) as session:
        session.add(container_db)
        session.commit()
        session.refresh(container_db)

    return container_db


@app.delete('/container/remove/{container_id}')
async def remove_container(container_id: str):
    with Session(engine) as session:
        container = session.exec(
            select(Container).where(Container.id == container_id)
        ).first()
        container.status = ContainerStatus.removed
        session.add(container)
        session.commit()
        session.refresh(container)
    return container
