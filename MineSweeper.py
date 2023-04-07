import tkinter as tk  # импортируем tkinter
from random import shuffle  # позволяет перемешивать коллекции
from tkinter.messagebox import showinfo, showerror  # для показа сообщений пользователям

# словарь для цветов цифр на игровом поле по кодам HEX
colors = {
    1: 'blue', 2: 'green', 3: 'red', 4: '#4245f5', 5: 'brown', 6: '#42f5e3', 7: 'black', 8: '#f54242', 0: 'white'
}


# Класс - набор объединенных функций
# Функции внутри класса называются методы
class MyButton(tk.Button):
    """ Наследует класс Button из tkinter """
    # Теперь классу MyButton доступны все методы класса tk.Button

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        """
        Метод __init __ вызывается, когда создается объект.
        Инициализация начального состояния объекта.
        """
        # number - номер кнопки (из счетчика count), по умолчанию 0
        # x, y - координаты кнопки,
        # *args, **kwargs - любые значения, которые могут понадобиться для определенной кнопки
        # (например, width, font и т.д.)

        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        # вызываем метод init родительского класса (tk.Button) для того, чтобы создалась изначальная кнопка,
        # потом у нее уже будем определять аттрибуты x и y
        # указываем ширину кнопки (width) и шрифт для текста внутри кнопки (шрифт Calibri, размер 15, жирный)
        self.x = x  # присваиваем координаты
        self.y = y  # присваиваем координаты
        self.number = number  # присваиваем номер кнопки
        self.is_mine = False  # мина кнопка или нет, по умолчанию все кнопки не мины
        self.count_bomb = 0  # количество мин среди соседей, по умолчанию 0
        self.is_open = False  # открывали кнопку или нет, по умолчанию все кнопки не открыты

    def __repr__(self):
        """ Выводит на экран консоли все атрибуты кнопки"""
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'


