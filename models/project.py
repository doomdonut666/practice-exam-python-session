from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название проекта (name) должно быть непустой строкой")
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError("Даты должны быть объектами datetime")

        self.id = None  # ID назначается при сохранении в базу данных
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = 'active'  # Статус по умолчанию

    def update_status(self, new_status) -> bool:
        valid_statuses = ('active', 'completed', 'on_hold')
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False

    def get_progress(self) -> float:
        if hasattr(self, 'tasks') and isinstance(self.tasks, list) and self.tasks:
            completed_tasks = sum(1 for task in self.tasks if getattr(task, 'status', '') == 'completed')
            return (completed_tasks / len(self.tasks)) * 100.0
        return 0.0

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status
        }