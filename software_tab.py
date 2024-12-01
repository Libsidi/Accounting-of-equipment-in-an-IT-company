import tkinter as tk
from tkinter import ttk, messagebox, Menu, PhotoImage
from db_connection import get_connection

class SoftwareTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Инициализация подключения к базе данных
        try:
            self.conn = get_connection()
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось подключиться к базе данных: {e}")
            return

        # Настройки основных цветов и стилей
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.primary_color = '#344955'
        self.secondary_color = '#232F34'
        self.accent_color = '#F9AA33'
        self.text_color = '#FFFFFF'
        self.background_color = '#4A6572'

        # Загрузка иконок
        try:
            self.add_icon = PhotoImage(file='icons/add.png')
            self.delete_icon = PhotoImage(file='icons/delete.png')
            self.refresh_icon = PhotoImage(file='icons/refresh.png')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить иконки: {e}")
            # Если иконки не найдены, создадим пустые изображения
            self.add_icon = PhotoImage()
            self.delete_icon = PhotoImage()
            self.refresh_icon = PhotoImage()

        # Настройка стилей
        self.setup_styles()

        # Создание основного фрейма
        self.configure(style='My.TFrame')

        # Создание виджетов
        self.create_widgets()

        # Обновление данных
        self.refresh_data()

    def setup_styles(self):
        # Стиль для фреймов
        self.style.configure('My.TFrame', background=self.primary_color)

        # Стиль для Treeview
        self.style.configure("My.Treeview",
                             background="#EFEFEF",
                             foreground="black",
                             rowheight=25,
                             fieldbackground="#EFEFEF",
                             bordercolor=self.primary_color,
                             borderwidth=0)
        self.style.configure("My.Treeview.Heading",
                             background=self.secondary_color,
                             foreground=self.text_color,
                             bordercolor=self.primary_color,
                             font=('Helvetica', 11, 'bold'))
        self.style.map('My.Treeview', background=[('selected', self.accent_color)])

        # Стиль для кнопок
        self.style.configure('My.TButton',
                             font=('Helvetica', 10, 'bold'),
                             foreground=self.text_color,
                             background=self.accent_color,
                             borderwidth=0,
                             focuscolor=self.accent_color)
        self.style.map('My.TButton',
                       background=[('active', self.secondary_color)],
                       foreground=[('active', self.text_color)])

        # Стиль для меток и полей ввода
        self.style.configure('My.TLabel', background=self.primary_color, foreground=self.text_color, font=('Helvetica', 10))
        self.style.configure('My.TEntry', fieldbackground='#FFFFFF', foreground='black')

    def create_widgets(self):
        # Фрейм для таблицы с прокруткой
        tree_frame = ttk.Frame(self, style='My.TFrame')
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side='right', fill='y')

        columns = ('software_id', 'name', 'license_key', 'expiration_date', 'assigned_to')
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            style='My.Treeview',
            yscrollcommand=tree_scroll.set,
            selectmode='extended'
        )
        tree_scroll.config(command=self.tree.yview)

        # Настраиваем заголовки столбцов
        for col in columns:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_column(_col, False))
            self.tree.column(col, width=120)

        self.tree.pack(expand=True, fill='both')

        # Чередование цветов строк
        self.tree.tag_configure('oddrow', background='#FFFFFF')
        self.tree.tag_configure('evenrow', background='#E8E8E8')

        # Фрейм для кнопок
        btn_frame = ttk.Frame(self, style='My.TFrame')
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))

        # Кнопки с иконками
        refresh_btn = ttk.Button(btn_frame, text=" Обновить", image=self.refresh_icon, compound='left', command=self.refresh_data, style='My.TButton')
        refresh_btn.pack(side='left')

        add_btn = ttk.Button(btn_frame, text=" Добавить", image=self.add_icon, compound='left', command=self.add_record, style='My.TButton')
        add_btn.pack(side='left', padx=(10, 0))

        delete_btn = ttk.Button(btn_frame, text=" Удалить", image=self.delete_icon, compound='left', command=self.delete_record, style='My.TButton')
        delete_btn.pack(side='left', padx=(10, 0))

        # Создание контекстного меню
        self.create_context_menu()

        # Привязка событий
        self.tree.bind("<Button-3>", self.show_context_menu)  # ПКМ на элементе дерева

    def create_context_menu(self):
        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Удалить", command=self.delete_record)

    def show_context_menu(self, event):
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            self.tree.selection_set(selected_item)
            self.context_menu.tk_popup(event.x_root, event.y_root)
        else:
            pass  # Контекстное меню не показывается, если не выбрана строка
        self.context_menu.grab_release()

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = "SELECT * FROM software"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            count = 0
            for row in rows:
                tag = 'evenrow' if count % 2 == 0 else 'oddrow'
                self.tree.insert("", 'end', values=row, tags=(tag,))
                count += 1
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Удаление", "Пожалуйста, выберите запись для удаления.")
            return
        software_id = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранное ПО?")
        if confirm:
            query = "DELETE FROM software WHERE software_id = %s"
            try:
                self.cursor.execute(query, (software_id,))
                self.conn.commit()
                self.refresh_data()
                messagebox.showinfo("Успех", "ПО успешно удалено.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить запись: {e}")

    def add_record(self):
        add_window = tk.Toplevel(self)
        add_window.title("Добавить программное обеспечение")
        add_window.geometry("400x350")
        add_window.resizable(False, False)
        add_window.configure(background=self.primary_color)

        frame = ttk.Frame(add_window, style='My.TFrame')
        frame.pack(expand=True, fill='both', padx=20, pady=20)

        labels = ["Название:", "Лицензионный ключ:", "Дата истечения лицензии (ГГГГ-ММ-ДД):", "ID сотрудника (назначено):"]
        entries = []

        for idx, label_text in enumerate(labels):
            ttk.Label(frame, text=label_text, style='My.TLabel').grid(row=idx, column=0, sticky='e', padx=(0, 10), pady=(10, 10))
            entry = ttk.Entry(frame, width=30, style='My.TEntry')
            entry.grid(row=idx, column=1)
            entries.append(entry)

        def save_new_record():
            name = entries[0].get()
            license_key = entries[1].get()
            expiration_date = entries[2].get()
            assigned_to = entries[3].get()

            if not name or not license_key:
                messagebox.showwarning("Предупреждение", "Пожалуйста, заполните обязательные поля.")
                return

            try:
                query = """
                INSERT INTO software (name, license_key, expiration_date, assigned_to)
                VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(query, (name, license_key, expiration_date or None, assigned_to or None))
                self.conn.commit()
                messagebox.showinfo("Успех", "Программное обеспечение успешно добавлено.")
                add_window.destroy()
                self.refresh_data()
            except Exception as err:
                messagebox.showerror("Ошибка", f"Не удалось добавить запись: {err}")

        save_btn = ttk.Button(frame, text="Сохранить", command=save_new_record, style='My.TButton')
        save_btn.grid(row=len(labels), column=0, columnspan=2, pady=(20, 0))

    def sort_column(self, col, reverse):
        data_list = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        # Сортировка с учётом типов данных
        if col == 'software_id':
            data_list.sort(key=lambda x: int(x[0]), reverse=reverse)
        else:
            data_list.sort(key=lambda x: x[0], reverse=reverse)

        # Ресортируем данные
        for index, (val, child) in enumerate(data_list):
            self.tree.move(child, '', index)

        # Меняем порядок сортировки при следующем клике
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))