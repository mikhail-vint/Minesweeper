import tkinter as tk # импортируем tkinter
from random import shuffle # позволяет перемешивать коллекцию

# словарь для цветов цифр на игровом поле по кодам HEX (
colors = {1: 'blue', 2: 'green', 3: 'red', 4: '#4245f5',
          5: 'brown', 6: '#42f5e3', 7: 'black', 8: '#f54242', 0: 'white'} 

class MyButton(tk.Button): # класс наследуется от класса Button из tkinter
    
    def __init__ (self, master, x, y, number=0, *args, **kwargs):
        # number - номер кнопки (из счетчика count), по умолчанию 0
        # x, y - координаты кнопки,
        # *args, **kwargs - любые значения, которые могут понадобиться для определенной кнопки
        # (например, width, font и т.д.)
        super(MyButton, self).__init__(
            master, width = 3, font = 'Calibri 15 bold', *args, **kwargs)
        # вызываем метод init у самой кнопки (tk.Button) для того,
        # чтобы создалась изначальная кнопка, потом у нее уже будем определять аттрибуты x и y
        # указываем ширину кнопки (width) и шрифт для текста внутри кнопки
        # шрифт Calibri, размер 15, жирный
        self.x = x # присваиваем координаты
        self.y = y
        self.number = number # присваиваем номер кнопки
        self.is_mine = False # мина кнопка или нет, по умолчанию все кнопки не мины
        self.count_bomb = 0 # количество мин среди соседей, по умолчанию 0
        self.is_open = False # открывали кнопку или нет, по умолчанию все кнопки не открыты
    
    def __repr__ (self): # от класса repr зависит, как будет выглядеть объект внутри консоли
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'
        # для вывода на экран всех аттрибутов кнопки
    
    
