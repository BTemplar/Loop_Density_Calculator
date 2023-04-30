# Программа для рассчета полотна по петельной пробе. Используется для упрощения процесса производства трикотажных изделий.

# Импортируем необходимые модули
import tkinter as tk
import math as mt
import datetime as dt
from tkinter import filedialog, messagebox


# функция для расчета плотности ширины
def Density_loops(width, loops):
    width_density = loops / width
    return width_density

# функция для расчета плотности высоты
def Density_lines(hight, lines):
    hight_density = lines / hight
    return hight_density

# функция для преобразования ширины плотности из см в петли
def Density_with(density_loops, width_piece):
    width_loops = density_loops * width_piece
    return width_loops

# функция для преобразования высоты плотности из см в ряды
def Density_hight(density_lines, hight_piece):
    hight_loops = density_lines * hight_piece
    return hight_loops


# класс для GUI
class App:
    def __init__(self, master):
        self.master = master
        
        # создание имен строк
        tk.Label(master, text="Ширина петельной пробы в см:").grid(row=0, column=0)
        tk.Label(master, text="Высота петельной пробы в см:").grid(row=1, column=0)
        tk.Label(master, text="Ширина петельной пробы в петлях:").grid(row=2, column=0)
        tk.Label(master, text="Высота петельной пробы в рядах:").grid(row=3, column=0)
        tk.Label(master, text="Ширина участка в см:").grid(row=4, column=0)
        tk.Label(master, text="Высота участка в см:").grid(row=5, column=0)
        tk.Label(master, text="Пряжа:").grid(row=6, column=0)
        tk.Label(master, text="Цвет:").grid(row=7, column=0)
        tk.Label(master, text="Производитель:").grid(row=8, column=0)
        tk.Label(master, text="Дата формирования:").grid(row=9, column=0)
        
        # создание полей ввода
        self.width_input = tk.Entry(master)
        self.hight_input = tk.Entry(master)
        self.loop_width_input = tk.Entry(master)
        self.lines_hight_input = tk.Entry(master)
        self.width_piece_input = tk.Entry(master)
        self.hight_piece_input = tk.Entry(master)
        self.yarn_input = tk.Entry(master)
        self.color_input = tk.Entry(master)
        self.producer_input = tk.Entry(master)
        self.date_input = tk.Entry(master)
        
        # настройки для вывода даты
        self.date_input.insert(0, dt.datetime.now().strftime("%d.%m.%Y"))

        
        # расположение форм ввода
        self.width_input.grid(row=0, column=1)
        self.hight_input.grid(row=1, column=1)
        self.loop_width_input.grid(row=2, column=1)
        self.lines_hight_input.grid(row=3, column=1)
        self.width_piece_input .grid(row=4, column=1)
        self.hight_piece_input.grid(row=5, column=1)
        self.yarn_input .grid(row=6, column=1)
        self.color_input.grid(row=7, column=1)
        self.producer_input.grid(row=8, column=1)
        self.date_input.grid(row=9, column=1)
        
        # создание кнопки рассчитать
        self.calculate_button = tk.Button(master, text="Рассчитать", command=self.calculate)
        self.calculate_button.grid(row=10, column=0, columnspan=2)
        
        # создание меню
        self.menu = tk.Menu(master)
        master.config(menu=self.menu)
        
        # созхдание команд в меню
        self.export_command = lambda: self.export_to_txt()
        self.about_command = lambda: self.about()
        self.menu.add_command(label="Сохранить в txt", command=self.export_command)
        self.menu.add_command(label="О программе", command=self.about_command)
        
        # создание отображения резульатата
        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=11, column=0, columnspan=2)
    
    # функция для расчета и вывода результата
    def calculate(self):
        # получаем значения переменных
        width = float(self.width_input.get())
        hight = float(self.hight_input.get())
        loop_width = float(self.loop_width_input.get())
        lines_hight = float(self.lines_hight_input.get())
        width_piece = float(self.width_piece_input.get())
        hight_piece = float(self.hight_piece_input.get())
        yarn = self.yarn_input.get()
        color = self.color_input.get()
        producer = self.producer_input.get()
        date = self.date_input.get()
        
        # рассчитываем плотность
        density_loops = Density_loops(width, loop_width)
        density_lines = Density_lines(hight, lines_hight)
        density_width = mt.ceil(Density_with(density_loops, width_piece))
        density_hight = mt.ceil(Density_hight(density_lines, hight_piece))
        
        # отображение результата
        self.result_label.configure(text='Ширина участка в петлях: ' + str(density_width) + '\n' + 'Высота участка в рядах: ' + str(density_hight))
    
    # фенкция для экспорта результатов в .txt файл
    def export_to_txt(self):
        # порлучаем результат в текстовом виде
        result = self.result_label.cget("text")
        if not result:
            messagebox.showerror("Ошибка", "Нечего экспортировать!\nЗаполните пустые поля и нажмите Рассчитать")
        else:
            # выбор расположения файла и присвоение ему имени
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'w') as f:
                    f.write("Пряжа: {}\nЦвет: {}\nПроизводитель: {}\nДата формирования: {}\n\n".format(self.yarn_input.get(), self.color_input.get(), self.producer_input.get(), self.date_input.get()))
                    f.write(result)
                    messagebox.showinfo("Экспорт", "Результаты успешно экспортированы в {}".format(file_path))
    
    # функция для вывода информации "О программе"
    def about(self):
        # создаем новое окно
        about_window = tk.Toplevel(self.master)
        about_window.title("О программе")
        
        # этот код создаёт окно с информацией о разработчике
        about_label = tk.Label(about_window, text="Программа для рассчета петельной пробы\n участка в целях создания детали изделия\n с последующей возможностью сохранения данных\nВерсия: 0.1\n Автор: Олег Рудь")
        about_label.pack(padx=20, pady=20)


# создание объекта tkinter и объекта приложения
root = tk.Tk()
root.title("Петельный калькулятор V 0.1")
app = App(root)
root.mainloop()