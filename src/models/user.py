from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from ..db import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("admin", "user", name="role types"), nullable=False
    )
    trigger_application_id: Mapped[int] = mapped_column(nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"User\nID: {self.id}\nName: {self.name}\nApp ID: {self.trigger_application_id}"
