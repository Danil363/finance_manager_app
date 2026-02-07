from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QStyleOption, QStylePainter
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon, QFont,QPainter, QLinearGradient, QColor, QCursor

from PySide6.QtWidgets import QStyle





class TitleBar1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent  # Сохраняем ссылку на родительское окно
        self.setup_ui()
        self.mouse_pressed = False
        self.old_pos = QPoint()

    def setup_ui(self):
        self.setFixedHeight(30)
        self.setStyleSheet("""
            TitleBar {
                background-color: #2c3e50;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: none;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                font-weight: bold;
                border: none;
                           
            }
            QPushButton {
               
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            QPushButton#close_button:hover {
                background: #e74c3c;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(5)

        # Иконка приложения
        self.icon_label = QLabel()
        # Если нет своей иконки, можно использовать стандартную
        self.icon_label.setPixmap(QIcon.fromTheme("document-edit").pixmap(20, 20))
        layout.addWidget(self.icon_label)

        # Название приложения
        self.title_label = QLabel("Финансовый менеджер")
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(self.title_label)

        # Растягивающийся элемент
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Кнопки управления окном
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton))
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.parent.showMinimized)

        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.maximize_button.setFixedSize(30, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize)

        self.close_button = QPushButton()
        self.close_button.setObjectName("close_button")
        self.close_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.parent.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
        else:
            self.parent.showMaximized()
            self.maximize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed and not self.parent.isMaximized():
            delta = QPoint(event.globalPos() - self.old_pos)
            self.parent.move(self.parent.pos() + delta)
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def mouseDoubleClickEvent(self, event):
        self.toggle_maximize()

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.mouse_pressed = False
        self.old_pos = QPoint()
        self.resize_border_width = 5
        self.setup_ui()
        self.setMouseTracking(True)

    def setup_ui(self):
        self.setFixedHeight(30)
        self.setStyleSheet("""
            TitleBar {
                background-color: #2c3e50;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border: none;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 12px;
                font-weight: bold;
                            border: none;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                padding: 2px;
                margin: 0;
            }
            QPushButton:hover {
                background: rgba(130, 130, 130, 0.1);
                border-radius: 3px;
            }
            QPushButton#close_button:hover {
                background: #e74c3c;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(2)

        # Иконка приложения
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QIcon.fromTheme("document-edit").pixmap(16, 16))
        layout.addWidget(self.icon_label)

        # Название приложения
        self.title_label = QLabel("Финансовый менеджер")
        self.title_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        layout.addWidget(self.title_label)

        # Растягивающийся элемент
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Кнопки управления окном (уменьшенные)
        self.minimize_button = QPushButton()
        self.minimize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton))
        self.minimize_button.setFixedSize(22, 22)
        self.minimize_button.clicked.connect(self.parent.showMinimized)

        self.maximize_button = QPushButton()
        self.maximize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.maximize_button.setFixedSize(22, 22)
        self.maximize_button.clicked.connect(self.toggle_maximize)

        self.close_button = QPushButton()
        self.close_button.setObjectName("close_button")
        self.close_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        self.close_button.setFixedSize(22, 22)
        self.close_button.clicked.connect(self.parent.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.maximize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
        else:
            self.parent.showMaximized()
            self.maximize_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed and not self.parent.isMaximized():
            delta = QPoint(event.globalPos() - self.old_pos)
            self.parent.move(self.parent.pos() + delta)
            self.old_pos = event.globalPos()
        else:
            # Определяем границы для изменения размера
            rect = self.parent.rect()
            pos = event.pos()
            
            if (pos.x() <= self.resize_border_width and 
                pos.y() <= self.resize_border_width):
                self.setCursor(Qt.SizeFDiagCursor)
            elif (pos.x() >= rect.width() - self.resize_border_width and 
                  pos.y() >= rect.height() - self.resize_border_width):
                self.setCursor(Qt.SizeFDiagCursor)
            elif pos.x() <= self.resize_border_width:
                self.setCursor(Qt.SizeHorCursor)
            elif pos.x() >= rect.width() - self.resize_border_width:
                self.setCursor(Qt.SizeHorCursor)
            elif pos.y() <= self.resize_border_width:
                self.setCursor(Qt.SizeVerCursor)
            elif pos.y() >= rect.height() - self.resize_border_width:
                self.setCursor(Qt.SizeVerCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False
        self.setCursor(Qt.ArrowCursor)

    def mouseDoubleClickEvent(self, event):
        self.toggle_maximize()

    def resizeEvent(self, event):
        # Обновляем курсор при изменении размера
        pos = QCursor.pos() - self.parent.pos()
        rect = self.parent.rect()
        
        if (pos.x() <= self.resize_border_width or 
            pos.x() >= rect.width() - self.resize_border_width or
            pos.y() <= self.resize_border_width or 
            pos.y() >= rect.height() - self.resize_border_width):
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)