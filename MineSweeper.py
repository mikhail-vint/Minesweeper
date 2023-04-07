import tkinter as tk # ����������� tkinter
from random import shuffle # ��������� ������������ ���������

# ������� ��� ������ ���� �� ������� ���� �� ����� HEX (
colors = {1: 'blue', 2: 'green', 3: 'red', 4: '#4245f5',
          5: 'brown', 6: '#42f5e3', 7: 'black', 8: '#f54242', 0: 'white'} 

class MyButton(tk.Button): # ����� ����������� �� ������ Button �� tkinter
    
    def __init__ (self, master, x, y, number=0, *args, **kwargs):
        # number - ����� ������ (�� �������� count), �� ��������� 0
        # x, y - ���������� ������,
        # *args, **kwargs - ����� ��������, ������� ����� ������������ ��� ������������ ������
        # (��������, width, font � �.�.)
        super(MyButton, self).__init__(
            master, width = 3, font = 'Calibri 15 bold', *args, **kwargs)
        # �������� ����� init � ����� ������ (tk.Button) ��� ����,
        # ����� ��������� ����������� ������, ����� � ��� ��� ����� ���������� ��������� x � y
        # ��������� ������ ������ (width) � ����� ��� ������ ������ ������
        # ����� Calibri, ������ 15, ������
        self.x = x # ����������� ����������
        self.y = y
        self.number = number # ����������� ����� ������
        self.is_mine = False # ���� ������ ��� ���, �� ��������� ��� ������ �� ����
        self.count_bomb = 0 # ���������� ��� ����� �������, �� ��������� 0
        self.is_open = False # ��������� ������ ��� ���, �� ��������� ��� ������ �� �������
    
    def __repr__ (self): # �� ������ repr �������, ��� ����� ��������� ������ ������ �������
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mine}'
        # ��� ������ �� ����� ���� ���������� ������
    
    
