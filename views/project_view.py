import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ProjectView(ttk.Frame):
    def __init__(self, parent, project_controller) -> None:
        super().__init__(parent)
        self.project_controller = project_controller
        self.create_widgets()
        self.refresh_projects()

    def create_widgets(self) -> None:
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Добавить проект", command=self.add_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Удалить выбранный", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Обновить список", command=self.refresh_projects).pack(side=tk.LEFT, padx=5)

        columns = ("id", "name", "status", "start_date", "progress")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("status", text="Статус")
        self.tree.heading("start_date", text="Дата начала")
        self.tree.heading("progress", text="Прогресс (%)")
        
        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def refresh_projects(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        projects = self.project_controller.get_all_projects()
        for project in projects:
            progress = self.project_controller.get_project_progress(project.id)
            self.tree.insert("", tk.END, values=(
                project.id, project.name, project.status, 
                project.start_date.strftime("%Y-%m-%d"), f"{progress:.1f}"
            ))

    def add_project(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Новый проект")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Название:").pack(pady=2)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=2)

        def save():
            name = name_entry.get()
            if not name:
                messagebox.showerror("Ошибка", "Название не может быть пустым")
                return
            
            start_date = datetime.now()
            end_date = datetime.now() # Упрощенно для примера
            self.project_controller.add_project(name, "Описание проекта", start_date, end_date)
            self.refresh_projects()
            dialog.destroy()

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def delete_selected(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите проект для удаления")
            return
            
        project_id = self.tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Подтверждение", f"Удалить проект ID {project_id}?"):
            self.project_controller.delete_project(project_id)
            self.refresh_projects()