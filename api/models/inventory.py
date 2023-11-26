import datetime
import uuid
from enum import Enum
from typing import Optional, ClassVar

import qrcode
from sqlmodel import SQLModel, Field, Relationship

from api.config import CONFIG


class ContainerStatus(str, Enum):
    unused = 'unused'  # Container never opened
    used = 'used'  # Container already used
    removed = 'removed'  # Container discarded


class Label(SQLModel, table=True):
    id: Optional[str] = Field(default=str(uuid.uuid4()), primary_key=True)
    container: Optional['Container'] = Relationship(back_populates='label')
    printed: bool = False

    def create_qrcode(self) -> None:
        img = qrcode.make(self.id)
        img.save(f'api/attachments/{self.id}.png')


class ContainerBase(SQLModel):
    CONSERVATION_LIMIT_TIMEDELTA: ClassVar[datetime.timedelta] = datetime.timedelta(
        days=int(CONFIG['MILK']['conservation_limit_days'])
    )

    id: uuid.UUID = Field(primary_key=True, nullable=False)

    baby_name: str
    volume: float
    expressed_on: datetime.datetime = datetime.datetime.now()
    expires_on: datetime.datetime = expressed_on + CONSERVATION_LIMIT_TIMEDELTA
    status: str = Field(default=ContainerStatus.unused, nullable=False)


class Container(ContainerBase, table=True):
    label_id: Optional[int] = Field(default=None, foreign_key='label.id')
    label: Optional['Label'] = Relationship(back_populates='container')


class ContainerCreate(ContainerBase):
    pass


class ContainerRead(ContainerBase):
    pass


class ContainerDelete(ContainerBase):
    pass