class MineSweeper: # ������� �����
    
    window = tk.Tk() # ������� ����

    ROWS = 10 # ���������� ��� ���������� ����� 
    COLUMNS = 7 # ���������� ��� ���������� ��������
    MINES = 15 # ���������� ��� ���������� ���

    def __init__ (self): # �������������� (�.�. �� ��� ��������� � tkinter) ����� init
        # ����� ������������� �����������, ����� ��������� �����
        
        self.buttons = [] # ������ ������ ��� �������� ������ (������� ����)
        # � ���������� ������ ���������� ����� self
        
        # ��������� ������ ����� ��� ����, ����� � ������ ������ ���� �� 8 �������,
        # ������� ������ �� ����� ���� (� ������� ���� ���� 5, ���� 3 ������)
        for i in range(MineSweeper.ROWS + 2): # +2 ��� ��������� ������
            # ���� ��� ��������� ������ ������
            # ���������� � ���������� ����� ��� ������
            temp = [] # ��������� ������
            
            for j in range(MineSweeper.COLUMNS + 2): # +2 ��� ��������� ������
                # ����� ��������� ������� ������ ��� ������ �������, ������� ������� � COLUMNS
                btn = MyButton(MineSweeper.window, x = i, y = j) #, number = count)
                # ������� ������ � ���� (�������� �� ������ MyButton),
                # ����������� ���������� (x = i (���������� ������), y = j (���������� �������))
                # � number �������� ����� ������
                btn.config(command = lambda button = btn: self.click(button))
                # command �������� �� ��������� ������
                # ������� ��������� �������
                # ������� ��������� ���������� button (�������� ����� ���� �����)
                # � �������� ���� �� ���� ���������� 
                temp.append(btn) # ��������� ������ �� ��������� ������
                                
            self.buttons.append(temp) # ��������� � �������� ������ � ��������
    
    def click(self, clicked_button: MyButton): # ����� ��� ������� ������
        # ������� � ������ MineSweeper, � �� � MyButton,
        # �.�. ������ ���� ���������� ��� �������� ������, 
        # � � ������ MyButton ��� ����� ����������
        # ��������� �� ���� ������, ������� ������ (clicked_button)
        # ��������� ��� ������, ������� �������
        if clicked_button.is_mine:
            clicked_button.config(text = '*', background = 'red', disabledforeground = 'black')
            # ���� ����, ����� �� ������ *, ������ ��� �� �������
            # ���� ������ ��� * ������ (disabledforeground)
            clicked_button.is_open = True # ������ �������� is_open �� True (������ ��� ���������)
        else:
            color = colors.get(clicked_button.count_bomb) # �������� �������� ����� �� ������� color
            if clicked_button.count_bomb: # ���� ���� ���� ����� ������� (������ - �� ����)
                # ����� - ������� ��� ����� �������
                clicked_button.config(text = clicked_button.count_bomb, disabledforeground = color)
                clicked_button.is_open = True # ������ �������� is_open �� True (������ ��� ���������)
            else:
                #clicked_button.config(text = '', disabledforeground = color)
                self.breadth_first_search(clicked_button) # ����� � ������ (��� �������� �������� ������ ������)
        clicked_button.config(state = 'disabled') # ������ ������ ������ ��� ������ �� ������
        clicked_button.config(relief = tk.SUNKEN) # �������� ������ ��� "�������"
    
    def breadth_first_search(self, btn: MyButton): # ����� � ������ (��� �������� �������� ������ ������)
        queue = [btn] # ������ ������, ������� ���� ��������� �� ������� ��� ��� ����
        # ���� � ������ ������, ������� ������
        # ����� ��������� ���� ������� ������� ������ � �� �������, ���� ��� ������ ������
        while queue: # ���� ���� ������ � ������ ��� ��������
            cur_btn = queue.pop() # �� ������� ������� ������ ��� ��������
            color = colors.get(cur_btn.count_bomb, 'black') # �������� �������� ����� �� ������� color
            # ����� pop() ������� ������� �� ������ � ���������� ���
            if cur_btn.count_bomb: # ���� ����������� ������ ����� �����
                cur_btn.config(text = cur_btn.count_bomb, disabledforeground = color)  # ����� - ������� ��� ����� �������
            else: # ���� ���� ���
                cur_btn.config(text = '', disabledforeground = color)  # ������ �����
            cur_btn.is_open = True # ������ �������� is_open �� True (������ ��� ���������)
            cur_btn.config(state = 'disabled') # ������ ������ ������ ��� ������ �� ������
            cur_btn.config(relief = tk.SUNKEN) # �������� ������ ��� "�������"
            # ����� ����, ��� ���������� ������, ����� ���������� �� �� ������� �� ����������� � ���������                     
            if cur_btn.count_bomb == 0: # ������ ��� ��� ������, ������� �� ����� ����
                x, y = cur_btn.x, cur_btn.y # � x, y  ���������� ���������� ������� ������
                for dx in [-1, 0 , 1]: # ���������� ���� ������� �� x
                    for dy in [-1, 0 , 1]: # ���������� ���� ������� �� y
                        if not abs(dx - dy) == 1: # ������� �� ������=1 ������ � ������ ��� ������� �� ����������� � ���������
                            continue # ���������� �������� ������� (���� � ������� ��������� not)
                        next_btn = self.buttons[x+dx][y+dy] # �������� ���������� ��������� ������
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROWS and 1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            # ���� ������ ��� �� ���� ������� � ��� �� �������� ��������� � ��� �� ����� � ������� �� ��������
                            queue.append(next_btn) # ��������� � ������� �� ��������
                        
            
    def create_widgets(self): # ����� ��� ���������� ������ �� ������� ����
        
        for i in range(1, MineSweeper.ROWS + 1): # i - ����� ������, +2 ��� ��������� ������
            for j in range(1, MineSweeper.COLUMNS + 1): # j - ����� �������, +2 ��� ��������� ������
                # �������� � 1 (�.�. 0 - ��������� ������)
                # +2 ������ �� +1, �.�. ��������� ���� ��������� ������                
                btn = self.buttons[i][j] # ��������� ���������� ������ (����� ������ � �������)
                btn.grid(row = i, column = j) # ��������� ������ �� ������� ����
    
    def open_all_buttons(self): # ����� ��� �������� ���� ������
        
        for i in range(MineSweeper.ROWS + 2): # i - ����� ������, +2 ��� ��������� ������
            for j in range(MineSweeper.COLUMNS + 2): # j - ����� �������, +2 ��� ��������� ������
                btn = self.buttons[i][j] # ��������� ���������� ������ (����� ������ � �������)
                if btn.is_mine:
                    btn.config(text = '*', background = 'red', disabledforeground = 'black')
                    # ���� ����, ����� �� ������ *, ������ ��� �� �������
                    # ���� ������ ��� * ������ (disabledforeground)
                elif btn.count_bomb in colors: # ���� ���-�� ���� ���� ����� ������ � ������� colors (����� �� ��������� 0)
                    color = colors.get(btn.count_bomb) # �������� �������� �����
                    btn.config(text = btn.count_bomb, fg = color) 
                    # ���� �� ����, ����� - ����� ������ + ������������� ����
                                            
    def start(self): # ����� ��� ������ ����
        
        self.create_widgets() # ������� �������
        self.insert_mines() # ����������� ����
        self.count_mines_in_buttons() # ������� ���������� ��� ����� �������
        self.print_buttons() # ������� ������
        #self.open_all_buttons() # ����������� ������ / ���� ���� ������
        MineSweeper.window.mainloop() # ������� ���� (mainloop - ���������� �������)
        # ������ ���� ������� �� ���������� ROW � COLUMNS (����������� �������������)      
        
    def print_buttons(self): # ��� ������ ���������� ������ �� �����
                
        for i in range(1, MineSweeper.ROWS + 1): 
            # i - ����� ������, +2 ���� �� ��� ��������� ������
            # �������� � 1 (�.�. 0 - ��������� ������)
            # +2 ������ �� +1, �.�. ��������� ���� ��������� ������
            for j in range(1, MineSweeper.COLUMNS + 1):
                # j - ����� �������, +2 ��� ��������� ������
                # �������� � 1 (�.�. 0 - ��������� ������)
                # +2 ������ �� +1, �.�. ��������� ���� ��������� ������
                btn = self.buttons[i][j] # ��������� ���������� ������ (����� ������ � �������)
                if btn.is_mine: # ���� ������ - ����
                    print('B', end = '') # ������� B, ������� ������� �����
                else:
                    print(btn.count_bomb, end = '') # ���� ��� - ������� ��� ������, ������� ������� �����
            print() # ��������� ������ ����� ��� ��������� ������ �� �������
                    
            
    def insert_mines(self): # ����������� ����  
        
        index_mines = self.get_mines_places() # �������� ������� ��� ���
        print(index_mines)
        count = 1 # �������
        for i in range(1, MineSweeper.ROWS + 1): 
            # i - ����� ������, +2 ���� �� ��� ��������� ������
            # �������� � 1 (�.�. 0 - ��������� ������)
            # +2 ������ �� +1, �.�. ��������� ���� ��������� ������
            for j in range(1, MineSweeper.COLUMNS + 1):
                # j - ����� �������, +2 ��� ��������� ������
                # �������� � 1 (�.�. 0 - ��������� ������)
                # +2 ������ �� +1, �.�. ��������� ���� ��������� ������
                btn = self.buttons[i][j] # ��������� ���������� ������ (����� ������ � �������)
                btn.number = count
                if btn.number in index_mines: # ���� ����� ������ � ������ �������� ���
                    btn.is_mine = True # ������ �������� ������ is_mine � False �� True
                count += 1 # � ������ ������� count ������������� �� 1
        # � ����� ������ ������������� ���� �������, ����� ��������� (�� ����� ����)
    
    def count_mines_in_buttons(self): # ������� ���������� ��� ����� ������� ��� ������ ������-�� ����
        
        for i in range(1, MineSweeper.ROWS + 1): 
            # �������� �� ���� �������, ����� ���������
            for j in range(1, MineSweeper.COLUMNS + 1):
                # �������� �� ���� ��������, ����� ���������
                btn = self.buttons[i][j] # ��������� ���������� ������ (����� ������ � �������)
                count_bomb = 0 # ������� ������� ���� ����� �������
                if not btn.is_mine:
                # ������� ������� ������ ��� ��� ������, ������� �� �������� ������
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            # ��� ��������� ������ ��� ������ btn
                            if neighbour.is_mine:
                                # ���� ����� - ����, ������� �����������
                                count_bomb += 1
                btn.count_bomb = count_bomb # �������� ��� ������ ������
    
    @staticmethod # ��������� �����
    def get_mines_places(): # ��� ������������ ���
        
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROWS + 1)) 
        # ������� ������ ������� �� 1 �� ��������� ���������� ������ 
        # ��� ����� ���������� ����� �������� �� ���������� �������� � �������� �� 1
        # (�.�. ��������� ����� � range �� ������)
        shuffle(indexes) # ������������ ������ � �������� ������
        return indexes[:MineSweeper.MINES] # ���������� ������� � ������ �� ���������� ���

game = MineSweeper() # ����� ������
# ������ ���������� � game, ������� ���������� ����� game.buttons
game.start() # ��������� ����




        
