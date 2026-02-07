from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, 
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTextEdit,
    QDateEdit, QMessageBox, QFileDialog, QLineEdit, QComboBox, QFrame, QTabWidget, QHeaderView
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtGui import QDoubleValidator
import sys
from pathlib import Path
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSpacerItem, QSizePolicy


# Добавляем папку `program/` в пути Python
sys.path.append(str(Path(__file__).parent.parent))  # Поднимаемся на уровень выше

from db.models import *

class AddWindow(QWidget):
    record_added = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавление записи")
        self.setMinimumSize(480, 360)

        self.init_ui()

    def init_ui(self):
        lab_type = QLabel("Выбирете тип операции: ")
        lab_date = QLabel("Выбирете дату операции: ")
        lab_category = QLabel("Выбирете категорию операции: ")
        lab_description = QLabel("Напишите описание операции (необязательно): ")
        lab_amount = QLabel("Напишите цену: ")

        self.data = {
                "income": ["Salary", "Bonus", "Gift", "Sale of items"],
                "expense": ["Groceries", "Transport", "Entertainment", "Utilities", "Clothing"]
            
        }

        self.box_type = QComboBox()
        self.box_type.addItems(self.data.keys())
        self.box_type.currentIndexChanged.connect(self.update_category_combo)

        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(QDate.currentDate())

        self.box_category = QComboBox()
        self.update_category_combo(0)

        self.description_edit = QLineEdit(placeholderText= "Введите текст")

        self.amount_edit = QLineEdit(placeholderText= "Введите число")
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation) 
        validator.setDecimals(2)  
        validator.setBottom(0.0) 
        self.amount_edit.setValidator(validator)

        self.but_add = QPushButton("Добавить запись")
        self.cancl_but = QPushButton("Отмена")

        
        self.but_add.clicked.connect(self.add_rec)
        self.cancl_but.clicked.connect(self.close)
        
        layout = QGridLayout()

        layout.addWidget(lab_type, 0, 0)
        layout.addWidget(self.box_type, 0, 1)

        layout.addWidget(lab_date, 1, 0)
        layout.addWidget(self.date, 1, 1)

        layout.addWidget(lab_category, 2, 0)
        layout.addWidget(self.box_category, 2, 1)

        layout.addWidget(lab_description, 3, 0)
        layout.addWidget(self.description_edit, 3, 1)

        layout.addWidget(lab_amount, 4, 0)
        layout.addWidget(self.amount_edit, 4, 1)

       
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.but_add)
        button_layout.addWidget(self.cancl_but)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 5, 0)
        layout.addLayout(button_layout, 6, 0, 1, 2) 

        self.setLayout(layout)

        self.setStyleSheet("""
    /* Основной фон окна */
    QWidget {
        background-color: #2d2d2d;
        color: #e0e0e0;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
    }
    
    /* Заголовки меток */
    QLabel {
        color: #bbbbbb;
        padding: 4px 0;
        font-weight: 500;
    }
    
    /* Выпадающие списки */
    QComboBox {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #4a4a4a, stop:1 #3a3a3a);
        border: 1px solid #444;
        border-radius: 4px;
        padding: 6px 12px;
        min-width: 120px;
        color: #e0e0e0;
        selection-background-color: #5d9cec;
    }
    
    QComboBox::drop-down {
        width: 24px;
        border-left: 1px solid #444;
        background: transparent;
    }
    
    QComboBox::down-arrow {
        image: url(icons/down-arrow.png);
        width: 12px;
        height: 12px;
    }
    
    QComboBox QAbstractItemView {
        background: #3e3e3e;
        border: 1px solid #444;
        selection-background-color: #5d9cec;
        color: #e0e0e0;
    }
    
    /* Поля ввода */
    QLineEdit, QDateEdit {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #4a4a4a, stop:1 #3a3a3a);
        border: 1px solid #444;
        border-radius: 4px;
        padding: 6px 12px;
        color: #e0e0e0;
        selection-background-color: #5d9cec;
    }
    
    QLineEdit:focus, QDateEdit:focus {
        border: 1px solid #5d9cec;
    }
    
    QDateEdit::drop-down {
        width: 24px;
        border-left: 1px solid #444;
    }
    
    /* Календарь */
    QCalendarWidget {
        background: #3a3a3a;
        border: 1px solid #444;
    }
    
    QCalendarWidget QToolButton {
        color: #e0e0e0;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #4a4a4a, stop:1 #3a3a3a);
    }
    
    /* Кнопки */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #5d9cec, stop:1 #4a89dc);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        min-width: 120px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #4a89dc, stop:1 #3b7dd8);
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #3b7dd8, stop:1 #2a6cd0);
    }
    
    /* Кнопка "Отмена" */
    QPushButton#cancl_but {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #e74c3c, stop:1 #c0392b);
    }
    
    QPushButton#cancl_but:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #c0392b, stop:1 #a5281b);
    }
    
    QPushButton#cancl_but:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                  stop:0 #a5281b, stop:1 #8c1b0f);
    }
    
    /* Плейсхолдеры */
    QLineEdit[placeholderText] {
        color: #888;
        font-style: italic;
    }
    
    /* Валидация поля суммы */
    QLineEdit:invalid {
        border: 1px solid #e74c3c;
    }
""")

    def update_category_combo(self, i):
        t = self.box_type.currentText()
        self.box_category.clear()
        self.box_category.addItems(self.data[t])

    def add_rec(self):
        type = self.box_type.currentText()
        category = self.box_category.currentText()
        date = self.date.date().toPython()
        description = self.description_edit.text().strip()
        try:
            amount = float(self.amount_edit.text().strip().replace(',', '.'))
            if not amount:
                QMessageBox.warning(self, "Ошибка", "Поле не может быть пустым!", QMessageBox.Ok)
        except:
            QMessageBox.warning(self, "Ошибка", "Поле не может быть пустым!", QMessageBox.Ok)
            print("Ошибка конвертации")

        

        add_record(conn, type, date, category, description, amount)

        self.record_added.emit()  
        self.close()     
    
    def update_rec(self, id):
        type = self.box_type.currentText()
        category = self.box_category.currentText()
        date = self.date.date().toPython()
        description = self.description_edit.text().strip()
        try:
            amount = float(self.amount_edit.text().strip().replace(',', '.'))
            if not amount:
                QMessageBox.warning(self, "Ошибка", "Поле не может быть пустым!", QMessageBox.Ok)
        except:
            QMessageBox.warning(self, "Ошибка", "Поле не может быть пустым!", QMessageBox.Ok)
            print("Ошибка конвертации")

        

        update_record(conn, id, type, date, category, description, amount)

        self.record_added.emit() 
        self.close()     




