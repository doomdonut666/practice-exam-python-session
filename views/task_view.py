import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TaskView(ttk.Frame):
    def __init__(self, parent, task_controller, project_controller, user_controller) -> None:
        super().__init__(parent)
        self.task_controller = task_controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        
        self.create_widgets()
        self.refresh_tasks()

    def create_widgets(self) -> None:
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Добавить задачу", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Удалить выбранную", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Обновить список", command=self.refresh_tasks).pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.search_var, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Поиск", command=self.refresh_tasks).pack(side=tk.LEFT, padx=5)

        columns = ("id", "title", "priority", "status", "due_date")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Название")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("status", text="Статус")
        self.tree.heading("due_date", text="Срок")
        
        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def refresh_tasks(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        search_query = self.search_var.get()
        if search_query:
            tasks = self.task_controller.search_tasks(search_query)
        else:
            tasks = self.task_controller.get_all_tasks()
            
        for task in tasks:
            self.tree.insert("", tk.END, values=(task.id, task.title, task.priority, task.status, task.due_date.strftime("%Y-%m-%d")))

    def add_task(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Новая задача")
        dialog.geometry("300x250")
        
        ttk.Label(dialog, text="Название:").pack(pady=2)
        title_entry = ttk.Entry(dialog)
        title_entry.pack(pady=2)
        
        ttk.Label(dialog, text="Приоритет (1-3):").pack(pady=2)
        priority_entry = ttk.Entry(dialog)
        priority_entry.pack(pady=2)

        def save():
            try:
                title = title_entry.get()
                priority = int(priority_entry.get())
                due_date = datetime.now()
                self.task_controller.add_task(title, "Описание", priority, due_date, None, None)
                self.refresh_tasks()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Проверьте введенные данные!")

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def delete_selected(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления")
            return
            
        task_id = self.tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Подтверждение", f"Удалить задачу ID {task_id}?"):
            self.task_controller.delete_task(task_id)
            self.refresh_tasks()