class MineSweeper:

    window = tk.Tk()  # создаем окно
    ROWS = 10  # переменная для количества строк
    COLUMNS = 7  # переменная для количества столбцов
    MINES = 15  # переменная для количества мин
    IS_GAME_OVER = False  # закончена игра или нет, по умолчанию нет
    IS_FIRST_CLICK = True  # для расстановки бомб на поле только после первого клика
    # исключаем возможность при первом клике сразу попасть на бомбу и закончить игру

    def __init__(self):
        """
        Определяет кнопки на игровом поле, включая барьерные.
        Барьерные кнопки нужны для того, чтобы у каждой кнопки было по 8 соседей,
        включая кнопки по краям поля (у которых либо 5, либо 3 соседа).
        """
        # Переопределяем метод init (т.к. он уже определен в tkinter)
        # метод автоматически запускается, когда запускаем класс

        self.buttons = []  # пустой список для хранения кнопок (игровое поле)
        # к экземпляру класса обращаемся через self

        # цикл для генерации списка кнопок
        # обращаемся к переменной через имя класса
        for i in range(MineSweeper.ROWS + 2):  # перебираем количество строк (+2 для барьерных кнопок)

            temp = []  # временный список

            for j in range(MineSweeper.COLUMNS + 2):  # перебираем количество столбцов (+2 для барьерных кнопок)
                # создаем кнопку в окне (вызываем из класса MyButton),
                # присваиваем координаты (x = i (строки), y = j (столбцы))
                btn = MyButton(MineSweeper.window, x=i, y=j)
                # command отвечает за обработку кнопок
                # создаем анонимную функцию, которая принимает переменную и вызывает клик от этой переменной
                btn.config(command=lambda button=btn: self.click(button))
                # bind вызывает функцию при определенном событии, Button-3 - нажатие правой кнопкой мыши
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)  # добавляем кнопку во временный список

            self.buttons.append(temp)  # добавляем в итоговый список с кнопками

    def right_click(self, event):
        """
        Определяет действия при нажатии правой кнопкой мыши.
        Позволяет отмечать предполагаемые мины на поле.
        """
        if MineSweeper.IS_GAME_OVER:  # чтобы нельзя было ставить и снимать флажки, когда игра закончена
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':  # по умолчанию все кнопки в event в состоянии normal
            cur_btn['state'] = 'disabled'  # меняем состояние
            cur_btn['text'] = '🚩'  # меняем текст на символ отметки мины
            cur_btn['disabledforeground'] = 'red'  # меняем цвет флажка на красный
        elif cur_btn['text'] == '🚩':  # обратный процесс - снимаем флажок с кнопки
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    def click(self, clicked_button: MyButton):
        """ Определяет действия при нажатии кнопки """
        # Создаем в классе MineSweeper, а не в MyButton, т.к. должна быть информация про соседние кнопки,
        # а в классе MyButton такой информации нет
        # принимает на вход нажатую кнопку (clicked_button)
        # указываем тип объекта, который ожидаем (MyButton)

        if MineSweeper.IS_GAME_OVER:  # чтобы нельзя было нажимать кнопки после проигрыша
            return

        if MineSweeper.IS_FIRST_CLICK:  # если первый клик, то далее действуем:
            self.insert_mines(clicked_button.number)  # расставляем мины
            self.count_mines_in_buttons()  # считаем количество мин среди соседей
            self.print_buttons()  # выводим кнопки
            MineSweeper.IS_FIRST_CLICK = False  # указываем, что первый клик уже был

        if clicked_button.is_mine:  # если нажали на мину, то далее действуем:
            # текст на кнопке устанавливаем '*', меняем фон на красный, цвет шрифта для * черный (disabledforeground)
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True  # меняем аттрибут is_open на True (кнопку уже открыли)
            MineSweeper.IS_GAME_OVER = True  # конец игры, т.к. нажали на бомбу
            showinfo('Game Over', 'Вы проиграли!')  # показ сообщения пользователю

            # ниже цикл для показа пользователю после проигрыша, где были мины
            for i in range(1, MineSweeper.ROWS + 1):  # i - номер строки
                for j in range(1, MineSweeper.COLUMNS + 1):  # j - номер столбца
                    # начинаем с 1 (т.к. 0 - барьерная кнопка)
                    # +2 меняем на +1, т.к. последняя тоже барьерная кнопка
                    btn = self.buttons[i][j]  # указываем координаты кнопки (номер строки и столбца)
                    if btn.is_mine:  # если кнопка - мина, показываем *
                        btn['text'] = '*'
        else:  # если нажали не на мину, то далее действуем:
            color = colors.get(clicked_button.count_bomb)  # получаем значение ключа из словаря color
            if clicked_button.count_bomb:  # если есть мины среди соседей
                # текст - сколько мин среди соседей
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True  # меняем атрибут is_open на True (кнопку уже открывали)
            else:  # если нет мин среди соседей, обращаемся к методу "поиск в ширину"
                self.breadth_first_search(clicked_button)  # для открытия соседних пустых кнопок
        # меняем конфигурацию кнопки
        clicked_button.config(state='disabled')  # теперь нельзя второй раз нажать на кнопку
        clicked_button.config(relief=tk.SUNKEN)  # выделяем кнопку как "нажатую"

    def breadth_first_search(self, btn: MyButton):
        """
        Поиск в ширину (для открытия соседних пустых кнопок в том случае,
        если нажали на пустую кнопку (не мина и нет мин среди соседей)
        """
        queue = [btn]  # список кнопок, которые нужно проверить на предмет мин или цифр количества мин рядом
        # пока в списке кнопка, которую нажали
        # нужно проверить всех соседей нажатой кнопки и их соседей, если эти кнопки пустые
        while queue:  # пока есть кнопки в списке для проверки
            cur_btn = queue.pop()  # из очереди достаем кнопку для проверки
            # Метод pop() возвращает элемент из списка и удаляет его в списке
            color = colors.get(cur_btn.count_bomb, 'black')  # получаем значение ключа из словаря color
            if cur_btn.count_bomb:  # если проверяемая кнопка имеет бомбы среди соседних кнопок
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)  # текст - сколько мин среди соседей
            else:  # если бомб нет
                cur_btn.config(text='', disabledforeground=color)  # пустой текст

            cur_btn.is_open = True  # меняем атрибут is_open на True (кнопку уже открывали)
            cur_btn.config(state='disabled')  # теперь нельзя второй раз нажать на кнопку
            cur_btn.config(relief=tk.SUNKEN)  # выделяем кнопку как "нажатую"
            # после того как обработали кнопку, нужно посмотреть на ее соседей по горизонтали и вертикали
            if cur_btn.count_bomb == 0:  # только для той кнопки, которая не имеет бомб среди соседей
                x, y = cur_btn.x, cur_btn.y  # в x, y записываем координаты текущей кнопки
                for dx in [-1, 0, 1]:  # координаты всех соседей по x
                    for dy in [-1, 0, 1]:  # координаты всех соседей по y
                        next_btn = self.buttons[x + dx][y + dy]  # получаем координаты следующей кнопки
                        if not next_btn.is_open and \
                                1 <= next_btn.x <= MineSweeper.ROWS and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and \
                                next_btn not in queue:
                            # если кнопка еще не была открыта и она не является барьерной
                            # и уже не стоит в очереди на проверку
                            queue.append(next_btn)  # добавляем в очередь на проверку

    def reload(self):
        """ Перезапускает игру """
        # вызываем метод destroy для всех дочерних элементов окна
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()  # формируем новые кнопки
        self.create_widgets()  # отрисовка новых кнопок
        MineSweeper.IS_FIRST_CLICK = True  # Возвращаем параметр в True (т.к. уже нажимали кнопку)
        MineSweeper.IS_GAME_OVER = False  # если reload запустится после окончания игры

    def create_settings_win(self):
        """ Создает меню игры """
        win_settings = tk.Toplevel(self.window)  # дочернее окно, передаем, к какому окну оно будет относиться
        win_settings.wm_title('Настройки')  # добавляем заголовок
        # создаем лейблы для меню, указываем текст и где находится (в grid)
        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)  # отвечает за ряды
        row_entry.insert(0, MineSweeper.ROWS)  # индекс, куда расположить, и содержимое
        row_entry.grid(row=0, column=1, padx=20, pady=20)  # расположение, отступы по x и y
        # создаем лейблы для меню, указываем текст и где находится (в grid)
        tk.Label(win_settings, text='Количество столбцов').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)  # отвечает за столбцы
        column_entry.insert(0, MineSweeper.COLUMNS)  # индекс, куда расположить, и содержимое
        column_entry.grid(row=1, column=1, padx=20, pady=20)  # расположение, отступы по x и y
        # создаем лейблы для меню, указываем текст и где находится (в grid)
        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)  # отвечает за мины
        mines_entry.insert(0, MineSweeper.MINES)  # индекс, куда расположить, и содержимое
        mines_entry.grid(row=2, column=1, padx=20, pady=20)  # расположение, отступы по x и y
        # создаем кнопку для применения изменений в игре
        save_btn = tk.Button(win_settings, text='Применить',
                  command=lambda: self.change_settings(row_entry, column_entry, mines_entry))
        # располагаем по центру 3го ряда, columnspan - объединяем 2 столбца
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        """
        Меняет настройки игры (количество строк, столбцов и мин),
        введенные пользователем в меню настроек.
        """
        # передаем строку, столбец и мины для полей ввода
        try:
            int(row.get()), int(column.get()), int(mines.get())  # преобразуем введенные значения в числа
        except:
            showerror('Ошибка', 'Вы ввели неправильное значение!')  # показ ошибки, если введены не числа
            return  # выход
        MineSweeper.ROWS = int(row.get())  # передаем в ROW число строк (int) из поля ввода
        MineSweeper.COLUMNS = int(column.get())  # передаем число столбцов (int) из поля ввода
        MineSweeper.MINES = int(mines.get())  # передаем число мин (int) из поля ввода
        self.reload()  # после изменения настроек делаем перезапуск игры

    def create_widgets(self):
        """ Размещает кнопки на игровом поле и меню игры """
        menubar = tk.Menu(self.window)  # создаем меню, прикрепляем к окну
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)  # создаем подменю, tearoff - удаляем строчку с тире в подменю
        # ниже кнопки в подменю
        settings_menu.add_command(label='Играть', command=self.reload)  # перезапуск игры при нажатии 'Играть'
        settings_menu.add_command(label='Настройки', command=self.create_settings_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)  # выход из игры при нажатии Выход
        menubar.add_cascade(label='Файл', menu=settings_menu)  # объединяем в каскад под именем Файл

        count = 1  # счетчик
        for i in range(1, MineSweeper.ROWS + 1):  # i - номер строки
            for j in range(1, MineSweeper.COLUMNS + 1):  # j - номер столбца
                # начинаем с 1 (т.к. 0 - барьерная кнопка)
                # +2 меняем на +1, т.к. последняя тоже барьерная кнопка                
                btn = self.buttons[i][j]  # указываем координаты кнопки (номер строки и столбца)
                btn.number = count  # назначаем кнопке номер
                # размещаем кнопку на игровом поле
                # stick - растянуть кнопки по сторонам света (North, South, West, East)
                # на тот случай, если пользователь увеличивает размер поля
                btn.grid(row=i, column=j, stick='NSWE')
                count += 1  # с каждой кнопкой count увеличивается на 1

        for i in range(1, MineSweeper.ROWS + 1):  # i - номер строки
            # аттрибут Grid, метод rowconfigure - настройка размера строки
            # передаем, где находится строка, номер строки (переменная i), какой будет вес у строки (weight)
            # (это пропорция строки по отношению к другим)
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, MineSweeper.COLUMNS + 1):  # j - номер столбца
            # аттрибут Grid, метод columnconfigure - настройка размера столбца
            # передаем, где находится столбец, номер столбца (переменная j), какой будет вес у столбца (weight)
            # (это пропорция столбца по отношению к другим)
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def open_all_buttons(self):
        """ Открывает все кнопки на поле """
        for i in range(MineSweeper.ROWS + 2):  # i - номер строки, +2 для барьерных кнопок
            for j in range(MineSweeper.COLUMNS + 2):  # j - номер столбца, +2 для барьерных кнопок
                btn = self.buttons[i][j]  # указываем координаты кнопки (номер строки и столбца)
                if btn.is_mine:  # если кнопка - мина
                    # текст на кнопке *, меняем фон на красный, цвет шрифта черный (disabledforeground)
                    btn.config(text='*', background='red', disabledforeground='black')
                # если кол-во бомб среди соседей, есть среди ключей в словаре colors (чтобы не выводился 0)
                elif btn.count_bomb in colors:
                    color = colors.get(btn.count_bomb)  # получаем значение ключа
                    btn.config(text=btn.count_bomb, fg=color)  # текст - номер кнопки + устанавливаем цвет

    def start(self):
        """ Запускает игру """
        self.create_widgets()  # создаем виджеты
        MineSweeper.window.mainloop()  # выводим окно (mainloop - обработчик событий)
        # размер окна зависит от переменных ROW и COLUMNS (подбирается автоматически)      

    def print_buttons(self):
        """ Выводит атрибуты кнопок на экран """
        for i in range(1, MineSweeper.ROWS + 1):
            # i - номер строки, начинаем с 1 (т.к. 0 - барьерная кнопка)
            # +1, т.к. последняя тоже барьерная кнопка
            for j in range(1, MineSweeper.COLUMNS + 1):
                # j - номер столбца, начинаем с 1 (т.к. 0 - барьерная кнопка)
                # +1, т.к. последняя тоже барьерная кнопка
                btn = self.buttons[i][j]  # указываем координаты кнопки (номер строки и столбца)
                if btn.is_mine:  # если кнопка - мина
                    print('B', end='')  # выводим B, убираем перенос строк
                else:  # если не мина
                    print(btn.count_bomb, end='')  # выводим сколько мин вокруг, убираем перенос строк
            print()  # добавляем пустой принт для разбиения вывода по строкам

    def insert_mines(self, number: int):
        """ Располагает мины на поле """
        index_mines = self.get_mines_places(number)  # получаем индексы для мин
        print(index_mines)
        for i in range(1, MineSweeper.ROWS + 1):
            # i - номер строки, начинаем с 1 (т.к. 0 - барьерная кнопка)
            # +1, т.к. последняя тоже барьерная кнопка
            for j in range(1, MineSweeper.COLUMNS + 1):
                # j - номер столбца, начинаем с 1 (т.к. 0 - барьерная кнопка)
                # +1, т.к. последняя тоже барьерная кнопка
                btn = self.buttons[i][j]  # указываем координаты кнопки (номер строки и столбца)
                if btn.number in index_mines:  # если номер кнопки в списке индексов мин
                    btn.is_mine = True  # меняем аттрибут кнопки is_mine с False на True
        # в итоге номера присваиваются всем кнопкам, кроме барьерных (по краям поля)

    def count_mines_in_buttons(self):
        """ Находит количество мин среди соседей для каждой кнопки-не мины """
        for i in range(1, MineSweeper.ROWS + 1):
            # проходим по всем строкам, кроме барьерных
            for j in range(1, MineSweeper.COLUMNS + 1):
                # проходим по всем столбцам, кроме барьерных
                btn = self.buttons[i][j]  # указываем координаты кнопки (номер строки и столбца)
                count_bomb = 0  # заводим счетчик бомб среди соседей
                if not btn.is_mine:  # считаем соседей только для тех кнопок, которые не являются бомбой
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]  # все возможные соседи для кнопки btn
                            if neighbour.is_mine:  # если сосед - мина, счетчик увеличиваем
                                count_bomb += 1
                btn.count_bomb = count_bomb  # атрибут для каждой кнопки

    @staticmethod  # статичный метод (для методов без self)
    def get_mines_places(exclude_number: int):
        # для расположения мин, исключаем номер кнопки первого клика
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROWS + 1))
        # Создаем список номеров от 1 до итогового количества кнопок
        # для этого количество строк умножаем на количество столбцов и прибавляем 1
        # (т.к. последнее число в range не входит)
        print(f'Исключаем кнопку номер {exclude_number}')
        indexes.remove(exclude_number)  # удаляем кнопку первого клика
        shuffle(indexes)  # перемешиваем список с номерами кнопок
        return indexes[:MineSweeper.MINES]  # возвращаем индексы с начала до количества мин


game = MineSweeper()  # вызов класса
# кнопки сохранятся в game, поэтому обращаться через game.buttons
game.start()  # запускаем игру