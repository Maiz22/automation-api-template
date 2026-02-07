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

    # Only for users
    trigger_app_id: Mapped[str] = mapped_column(nullable=True)
    locel_device_webhook: Mapped[str] = mapped_column(nullable=True)

    # Only for admin
    username: Mapped[str] = mapped_column(nullable=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"User\nID: {self.id}\nName: {self.name}\nRole: {self.role}"
