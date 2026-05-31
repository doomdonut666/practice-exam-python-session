from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название задачи (title) должно быть непустой строкой.")
        if not isinstance(priority, int) or priority not in (1, 2, 3):
            raise ValueError("Приоритет (priority) должен быть целым числом: 1 (высокий), 2 (средний) или 3 (низкий).")
        if not isinstance(due_date, datetime):
            raise ValueError("Срок выполнения (due_date) должен быть объектом datetime.")

        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.status = 'pending'
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        valid_statuses = ('pending', 'in_progress', 'completed')
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False

    def is_overdue(self) -> bool:
        if self.status == 'completed':
            return False
        return datetime.now() > self.due_date

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'project_id': self.project_id,
            'assignee_id': self.assignee_id
        }
