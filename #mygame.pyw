# -*- coding: utf-8 -*-

# Игра "Холодильник!" Автор: Мария

import sys
from random import choice
from PyQt4 import QtGui, QtCore


class NewGame(QtGui.QWidget):
    
    """Класс содержит объекты и функции для игры 'Холодильник!'"""
  
    
    def __init__(self, parent = None):

        """Создание главного окна, кнопок, меню"""


        QtGui.QWidget.__init__(self, parent)

        # Настройки главного окна
        self.setWindowTitle("Холодильник!")
        self.setWindowIcon(QtGui.QIcon("ex.png"))
        self.setFixedSize(190, 200)
        color = QtGui.QColor(228, 225, 217)
        self.setStyleSheet("QWidget {background-color: %s}"
                           % color.name())

        # Создание сетки для кнопок, иконок
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(0)
        self.iconH = QtGui.QIcon("1.png")
        self.iconV = QtGui.QIcon("0.png")
        
        # Цвет для кнопок
        color.setRgb(255, 255, 255, 100)

        # Создание кнопок,их настройка, помещение в сетку    
        for i in range(4):
            for j in range(4):
               
                button = QtGui.QPushButton(self)
                button.setMinimumHeight(40)
                button.setMaximumWidth(55)
                button.setStyleSheet("QPushButton {background-color: %s}"
                           % color.name())
                self.connect(button, QtCore.SIGNAL("clicked()"),\
                             self.click)
                self.grid.addWidget(button, i + 1, j + 1)

        # Создание списка значений и вывод иконок на кнопки        
        self.changeitems()
      
        # Создание пунктов меню (объект QAction относится не только к меню)
        exit = QtGui.QAction(u"Выход", self)
        exit.setStatusTip(u"Выйти из игры")
        self.connect(exit, QtCore.SIGNAL("triggered()"),\
                                     QtCore.SLOT("close()"))
        
        news = QtGui.QAction(u"Новая игра", self)
        news.setStatusTip(u"Начать новую игру")
        self.connect(news, QtCore.SIGNAL("triggered()"),\
                                          self.changeitems)

        rules = QtGui.QAction(u"Об игре", self)
        rules.setStatusTip(u"Узнать подробности")
        self.connect(rules, QtCore.SIGNAL("triggered()"),\
                                          self.helps)
        
        # Создание меню, настройка цвета, добавление пунктов
        menu = QtGui.QMenuBar(self)
        color.setRgb(255, 255, 255, 50)
        menu.setStyleSheet("QMenuBar {background-color: %s}"
                           % color.name())
        menu.addAction(news)
        menu.addAction(rules)
        menu.addAction(exit)

        # Добавление меню в сетку, вывод сетки с содержимым
        self.grid.setMenuBar(menu)
        self.setLayout(self.grid)             


    def helps(self):

        """Вывод диалогового окна 'Об игре'"""

        self.help = QtGui.QMessageBox(self)   
        self.help.setWindowTitle(u"Об игре")
        self.help.setButtonText(1, u"Закрыть")
        self.help.setGeometry(self.x() + self.width() + 20,\
                              self.y() + 30, 0, 0)
        self.help.setInformativeText(u"""
Название:  Холодильник!
Автор:     Мария
Идея игры: Холодильник из игры 'Братья Пилоты. По следам\
Полосатого Слона'

Описание игры:
    На холодильнике хитроумный замок с 16 ручками. \
Чтобы открыть холодильник, нужно все ручки установить \
в горизонтальное положение. Но это не так просто! \
Когда ручка поворачивается, вместе с ней приходят в движение \
все ручки, из той же строки и того же столбца.

""")              
        self.help.show()
    
    
    def changeitems(self):

        """Создание(изменение) списка значений
вызывается в начале и после нажатия пункта меню 'Новая игра'"""
        
        # Список значений - содержит значения кнопок     
        # по нему определяется конец игры и выводятся иконки
        self.mlist = [choice(range(2)) for x in range(16)]
        self.output()


    def output(self):

        """Вывод иконок на кнопки по списку значений"""

        btn = QtGui.QWidget()

        for i in range(self.grid.count()):

            btn = self.grid.itemAt(i).widget
            # Смена иконок на противоположные
            if self.mlist[i]== 1:       
                btn().setIcon(self.iconH) 
            else: 
                btn().setIcon(self.iconV)


    def click(self):

        """Вызывается при клике на кнопке
изменение списка значений, проверка на конец игры"""

        # Расчет стоблца и строки кнопки исходя из индекса в сетке
        index = self.grid.indexOf(self.sender())
        numi = index / 4
        numj = index % 4

        # Смена значений в списке
        self.mlist[index] = 0 if self.mlist[index]== 1 else 1
                       
        for i in range(4):

            self.mlist[int(numi) * 4 + i] = 0 if \
                self.mlist[int(numi) * 4 + i]== 1 else 1  
            self.mlist[i * 4 + int(numj)] = 0 if \
                self.mlist[i * 4 + int(numj)] == 1 else 1
            
        # Вывод иконок    
        self.output()

        # Проверка на конец игры - если в списке значений
        # не осталось 0 - все "ручки" горизонтальные
        if not 0 in self.mlist:
       
            res = QtGui.QMessageBox.information(self,\
                u"Поздравляю, холодильник открыт!!!",\
                                    u"Сыграть еще??",\
                        u"Конечно!", u"Выйти...")
    
            if res == 0:                
                self.changeitems()               
            else:
                self.close()

        

app = QtGui.QApplication(sys.argv)
newgame = NewGame()
newgame.show()
sys.exit(app.exec_())

