from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QDateEdit, QMessageBox, QFileDialog, QLineEdit, QComboBox, QFrame, QTabWidget, QHeaderView, QSizePolicy
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
        self.setMinimumSize(1000, 700)
        
        self.setup_dark_styles()
        self.init_ui()

    def setup_dark_styles(self):
        """Функция для установки темной темы приложения"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            
            QFrame {
                background-color: #3a3a3a;
                border-radius: 8px;
                border: 1px solid #444;
            }
            
            QTabWidget::pane {
                border: 1px solid #444;
                border-radius: 8px;
                padding: 5px;
                background: #3a3a3a;
            }
            
            QTabWidget::tab-bar {
                alignment: center;
                padding: 8px 16px;
                            margin-right: 2px;
            }
            QTabBar::tab {
                font-size: 14px;
                background: #3a3a3a;
                border: 1px solid #444;
                border-bottom: none;
                padding: 8px 16px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
                color: #bbb;
            }
            
            QTabBar::tab:selected {
                background: #2d2d2d;
                color: #eee;
                font-weight: bold;
                border-bottom: 2px solid #5d9cec;
            }
            
            QPushButton {
                background-color: #5d9cec;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 120px;
            }
            
            QPushButton:hover {
                background-color: #4a89dc;
            }
            
            QPushButton:pressed {
                background-color: #3b7dd8;
            }
            
            QTableWidget {
                background-color: #3a3a3a;
                border: 1px solid #444;
                border-radius: 6px;
                gridline-color: #444;
                selection-background-color: #5d9cec;
                selection-color: white;
                color: #ddd;
                alternate-background-color: #3a3a3a; /* Убирает чередование цветов */
            }

            QTableWidget QHeaderView::section {
                background-color: #4a4a4a;
                color: #eee;
                padding: 6px;
                border: 1px solid #444;
                font-weight: bold;
            }

            QTableWidget QTableCornerButton::section {
                background-color: #4a4a4a;
                border: 1px solid #444;
            }

            QTableWidget::item {
                background-color: #3a3a3a !important;
                           
            }

            QTableWidget::item:selected {
                background-color: #5d9cec;
                color: white;
            }

            
            QComboBox, QDateEdit {
                padding: 6px;
                border: 1px solid #444;
                border-radius: 4px;
                background: #4a4a4a;
                color: #ddd;
                min-width: 120px;
            }
            
            QComboBox::drop-down, QDateEdit::drop-down {
                width: 20px;
                border-left: 1px solid #444;
            }
            
            QComboBox QAbstractItemView {
                background-color: #4a4a4a;
                color: #ddd;
                selection-background-color: #5d9cec;
                selection-color: white;
            }
            
            QLabel {
                color: #bbb;
            }
            
            QCalendarWidget QWidget {
                background: #3a3a3a;
                color: #ddd;
            }
            
            QCalendarWidget QToolButton {
                background: #4a4a4a;
                color: #ddd;
            }
            
            QCalendarWidget QMenu {
                background: #4a4a4a;
                color: #ddd;
            }
            
            QCalendarWidget QAbstractItemView:enabled {
                color: #ddd;
                selection-background-color: #5d9cec;
                selection-color: white;
            }
        """)

    def init_ui(self):
        self.main_frame = QFrame()
        self.main_frame.setObjectName("mainFrame")
        self.setCentralWidget(self.main_frame)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.title_bar = TitleBar(self)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        
        self._create_period_widgets()
        self._create_table_tab()
        self._create_stats_tab()
        
        

        layout = QVBoxLayout()
        layout.addWidget(self.title_bar)
        layout.addSpacing(5)
        layout.addWidget(self.tabs)
        layout.addLayout(self.period_layout)
        
        layout.setContentsMargins(10, 10, 10, 10)
        self.main_frame.setLayout(layout)

    def _create_table_tab(self):
        self.table_tab = QWidget()
        self.table_tab.setObjectName("tableTab")
        
        self.add_but = QPushButton("Добавить запись")
        self.del_but = QPushButton("Удалить запись")
        self.change_but = QPushButton("Изменить запись")
        
        self.table = QTableWidget()
        
        self.del_but.clicked.connect(self.delete_record)
        self.add_but.clicked.connect(self.add_record_window)
        self.change_but.clicked.connect(self.update_record)

        lab1 = QLabel("Отображать данные по: ")
        self.sort_box = QComboBox()
        self.sort_box.addItems(["Все", "Доходы", "Расходы"])
        self.sort_box.currentIndexChanged.connect(self.change_period)

        # self._create_period_widgets()

        button_layout = QVBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_but)
        button_layout.addWidget(self.del_but)
        button_layout.addWidget(self.change_but)
        button_layout.addStretch()
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 0, 10, 0)
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(lab1)
        filter_layout.addWidget(self.sort_box)
        filter_layout.addStretch()
        filter_layout.setSpacing(10)
        
        table_layout = QVBoxLayout()
        table_layout.addLayout(filter_layout)
        table_layout.addWidget(self.table)
        # table_layout.addLayout(self.period_layout)
        table_layout.setSpacing(15)
        table_layout.setContentsMargins(10, 10, 10, 10)
        
        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(table_layout)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.table_tab.setLayout(main_layout)
        self.tabs.addTab(self.table_tab, "Таблица операций")
        self.table_setup()

    def _create_period_widgets(self):
        lab1 = QLabel("Выберите период: ")
        lab2 = QLabel("От:")
        lab3 = QLabel("До:")

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setDisplayFormat("dd.MM.yyyy")

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setDisplayFormat("dd.MM.yyyy")

        period_btn = QPushButton("Показать")
        period_btn.clicked.connect(self.change_period)
        period_btn.clicked.connect(self.set_data)

        self.period_layout = QHBoxLayout()
        self.period_layout.addStretch()
        self.period_layout.addWidget(lab1)
        self.period_layout.addWidget(lab2)
        self.period_layout.addWidget(self.date_from)
        self.period_layout.addWidget(lab3)
        self.period_layout.addWidget(self.date_to)
        self.period_layout.addWidget(period_btn)
        self.period_layout.addStretch()
        self.period_layout.setSpacing(10)

    def table_setup(self):
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID","Тип","Дата","Категория", "Описание", "Сумма"])
        self.table.setColumnWidth(0, 50)    
        self.table.setColumnWidth(1, 80)    
        self.table.setColumnWidth(2, 100)   
        self.table.setColumnWidth(3, 150)  
        self.table.setColumnWidth(4, 250)   
        self.table.setColumnWidth(5, 100)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  
        header = self.table.horizontalHeader()
        header.setSectionsMovable(False) 
        header.setSectionsClickable(False) 
        header.setStretchLastSection(False)
        header.setSectionResizeMode(QHeaderView.Fixed)  
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.change_period()





    def change_period(self):
        sort_stat = self.sort_box.currentIndex()
        per_from = self.date_from.date().toPython()
        per_to = self.date_to.date().toPython()

        if sort_stat == 0:
            data = get_data_by_period(conn, per_from, per_to)
            self._load_data_to_table(data)

        if sort_stat == 1:
            data = get_data_by_type(conn, per_from, per_to, "income")
            self._load_data_to_table(data)
        
        if sort_stat == 2:
            data = get_data_by_type(conn, per_from, per_to, "expense")
            self._load_data_to_table(data)
        


    def _load_data_to_table(self, data):
        self.table.setRowCount(len(data))   
        for r, row in enumerate(data):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value)))   

    def _create_stats_tab(self):
        self.stats_tab = QWidget()
        self.exp_cat = ["Продукты", "Транспорт", "Развлечения", "Комунальные услуги", "Одежда"]
        self.inc_cat = ["Зарплата", "Премия", "Подарок", "Продажа вещей"]

        header_style = """
                    /* Layout styling */
            QVBoxLayout {
                spacing: 15px;
            }
            
            QHBoxLayout {
                spacing: 15px;
            }
            
            #sumIncomeTitle {
                font-size: 18px;
                font-weight: bold;
                
                }

            #sumIncomeValue {
                font-size: 18px;
                font-weight: bold;
            
            }
            #sumExpTitle {
                font-size: 18px;
                font-weight: bold;
       
        }

         #sumExpValue {
            font-size: 18px;
            font-weight: bold;
      
        }
            
            /* Data value labels */
            QLabel[data="value"] {
                
        
            
            width: 250px;
             
    
                
                padding: 6px 10px;
                min-width: 90px;
                font-weight: 500;
                background-color: #3a3a3a;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
     
            QLabel{
            background-color: #4a4a4a;

            }
            
            QLabel[title="header"] {
                background-color: #4682B4;
                color: white;
                font-weight: bold;
                text-align: center;
                padding: 8px;
                border-radius: 4px;
                font-size: 16px;
                margin-bottom: 20px;
                }

        """

        labels_exp = [QLabel(cat) for cat in self.exp_cat]
        labels_inc = [QLabel(cat) for cat in self.inc_cat]

        label_exp = QLabel("Расходы")
        label_exp.setProperty("title", "header")
        label_exp.setAlignment(Qt.AlignCenter)
        label_inc = QLabel("Доходы")
        label_inc.setProperty("title", "header")
        label_inc.setAlignment(Qt.AlignCenter)

        self.data_exp_lab = [QLabel() for _ in self.exp_cat]
        self.data_inc_lab = [QLabel() for _ in self.inc_cat]

        
        
        for label in self.data_exp_lab + self.data_inc_lab:
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.max_exp_lab = QLabel()
        self.min_exp_lab = QLabel()
        self.sum_exp_lab = QLabel()

        self.max_inc_lab = QLabel()
        self.min_inc_lab = QLabel()
        self.sum_inc_lab = QLabel()

        exp_layout = QVBoxLayout()
        exp_layout.setSpacing(5)
        exp_layout.addWidget(label_exp)

        for lab, dat in zip(labels_exp, self.data_exp_lab):
            row = QHBoxLayout()
            row.addWidget(lab)
            row.addWidget(dat)
            exp_layout.addLayout(row)


        exp_layout.addSpacing(25)

        for title, lab in [
            ("Максимальный расход:", self.max_exp_lab),
            ("Минимальный расход:", self.min_exp_lab),
            ("Сумма расходов:", self.sum_exp_lab),
        ]:
            row = QHBoxLayout()
            title_label = QLabel(title)
            row.addWidget(title_label)
            row.addWidget(lab)

            if title =="Сумма расходов:":
                exp_layout.addSpacing(50)
                title_label.setObjectName("sumExpTitle")  
                lab.setObjectName("sumExpValue")

            exp_layout.addLayout(row)

        inc_layout = QVBoxLayout()
        inc_layout.setSpacing(5)
        inc_layout.addWidget(label_inc)

        for lab, dat in zip(labels_inc, self.data_inc_lab):
            row = QHBoxLayout()
            row.addWidget(lab)
            row.addWidget(dat)
            inc_layout.addLayout(row)

        inc_layout.addSpacing(25)
        for title, lab in [
            ("Максимальный доход:", self.max_inc_lab),
            ("Минимальный доход:", self.min_inc_lab),
            ("Сумма доходов:", self.sum_inc_lab),
        ]:
            row = QHBoxLayout()
            title_label = QLabel(title)
            row.addWidget(title_label)
            row.addWidget(lab)
            if title =="Сумма доходов:":
                inc_layout.addSpacing(50)
                title_label.setObjectName("sumIncomeTitle")  
                lab.setObjectName("sumIncomeValue")

            inc_layout.addLayout(row)
