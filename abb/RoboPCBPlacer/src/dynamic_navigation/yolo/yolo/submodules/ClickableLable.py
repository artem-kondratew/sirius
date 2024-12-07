from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt


class ClickableLabel(QLabel):

    def __init__(self, text='', parent=None, object=None, callback=None):
        if parent:
            super().__init__(text, parent)
        else:
            super().__init__(text)
        self.object = object
        self.callback = callback

    def mousePressEvent(self, event, callback=None):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.object:
                self.object.callback()
                return
            if self.callback:
                self.callback()
