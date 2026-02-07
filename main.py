
from ui.main_window import MainWindow
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())