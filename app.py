import tkinter as tk
from tkinter import ttk
from equipment_tab import EquipmentTab
from software_tab import SoftwareTab
from employees_tab import EmployeesTab
from vendors_tab import VendorsTab
from purchases_tab import PurchasesTab
from maintenance_tab import MaintenanceTab

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Система управления инвентарём")
        self.geometry("800x600")

        tab_control = ttk.Notebook(self)

        equipment_tab = EquipmentTab(tab_control)
        software_tab = SoftwareTab(tab_control)
        employees_tab = EmployeesTab(tab_control)
        vendors_tab = VendorsTab(tab_control)
        purchases_tab = PurchasesTab(tab_control)
        maintenance_tab = MaintenanceTab(tab_control)

        tab_control.add(equipment_tab, text='Оборудование')
        tab_control.add(software_tab, text='Программное обеспечение')
        tab_control.add(employees_tab, text='Сотрудники')
        tab_control.add(vendors_tab, text='Поставщики')
        tab_control.add(purchases_tab, text='Закупки')
        tab_control.add(maintenance_tab, text='Обслуживание')

        tab_control.pack(expand=1, fill='both')