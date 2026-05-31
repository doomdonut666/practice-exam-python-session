import pytest
import os
import tempfile
from datetime import datetime, timedelta
from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController

class TestControllers:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()
        
        self.task_ctrl = TaskController(self.db_manager)
        self.proj_ctrl = ProjectController(self.db_manager)
        self.user_ctrl = UserController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()
        os.unlink(self.temp_db.name)

    def test_full_workflow(self):
        user_id = self.user_ctrl.add_user("my_test_user", "mytestemail@gmail.com", "developer")
        assert user_id > 0

        start = datetime.now()
        end = start + timedelta(days=30)
        proj_id = self.proj_ctrl.add_project("Новый проект", "Описание", start, end)
        assert proj_id > 0

        due = start + timedelta(days=7)
        task_id = self.task_ctrl.add_task("Сделать бекенд", "Описание", 1, due, proj_id, user_id)
        assert task_id > 0

        user_tasks = self.user_ctrl.get_user_tasks(user_id)
        assert len(user_tasks) == 1
        assert user_tasks[0].id == task_id

        proj_tasks = self.task_ctrl.get_tasks_by_project(proj_id)
        assert len(proj_tasks) == 1

        self.task_ctrl.update_task_status(task_id, "completed")
        progress = self.proj_ctrl.get_project_progress(proj_id)
        assert progress == 100.0

    def test_overdue_tasks(self):
        proj_id = self.proj_ctrl.add_project("Проект", "Описание", datetime.now(), datetime.now())
        user_id = self.user_ctrl.add_user("my_test_user", "mytestemail@gmail.com", "developer")
        
        past_date = datetime.now() - timedelta(days=5)
        self.task_ctrl.add_task("Просрочка", "Текст", 1, past_date, proj_id, user_id)
        
        overdue = self.task_ctrl.get_overdue_tasks()
        assert len(overdue) == 1
        assert overdue[0].title == "Просрочка"