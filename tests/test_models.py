import pytest
from datetime import datetime, timedelta
from models.task import Task
from models.project import Project
from models.user import User

class TestTaskModel:
    def test_task_creation(self):
        due_date = datetime.now() + timedelta(days=1)
        task = Task("Название", "Описание", 1, due_date, 1, 1)
        assert task.title == "Название"
        assert task.status == "pending"

    def test_task_validation(self):
        with pytest.raises(ValueError):
            Task("", "Описание", 1, datetime.now(), 1, 1)
        with pytest.raises(ValueError):
            Task("Название", "Описание", 5, datetime.now(), 1, 1)

    def test_task_update_status(self):
        task = Task("Название", "Описание", 1, datetime.now(), 1, 1)
        assert task.update_status("in_progress") == True
        assert task.status == "in_progress"
        assert task.update_status("invalid_status") == False

    def test_task_is_overdue(self):
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)
        
        task1 = Task("Просрочена", "Описание", 1, past_date, 1, 1)
        assert task1.is_overdue() == True
        
        task2 = Task("В норме", "Описание", 1, future_date, 1, 1)
        assert task2.is_overdue() == False

class TestProjectModel:
    def test_project_creation(self):
        start = datetime.now()
        end = datetime.now() + timedelta(days=10)
        project = Project("Проект", "Описание", start, end)
        assert project.name == "Проект"
        assert project.status == "active"

    def test_project_validation(self):
        with pytest.raises(ValueError):
            Project("", "Описание", datetime.now(), datetime.now())

    def test_project_get_progress(self):
        project = Project("Проект", "Описание", datetime.now(), datetime.now())
        assert project.get_progress() == 0.0
        
        task1 = Task("Задача 1", "", 1, datetime.now(), 1, 1)
        task1.status = "completed"
        task2 = Task("Задача 2", "", 1, datetime.now(), 1, 1)
        task2.status = "in_progress"
        
        project.tasks = [task1, task2]
        assert project.get_progress() == 50.0

class TestUserModel:
    def test_user_creation(self):
        user = User("my_test_user", "mytestemail@gmail.com", "developer")
        assert user.username == "my_test_user"
        
    def test_user_validation(self):
        with pytest.raises(ValueError):
            User("my_test_user", "invalid_email", "developer")
        with pytest.raises(ValueError):
            User("my_test_user", "mytestemail@gmail.com", "hacker")

    def test_user_update_info(self):
        user = User("my_test_user", "mytestemail@gmail.com", "developer")
        user.update_info(username="Petr", role="manager")
        assert user.username == "Petr"
        assert user.role == "manager"