# 
# 
# 
        # self._create_period_widgets()

        
        exp_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(exp_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(inc_layout)

        self.set_data()
        main_layout1 = QVBoxLayout()
        main_layout1.setContentsMargins(0, 0, 0, 0)
        main_layout1.addLayout(main_layout)
        main_layout1.addStretch()
        # main_layout1.addLayout(self.period_layout)
        main_layout1.addSpacing(20)

        self.stats_tab.setStyleSheet(header_style)
        self.stats_tab.setLayout(main_layout1)

        self.tabs.addTab(self.stats_tab, "Статистика")

        for label in self.data_exp_lab + self.data_inc_lab:
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label.setProperty("data", "value")

        for lab in [self.max_exp_lab, self.min_exp_lab, self.sum_exp_lab,
                    self.max_inc_lab, self.min_inc_lab, self.sum_inc_lab]:
            lab.setProperty("data", "value")
            lab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            lab.setWordWrap(True)
      


    def set_data(self):
        date_from = self.date_from.date().toPython()
        date_to = self.date_to.date().toPython()

        res_exp = get_exp_data(conn, date_from, date_to)
        res_inc = get_inc_data(conn, date_from, date_to)

        max_exp = get_max_exp(conn, date_from, date_to)
        min_exp = get_min_exp(conn, date_from, date_to)

        max_inc = get_max_inc(conn, date_from, date_to)
        min_inc = get_min_inc(conn, date_from, date_to)

        sum_exp= get_sum_exp(conn, date_from, date_to)
        sum_inc = get_sum_inc(conn, date_from, date_to)

        data = {
            "income": ["Salary", "Bonus", "Gift", "Sale of items"],
            "expense": ["Groceries", "Transport", "Entertainment", "Utilities", "Clothing"]
        }

        for i, v in enumerate(data["expense"]):
            amount = res_exp.get(v, 0)  
            self.data_exp_lab[i].setText(f"{amount} грн")

        for i, v in enumerate(data["income"]):
            amount = res_inc.get(v, 0)  
            self.data_inc_lab[i].setText(f"{amount} грн")

        if max_exp:
            try:
                idx = data["expense"].index(max_exp[0][0])
                self.max_exp_lab.setText(f"Категория - {self.exp_cat[idx]}, сумма - {max_exp[0][1]} грн")
            except ValueError:
                self.max_exp_lab.setText("Нет данных")
        else:
            self.max_exp_lab.setText("Нет данных")

        if min_exp:
            try:
                idx = data["expense"].index(min_exp[0][0])
                self.min_exp_lab.setText(f"Категория - {self.exp_cat[idx]}, сумма - {min_exp[0][1]} грн")
            except ValueError:
                self.min_exp_lab.setText("Нет данных")
        else:
            self.min_exp_lab.setText("Нет данных")

        if max_inc:
            try:
                idx = data["income"].index(max_inc[0][0])
                self.max_inc_lab.setText(f"Категория - {self.inc_cat[idx]}, сумма - {max_inc[0][1]} грн")
            except ValueError:
                self.max_inc_lab.setText("Нет данных")
        else:
            self.max_inc_lab.setText("Нет данных")

        if min_inc:
            try:
                idx = data["income"].index(min_inc[0][0])
                self.min_inc_lab.setText(f"Категория - {self.inc_cat[idx]}, сумма - {min_inc[0][1]} грн")
            except ValueError:
                self.min_inc_lab.setText("Нет данных")
        else:
            self.min_inc_lab.setText("Нет данных")

        if sum_exp:
            try:
                idx = sum_exp[0][1]
                self.sum_exp_lab.setText(f"{idx} грн")
            except ValueError:
                self.sum_exp_lab.setText("Нет данных")
        else:
            self.sum_exp_lab.setText("Нет данных")

        if sum_inc:
            try:
                idx = sum_inc[0][1]
                self.sum_inc_lab.setText(f"{idx} грн")
            except ValueError:
                self.sum_inc_lab.setText("Нет данных")
        else:
            self.sum_inc_lab.setText("Нет данных")
        
    

    def add_record_window(self):
        self.add_window = AddWindow()  
        self.add_window.record_added.connect(self.change_period)  
        self.add_window.show()
        
    def delete_record(self):
    
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для удаления.")
            return

        selected_row = selected_items[0].row()
        record_id_item = self.table.item(selected_row, 0) 
        if record_id_item is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить ID выбранной записи.")
            return

        record_id = record_id_item.text()

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Удалить запись с ID {record_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            delete_record(conn, int(record_id))  
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить запись:\n{e}")
            return

        self.change_period()

    def update_record(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для изменения")
            return

        selected_row = selected_items[0].row()
        record_id_item = self.table.item(selected_row, 0) 
        if record_id_item is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить ID выбранной записи.")
            return

        record_id = record_id_item.text()
        self.update_window = AddWindow() 
        self.update_window.setWindowTitle("Изменение записи")
        self.update_window.but_add.setText("Изменить запись")
        try:
            self.update_window.but_add.clicked.disconnect()
        except TypeError:
            pass  
        self.update_window.but_add.clicked.connect(lambda: self.update_window.update_rec(record_id))
        self.update_window.record_added.connect(self.change_period)  
        self.update_window.show()
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())