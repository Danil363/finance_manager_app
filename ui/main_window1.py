from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QDateEdit, QMessageBox, QFileDialog, QLineEdit, QComboBox, QFrame, QTabWidget
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon, QPixmap
import sys
from pathlib import Path

# Добавляем папку `program/` в пути Python
sys.path.append(str(Path(__file__).parent.parent))  # Поднимаемся на уровень выше

from db.models import *
from ui.add_window import AddWindow
from ui.title_bar import TitleBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Финансовый трекер")
        self.setMinimumSize(800, 600)

        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.title_bar = TitleBar(self)
        self.main_frame = QFrame()
        self.setCentralWidget(self.main_frame)

        self.tabs = QTabWidget()
        
        self.table_tab = QWidget()

        

        self._table_tab()

        self.tabs.addTab(self.table_tab, "Таблица")

        self.stats_tab = QWidget()
        self.tabs.addTab(self.stats_tab, "Statistic")

        layout = QVBoxLayout()
        layout.addWidget(self.title_bar)
        layout.addWidget(self.tabs)
        self.main_frame.setLayout(layout)

    
    def _table_tab(self):
        self.table_tab = QWidget()
        self.table_frame = QFrame()

        self.add_but = QPushButton("Добавить запись")
        self.del_but = QPushButton("Удалить запись")
        self.change_but = QPushButton("Изменить запись")

        self.table = QTableWidget()


        lab1 = QLabel("Отображать данные по: ")
        self.sort_box = QComboBox()
        self.sort_box.addItems(["Все", "Доходы", "Расходы"])

        self._period()

        self.table_tab_layout = QHBoxLayout()

        but_layout = QVBoxLayout()
        # but_layout.addStretch()
        but_layout.addSpacing(50)
        but_layout.addWidget(self.add_but)
        but_layout.addWidget(self.del_but)
        but_layout.addWidget(self.change_but)
        but_layout.addStretch()

        sort_layout = QHBoxLayout()
        sort_layout.addWidget(lab1)
        sort_layout.addWidget(self.sort_box)
        sort_layout.addStretch()

        table_layout = QVBoxLayout()
        table_layout.addLayout(sort_layout)
        table_layout.addWidget(self.table)
        table_layout.addLayout(self.period_layout)

        self.table_tab_layout.addLayout(but_layout)
        self.table_tab_layout.addLayout(table_layout)

        self.table_frame.setLayout(self.table_tab_layout)
        self.table_tab.setLayout(self.table_tab_layout)


    def _period(self):
        lab1 = QLabel("Выберите период: ")
        lab2 = QLabel("ОТ:")
        lab3 = QLabel("ДО:")

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())

        period_btn = QPushButton("Показать")
        period_btn.clicked.connect(self.change_period)

        self.period_layout = QHBoxLayout()
        self.period_layout.addWidget(lab1)
        self.period_layout.addWidget(lab2)
        self.period_layout.addWidget(self.date_from)
        self.period_layout.addWidget(lab3)
        self.period_layout.addWidget(self.date_to)
        self.period_layout.addWidget(period_btn)
        self.period_layout.addStretch()

    def change_period():
        pass








# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())