import tkinter as tk
from tkinter import ttk, messagebox
from app import InventoryApp

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Вход в систему")
        self.geometry("400x250")
        self.resizable(False, False)

        # Настройки основных цветов и стилей
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.primary_color = '#344955'
        self.secondary_color = '#232F34'
        self.accent_color = '#F9AA33'
        self.text_color = '#FFFFFF'

        # Настройка стилей
        self.setup_styles()

        # Создание виджетов
        self.create_widgets()

    def setup_styles(self):
        # Стиль для фреймов
        self.style.configure('My.TFrame', background=self.primary_color)

        # Стиль для кнопок
        self.style.configure('My.TButton',
                             font=('Helvetica', 12, 'bold'),
                             foreground=self.text_color,
                             background=self.accent_color,
                             borderwidth=0,
                             focuscolor=self.primary_color)
        self.style.map('My.TButton',
                       background=[('active', self.secondary_color)],
                       foreground=[('active', self.text_color)])

        # Стиль для меток и полей ввода
        self.style.configure('My.TLabel',
                             background=self.primary_color,
                             foreground=self.text_color,
                             font=('Helvetica', 12))
        self.style.configure('My.TEntry',
                             font=('Helvetica', 12))

    def create_widgets(self):
        # Создание основного фрейма
        main_frame = ttk.Frame(self, style='My.TFrame')
        main_frame.pack(expand=True, fill='both')

        # Заголовок
        title_label = ttk.Label(main_frame, text="Авторизация", style='My.TLabel', font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(20, 10))

        # Фрейм для ввода данных
        input_frame = ttk.Frame(main_frame, style='My.TFrame')
        input_frame.pack(pady=10, padx=20)

        # Имя пользователя
        username_label = ttk.Label(input_frame, text="Имя пользователя:", style='My.TLabel')
        username_label.grid(row=0, column=0, pady=10, sticky='e')
        self.username_entry = ttk.Entry(input_frame, style='My.TEntry')
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        # Пароль
        password_label = ttk.Label(input_frame, text="Пароль:", style='My.TLabel')
        password_label.grid(row=1, column=0, pady=10, sticky='e')
        self.password_entry = ttk.Entry(input_frame, show="*", style='My.TEntry')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        # Кнопка входа
        login_button = ttk.Button(main_frame, text="Войти", command=self.login, style='My.TButton')
        login_button.pack(pady=20)

        # Привязка Enter к кнопке входа
        self.bind('<Return>', lambda event: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Учетные данные здесь
        if username == "1" and password == "1":
            self.destroy()
            app = InventoryApp()
            app.mainloop()
        else:
            messagebox.showerror("Ошибка входа", "Неверное имя пользователя или пароль.")