class MineSweeper: # создаем класс
    
    window = tk.Tk() # создаем окно

    ROWS = 10 # переменная для количества строк 
    COLUMNS = 7 # переменная для количества столбцов
    MINES = 15 # переменная для количества мин

    def __init__ (self): # переопределяем (т.к. он уже определен в tkinter) метод init
        # метод автоматически запускается, когда запускаем класс
        
        self.buttons = [] # пустой список для хранения кнопок (игровое поле)
        # к экземпляру класса обращаемся через self
        
        # барьерные кнопки нужны для того, чтобы у каждой кнопки было по 8 соседей,
        # включая кнопки по краям поля (у которых было либо 5, либо 3 соседа)
        for i in range(MineSweeper.ROWS + 2): # +2 для барьерных кнопок
            # цикл для генерации списка кнопок
            # обращаемся к переменной через имя класса
            temp = [] # временный список
            
            for j in range(MineSweeper.COLUMNS + 2): # +2 для барьерных кнопок
                # здесь накопится столько кнопок для одного столбца, сколько указано в COLUMNS
                btn = MyButton(MineSweeper.window, x = i, y = j) #, number = count)
                # создаем кнопку в окне (вызываем из класса MyButton),
                # присваиваем координаты (x = i (перебирает строки), y = j (перебирает столбцы))
                # в number передаем номер кнопки
                btn.config(command = lambda button = btn: self.click(button))
                # command отвечает за обработку кнопок
                # создаем анонимную функцию
                # функция принимает переменную button (название может быть любое)
                # и вызывает клик от этой переменной 
                temp.append(btn) # добавляем кнопку во временный список
                                
            self.buttons.append(temp) # добавляем в итоговый список с кнопками
    
    def click(self, clicked_button: MyButton): # метод для нажатия кнопки
        # создаем в классе MineSweeper, а не в MyButton,
        # т.к. должна быть информация про соседние кнопки, 
        # а в классе MyButton нет такой информации
        # принимает на вход кнопку, которую нажали (clicked_button)
        # указываем тип объкта, который ожидаем
        if clicked_button.is_mine:
            clicked_button.config(text = '*', background = 'red', disabledforeground = 'black')
            # если мина, текст на кнопке *, меняем фон на красный
            # цвет шрифта для * черный (disabledforeground)
            clicked_button.is_open = True # меняем аттрибут is_open на True (кнопку уже открывали)
        else:
            color = colors.get(clicked_button.count_bomb) # получаем значение ключа из словаря color
            if clicked_button.count_bomb: # если есть мины среды соседей (кнопка - не мина)
                # текст - сколько мин среди соседей
                clicked_button.config(text = clicked_button.count_bomb, disabledforeground = color)
                clicked_button.is_open = True # меняем аттрибут is_open на True (кнопку уже открывали)
            else:
                #clicked_button.config(text = '', disabledforeground = color)
                self.breadth_first_search(clicked_button) # поиск в ширину (для открытия соседних пустых кнопок)
        clicked_button.config(state = 'disabled') # теперь нельзя второй раз нажать на кнопку
        clicked_button.config(relief = tk.SUNKEN) # выделяем кнопку как "нажатую"
    
    def breadth_first_search(self, btn: MyButton): # поиск в ширину (для открытия соседних пустых кнопок)
        queue = [btn] # список кнопок, которые надо проверить на предмет мин или цифр
        # пока в списке кнопка, которую нажали
        # нужно проверить всех соседей нажатой кнопки и их соседей, если эти кнопки пустые
        while queue: # пока есть кнопки в списке для проверки
            cur_btn = queue.pop() # из очереди достаем кнопку для проверки
            color = colors.get(cur_btn.count_bomb, 'black') # получаем значение ключа из словаря color
            # Метод pop() удаляет элемент из списка и возвращает его
            if cur_btn.count_bomb: # если проверяемая кнопка имеет бомбы
                cur_btn.config(text = cur_btn.count_bomb, disabledforeground = color)  # текст - сколько мин среди соседей
            else: # если бомб нет
                cur_btn.config(text = '', disabledforeground = color)  # пустой текст
            cur_btn.is_open = True # меняем аттрибут is_open на True (кнопку уже открывали)
            cur_btn.config(state = 'disabled') # теперь нельзя второй раз нажать на кнопку
            cur_btn.config(relief = tk.SUNKEN) # выделяем кнопку как "нажатую"
            # после того, как обработали кнопку, нужно посмотреть на ее соседей по горизонтали и вертикали                     
            if cur_btn.count_bomb == 0: # только для той кнопки, которая не имеет бомб
                x, y = cur_btn.x, cur_btn.y # в x, y  записываем координаты текущей кнопки
                for dx in [-1, 0 , 1]: # координаты всех соседей по x
                    for dy in [-1, 0 , 1]: # координаты всех соседей по y
                        if not abs(dx - dy) == 1: # разница по модулю=1 только у нужных нам соседей по горизонтали и вертикали
                            continue # пропускаем ненужных соседей (выше в условии отрицание not)
                        next_btn = self.buttons[x+dx][y+dy] # получаем координаты следующей кнопки
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROWS and 1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            # если кнопка еще не была открыта и она не является барьерной и уже не стоит в очереди на проверку
                            queue.append(next_btn) # добавляем в очередь на проверку
                        
            
    def create_widgets(self): # метод для размещения кнопок на игровом поле
        
        for i in range(1, MineSweeper.ROWS + 1): # i - номер строки, +2 для барьерных кнопок
            for j in range(1, MineSweeper.COLUMNS + 1): # j - номер столбца, +2 для барьерных кнопок
                # начинаем с 1 (т.к. 0 - барьерная кнопка)
                # +2 меняем на +1, т.к. последняя тоже барьерная кнопка                
                btn = self.buttons[i][j] # указываем координаты кнопки (номер строки и столбца)
                btn.grid(row = i, column = j) # размещаем кнопку на игровом поле
    
    def open_all_buttons(self): # метод для открытия всех кнопок
        
        for i in range(MineSweeper.ROWS + 2): # i - номер строки, +2 для барьерных кнопок
            for j in range(MineSweeper.COLUMNS + 2): # j - номер столбца, +2 для барьерных кнопок
                btn = self.buttons[i][j] # указываем координаты кнопки (номер строки и столбца)
                if btn.is_mine:
                    btn.config(text = '*', background = 'red', disabledforeground = 'black')
                    # если мина, текст на кнопке *, меняем фон на красный
                    # цвет шрифта для * черный (disabledforeground)
                elif btn.count_bomb in colors: # если кол-во бомб есть среди ключей в словаре colors (чтобы не выводился 0)
                    color = colors.get(btn.count_bomb) # получаем значение ключа
                    btn.config(text = btn.count_bomb, fg = color) 
                    # если не мина, текст - номер кнопки + устанавливаем цвет
                                            
    def start(self): # метод для старта игры
        
        self.create_widgets() # создаем виджеты
        self.insert_mines() # расставляем мины
        self.count_mines_in_buttons() # считаем количество мин среди соседей
        self.print_buttons() # выводим кнопки
        #self.open_all_buttons() # открываются номера / мины всех кнопок
        MineSweeper.window.mainloop() # выводим окно (mainloop - обработчик событий)
        # размер окна зависит от переменных ROW и COLUMNS (подбирается автоматически)      
        
    def print_buttons(self): # для вывода аттрибутов кнопок на экран
                
        for i in range(1, MineSweeper.ROWS + 1): 
            # i - номер строки, +2 было бы для барьерных кнопок
            # начинаем с 1 (т.к. 0 - барьерная кнопка)
            # +2 меняем на +1, т.к. последняя тоже барьерная кнопка
            for j in range(1, MineSweeper.COLUMNS + 1):
                # j - номер столбца, +2 для барьерных кнопок
                # начинаем с 1 (т.к. 0 - барьерная кнопка)
                # +2 меняем на +1, т.к. последняя тоже барьерная кнопка
                btn = self.buttons[i][j] # указываем координаты кнопки (номер строки и столбца)
                if btn.is_mine: # если кнопка - мина
                    print('B', end = '') # выводим B, убираем перенос строк
                else:
                    print(btn.count_bomb, end = '') # если нет - сколько мин вокруг, убираем перенос строк
            print() # добавляем пустой принт для разбиения вывода по строкам
                    
            
    def insert_mines(self): # распологаем мины  
        
        index_mines = self.get_mines_places() # получаем индексы для мин
        print(index_mines)
        count = 1 # счетчик
        for i in range(1, MineSweeper.ROWS + 1): 
            # i - номер строки, +2 было бы для барьерных кнопок
            # начинаем с 1 (т.к. 0 - барьерная кнопка)
            # +2 меняем на +1, т.к. последняя тоже барьерная кнопка
            for j in range(1, MineSweeper.COLUMNS + 1):
                # j - номер столбца, +2 для барьерных кнопок
                # начинаем с 1 (т.к. 0 - барьерная кнопка)
                # +2 меняем на +1, т.к. последняя тоже барьерная кнопка
                btn = self.buttons[i][j] # указываем координаты кнопки (номер строки и столбца)
                btn.number = count
                if btn.number in index_mines: # если номер кнопки в списке индексов мин
                    btn.is_mine = True # меняем аттрибут кнопки is_mine с False на True
                count += 1 # с каждой кнопкой count увеличивается на 1
        # в итоге номера присваиваются всем кнопкам, кроме барьерных (по краям поля)
    
    def count_mines_in_buttons(self): # находим количество мин среди соседей для каждой кнопки-не мины
        
        for i in range(1, MineSweeper.ROWS + 1): 
            # проходим по всем строкам, кроме барьерных
            for j in range(1, MineSweeper.COLUMNS + 1):
                # проходим по всем столбцам, кроме барьерных
                btn = self.buttons[i][j] # указываем координаты кнопки (номер строки и столбца)
                count_bomb = 0 # заводим счетчик бомб среди соседей
                if not btn.is_mine:
                # считаем соседей только для тех кнопок, которые не являются бомбой
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            # все возможные соседи для кнопки btn
                            if neighbour.is_mine:
                                # если сосед - мина, счетчик увеличиваем
                                count_bomb += 1
                btn.count_bomb = count_bomb # аттрибут для каждой кнопки
    
    @staticmethod # статичный метод
    def get_mines_places(): # для расположения мин
        
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROWS + 1)) 
        # создаем список номеров от 1 до итогового количества кнопок 
        # для этого количество строк умножаем на количество столбцов и умножаем на 1
        # (т.к. последнее число в range не входит)
        shuffle(indexes) # перемешиваем список с номерами кнопок
        return indexes[:MineSweeper.MINES] # возвращаем индексы с начала до количества мин

game = MineSweeper() # вызов класса
# кнопки сохранятся в game, поэтому обращаться через game.buttons
game.start() # запускаем игру




        
