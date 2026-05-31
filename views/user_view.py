import tkinter as tk
from tkinter import ttk, messagebox

class UserView(ttk.Frame):
    def __init__(self, parent, user_controller) -> None:
        super().__init__(parent)
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_users()

    def create_widgets(self) -> None:
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(control_frame, text="Добавить пользователя", command=self.add_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Удалить выбранного", command=self.delete_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Обновить список", command=self.refresh_users).pack(side=tk.LEFT, padx=5)

        columns = ("id", "username", "email", "role")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Имя пользователя")
        self.tree.heading("email", text="Email")
        self.tree.heading("role", text="Роль")
        
        self.tree.column("id", width=50)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def refresh_users(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        users = self.user_controller.get_all_users()
        for user in users:
            self.tree.insert("", tk.END, values=(user.id, user.username, user.email, user.role))

    def add_user(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Новый пользователь")
        dialog.geometry("300x250")
        
        ttk.Label(dialog, text="Имя пользователя:").pack(pady=2)
        username_entry = ttk.Entry(dialog)
        username_entry.pack(pady=2)
        
        ttk.Label(dialog, text="Email:").pack(pady=2)
        email_entry = ttk.Entry(dialog)
        email_entry.pack(pady=2)
        
        ttk.Label(dialog, text="Роль:").pack(pady=2)
        role_combo = ttk.Combobox(dialog, values=["developer", "manager", "admin"], state="readonly")
        role_combo.set("developer")
        role_combo.pack(pady=2)

        def save():
            username = username_entry.get()
            email = email_entry.get()
            role = role_combo.get()
            
            try:
                self.user_controller.add_user(username, email, role)
                self.refresh_users()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def delete_selected(self) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите пользователя для удаления")
            return
            
        user_id = self.tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Подтверждение", f"Удалить пользователя ID {user_id}?"):
            self.user_controller.delete_user(user_id)
            self.refresh_users()