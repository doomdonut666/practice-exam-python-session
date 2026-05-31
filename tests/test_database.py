import pytest
import os
import tempfile
from datetime import datetime, timedelta
from database.database_manager import DatabaseManager
from models.project import Project
from models.user import User
from models.task import Task

class TestDatabaseManager:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db = DatabaseManager(self.temp_db.name)
        self.db.create_tables()

    def teardown_method(self):
        self.db.close()
        os.unlink(self.temp_db.name)

    def test_create_tables(self):
        self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in self.db.cursor.fetchall()]
        assert "users" in tables
        assert "projects" in tables
        assert "tasks" in tables

    def test_project_cascade_delete(self):
        p = Project("Проект", "Оп", datetime.now(), datetime.now())
        p_id = self.db.add_project(p)
        
        t = Task("Задача", "Оп", 1, datetime.now(), p_id, None)
        t_id = self.db.add_task(t)
        
        assert len(self.db.get_all_tasks()) == 1
        self.db.delete_project(p_id)
        assert len(self.db.get_all_tasks()) == 0

    def test_user_set_null_on_delete(self):
        u = User("my_test_user", "mytestemail@gmail.com", "developer")
        u_id = self.db.add_user(u)
        
        t = Task("Задача", "Оп", 1, datetime.now(), None, u_id)
        t_id = self.db.add_task(t)
        
        self.db.delete_user(u_id)
        
        task_from_db = self.db.get_task_by_id(t_id)
        assert task_from_db.assignee_id is None

    def test_search_tasks(self):
        t1 = Task("Написать автотесты", "Тесты для БД", 1, datetime.now(), None, None)
        t2 = Task("Сделать рефакторинг", "Важная задача", 2, datetime.now(), None, None)
        self.db.add_task(t1)
        self.db.add_task(t2)
        
        results = self.db.search_tasks("автотесты")
        assert len(results) == 1
        assert results[0].title == "Написать автотесты"
        
        results2 = self.db.search_tasks("Важная")
        assert len(results2) == 1
        assert results2[0].title == "Сделать рефакторинг"