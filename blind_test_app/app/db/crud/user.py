import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, JudgeCreate
from app.core.security import get_password_hash, verify_password


class CRUDUser:
    def get(self, db: Session, user_id: uuid.UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def get_by_role(self, db: Session, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: UserCreate, created_by_admin_id: Optional[uuid.UUID] = None) -> User:
        db_obj = User(
            email=obj_in.email,
            password_hash=get_password_hash(obj_in.password),
            role=obj_in.role,
            name=obj_in.name,
            surname=obj_in.surname,
            phone=obj_in.phone,
            is_active=obj_in.is_active,
            created_by_admin_id=created_by_admin_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_judge(self, db: Session, obj_in: JudgeCreate, admin_id: uuid.UUID, password: str) -> User:
        db_obj = User(
            email=obj_in.email,
            password_hash=get_password_hash(password),
            role=UserRole.JUDGE,
            name=obj_in.name,
            surname=obj_in.surname,
            phone=obj_in.phone,
            is_active=True,
            created_by_admin_id=admin_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, obj_in: UserUpdate) -> User:
        if obj_in.email:
            db_obj.email = obj_in.email
        if obj_in.role:
            db_obj.role = obj_in.role
        if obj_in.name:
            db_obj.name = obj_in.name
        if obj_in.surname:
            db_obj.surname = obj_in.surname
        if obj_in.phone is not None:
            db_obj.phone = obj_in.phone
        if obj_in.is_active is not None:
            db_obj.is_active = obj_in.is_active

        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.role == UserRole.ADMIN

    def is_head(self, user: User) -> bool:
        return user.role == UserRole.HEAD

    def is_judge(self, user: User) -> bool:
        return user.role == UserRole.JUDGE

    def remove(self, db: Session, user_id: uuid.UUID) -> Optional[User]:
        obj = db.query(User).get(user_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# Global instance
user = CRUDUser()
