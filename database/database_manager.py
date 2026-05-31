import sqlite3
from models.task import Task
from models.project import Project
from models.user import User
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("PRAGMA foreign_keys = ON;")

    def close(self) -> None:
        if self.conn:
            self.conn.close()

    def create_tables(self) -> None:
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT NOT NULL,
                    registration_date TEXT NOT NULL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    start_date TEXT NOT NULL,
                    end_date TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    project_id INTEGER,
                    assignee_id INTEGER,
                    FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
                    FOREIGN KEY(assignee_id) REFERENCES users(id) ON DELETE SET NULL
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Произошла ошибка при создании таблиц: {e}")

    # Tasks
    def add_task(self, task: Task) -> int:
        try:
            query = """
                INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                task.title, task.description, task.priority, task.status, 
                task.due_date.isoformat(), task.project_id, task.assignee_id
            ))
            self.conn.commit()
            task.id = self.cursor.lastrowid
            return task.id
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении задачи: {e}")
            return -1

    def get_task_by_id(self, task_id) -> Task | None:
        try:
            self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = self.cursor.fetchone()
            if row:
                due_date = datetime.fromisoformat(row['due_date'])
                task = Task(row['title'], row['description'], row['priority'], due_date, row['project_id'], row['assignee_id'])
                task.id = row['id']
                task.status = row['status']
                return task
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении задачи: {e}")
        return None

    def get_all_tasks(self) -> list[Task]:
        tasks = []
        try:
            self.cursor.execute("SELECT * FROM tasks")
            for row in self.cursor.fetchall():
                due_date = datetime.fromisoformat(row['due_date'])
                task = Task(row['title'], row['description'], row['priority'], due_date, row['project_id'], row['assignee_id'])
                task.id = row['id']
                task.status = row['status']
                tasks.append(task)
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении всех задач: {e}")
        return tasks

    def update_task(self, task_id, **kwargs) -> bool:
        if not kwargs:
            return False
            
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(f"{key} = ?")
            values.append(value.isoformat() if isinstance(value, datetime) else value)
            
        values.append(task_id)
        query = f"UPDATE tasks SET {', '.join(columns)} WHERE id = ?"
        
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Произошла ошибка при обновлении задачи: {e}")
            return False

    def delete_task(self, task_id) -> bool:
        try:
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Произошла ошибка при удалении задачи: {e}")
            return False

    def search_tasks(self, query) -> list[Task]:
        tasks = []
        try:
            search_pattern = f"%{query}%"
            self.cursor.execute("""
                SELECT * FROM tasks 
                WHERE title LIKE ? OR description LIKE ?
            """, (search_pattern, search_pattern))
            for row in self.cursor.fetchall():
                due_date = datetime.fromisoformat(row['due_date'])
                task = Task(row['title'], row['description'], row['priority'], due_date, row['project_id'], row['assignee_id'])
                task.id = row['id']
                task.status = row['status']
                tasks.append(task)
        except sqlite3.Error as e:
            print(f"Произошла ошибка при поиске задач: {e}")
        return tasks

    def get_tasks_by_project(self, project_id) -> list[Task]:
        tasks = []
        try:
            self.cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
            for row in self.cursor.fetchall():
                due_date = datetime.fromisoformat(row['due_date'])
                task = Task(row['title'], row['description'], row['priority'], due_date, row['project_id'], row['assignee_id'])
                task.id = row['id']
                task.status = row['status']
                tasks.append(task)
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении задач проекта: {e}")
        return tasks

    def get_tasks_by_user(self, user_id) -> list[Task]:
        tasks = []
        try:
            self.cursor.execute("SELECT * FROM tasks WHERE assignee_id = ?", (user_id,))
            for row in self.cursor.fetchall():
                due_date = datetime.fromisoformat(row['due_date'])
                task = Task(row['title'], row['description'], row['priority'], due_date, row['project_id'], row['assignee_id'])
                task.id = row['id']
                task.status = row['status']
                tasks.append(task)
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении задач пользователя: {e}")
        return tasks

    # Projects
    def add_project(self, project: Project) -> int:
        try:
            query = """
                INSERT INTO projects (name, description, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                project.name, project.description, 
                project.start_date.isoformat(), project.end_date.isoformat(), 
                project.status
            ))
            self.conn.commit()
            project.id = self.cursor.lastrowid
            return project.id
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении проекта: {e}")
            return -1

    def get_project_by_id(self, project_id) -> Project | None:
        try:
            self.cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            row = self.cursor.fetchone()
            if row:
                start_date = datetime.fromisoformat(row['start_date'])
                end_date = datetime.fromisoformat(row['end_date'])
                project = Project(row['name'], row['description'], start_date, end_date)
                project.id = row['id']
                project.status = row['status']
                return project
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении проекта: {e}")
        return None

    def get_all_projects(self) -> list[Project]:
        projects = []
        try:
            self.cursor.execute("SELECT * FROM projects")
            for row in self.cursor.fetchall():
                start_date = datetime.fromisoformat(row['start_date'])
                end_date = datetime.fromisoformat(row['end_date'])
                project = Project(row['name'], row['description'], start_date, end_date)
                project.id = row['id']
                project.status = row['status']
                projects.append(project)
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении всех проектов: {e}")
        return projects

    def update_project(self, project_id, **kwargs) -> bool:
        if not kwargs:
            return False
            
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(f"{key} = ?")
            values.append(value.isoformat() if isinstance(value, datetime) else value)
            
        values.append(project_id)
        query = f"UPDATE projects SET {', '.join(columns)} WHERE id = ?"
        
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Произошла ошибка при обновлении проекта: {e}")
            return False

    def delete_project(self, project_id) -> bool:
        try:
            self.cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Произошла ошибка при удалении проекта: {e}")
            return False

    # User
    def add_user(self, user: User) -> int:
        try:
            query = """
                INSERT INTO users (username, email, role, registration_date)
                VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                user.username, user.email, user.role, 
                user.registration_date.isoformat() if user.registration_date else datetime.now().isoformat()
            ))
            self.conn.commit()
            user.id = self.cursor.lastrowid
            return user.id
        except sqlite3.Error as e:
            print(f"Произошла ошибка при добавлении пользователя: {e}")
            return -1

    def get_user_by_id(self, user_id) -> User | None:
        try:
            self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = self.cursor.fetchone()
            if row:
                user = User(row['username'], row['email'], row['role'])
                user.id = row['id']
                user.registration_date = datetime.fromisoformat(row['registration_date'])
                return user
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении пользователя: {e}")
        return None

    def get_all_users(self) -> list[User]:
        users = []
        try:
            self.cursor.execute("SELECT * FROM users")
            for row in self.cursor.fetchall():
                user = User(row['username'], row['email'], row['role'])
                user.id = row['id']
                user.registration_date = datetime.fromisoformat(row['registration_date'])
                users.append(user)
        except sqlite3.Error as e:
            print(f"Произошла ошибка при получении всех пользователей: {e}")
        return users

    def update_user(self, user_id, **kwargs) -> bool:
        if not kwargs:
            return False
            
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(f"{key} = ?")
            values.append(value.isoformat() if isinstance(value, datetime) else value)
            
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(columns)} WHERE id = ?"
        
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Произошла ошибка при обновлении пользователя: {e}")
            return False

    def delete_user(self, user_id) -> bool:
        try:
            self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Произошла ошибка при удалении пользователя: {e}")
            return False