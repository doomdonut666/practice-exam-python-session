from datetime import datetime
import re

class User:
    def __init__(self, username, email, role) -> None:
        if not isinstance(username, str) or not username.strip():
            raise ValueError("Имя пользователя (username) должно быть непустой строкой.")
        if role not in ('admin', 'manager', 'developer'):
            raise ValueError("Роль (role) должна быть 'admin', 'manager' или 'developer'.")

        if not self._is_valid_email(email):
            raise ValueError("Некорректный формат email.")
        
        self.id = None  # ID будет назначен при сохранении в БД
        self.username = username
        self.email = email
        self.role = role
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        if not isinstance(email, str):
            return False

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))

    def update_info(self, username=None, email=None, role=None) -> None:
        if username is not None:
            if not isinstance(username, str) or not username.strip():
                raise ValueError("Имя пользователя должно быть непустой строкой")
            self.username = username
            
        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Некорректный формат email")
            self.email = email
            
        if role is not None:
            if role not in ('admin', 'manager', 'developer'):
                raise ValueError("Недопустимая роль")
            self.role = role

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'registration_date': self.registration_date.isoformat() if self.registration_date else None
        }
