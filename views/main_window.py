# Главное окно приложения согласно README.md

import tkinter as tk
from tkinter import ttk

from views.project_view import ProjectView
from views.task_view import TaskView
from views.user_view import UserView

class MainWindow(tk.Tk):
    def __init__(self, task_controller, project_controller, user_controller) -> None:
        super().__init__()
        self.title("Система управления задачами")
        self.geometry("900x600")
        
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.task_tab = TaskView(
            self.notebook, 
            self.task_controller, 
            self.project_controller, 
            self.user_controller
        )
        self.project_tab = ProjectView(self.notebook, self.project_controller)
        self.user_tab = UserView(self.notebook, self.user_controller)

        self.notebook.add(self.task_tab, text="Задачи")
        self.notebook.add(self.project_tab, text="Проекты")
        self.notebook.add(self.user_tab, text="Пользователи")