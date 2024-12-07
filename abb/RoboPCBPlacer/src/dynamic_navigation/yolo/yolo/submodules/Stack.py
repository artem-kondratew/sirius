from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

from .config import Config
from .Data import Component
from .ClickableLable import ClickableLabel


YELLOW = (246, 241, 169)
RED = (246, 169, 180)
BLUE = (177, 169, 246)

COMPONENTS_MAIN_WRAP_COLOR = (240, 240, 240)
COMPONENTS_WRAPS_COLORS = [RED, RED, BLUE, BLUE, YELLOW, YELLOW]


class Stack:

    def __init__(self, central_widget, main_window : QMainWindow):
        self.central_widget = central_widget
        self.main_window = main_window
        self.wrap = QWidget(self.central_widget)
        self.createStack(COMPONENTS_MAIN_WRAP_COLOR)
        self.hide()

    def createStack(self, wrap_color):
        self.wrap.setStyleSheet(f'background-color: rgb{wrap_color};')

        self.stack = []

        for i in range(Config.COMPONENTS_NUM):
            component = Component(i, None, None)
            component.canvas = ClickableLabel(parent=self.wrap, object=component)
            self.stack.append(component)

        self.resize()
        
    def resize(self):
        main_w = self.main_window.geometry().width()
        main_h = self.main_window.geometry().height()
        
        wrap_x = int(main_w * Config.STACK_X)
        wrap_y = int(main_h * Config.STACK_Y)
        wrap_w = int(main_w * Config.STACK_W)
        wrap_h = int(main_h * Config.STACK_H)
        self.wrap.setGeometry(wrap_x, wrap_y, wrap_w, wrap_h)

        scale = 0.99
        w = int(scale * wrap_w)
        h = int(scale * wrap_h / Config.COMPONENTS_NUM)
        x = int(0.5 * (1 - scale) * wrap_w)
        y = int(0.5 * (1 - scale) * wrap_h)

        self.resize_items(x, y, w, h)

        for i, component in enumerate(self.stack):
            pixmap = QPixmap(f'/home/robot/abb/src/dynamic_navigation/yolo/components/Aim{i}')
            if not component.available:
                image = pixmap.toImage().convertToFormat(QImage.Format.Format_Grayscale8)
                pixmap = QPixmap.fromImage(image)
                component.canvas.setStyleSheet(f'background-color: rgb{(0, 0, 0)};')
            else:
                component.canvas.setStyleSheet(f'background-color: rgb{COMPONENTS_WRAPS_COLORS[i]};')
            scaled_pixmap = pixmap.scaled(component.canvas.size(), Qt.AspectRatioMode.KeepAspectRatio)
            component.canvas.setPixmap(scaled_pixmap)

    def resize_items(self, x, y, w, h):
        dy = 0
        h -= 1
        for i, component in enumerate(self.stack):
            component.canvas.setGeometry(x, int(y + dy + i * h), w, h)
            dy += 1

    def show(self):
        self.wrap.show()
        for component in self.stack:
            component.canvas.show()

    def hide(self):
        self.wrap.hide()
        for component in self.stack:
            component.canvas.hide()
