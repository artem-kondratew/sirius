import copy

from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from .config import Config
from .ClickableLable import ClickableLabel
from .Data import Component


class Board:

    def __init__(self, central_widget, main_window : QMainWindow, id):
        self.id = id
        self.central_widget = central_widget
        self.main_window = main_window
        self.wrap = QLabel(self.central_widget)
        self.hide()
        self.x = None
        self.q = None

        self.wrap.setStyleSheet(f'background-color: rgb{Config.BOARDS_COLOR};')
        self.board_label = QLabel(self.wrap)
        self.aruco_label = QLabel(self.wrap)

        self.places = [None for _ in range(Config.COMPONENTS_ON_BOARD)]
        
        self.restore_places()

        self.available_ids = (((0, 4), (1, 3), (2, 5)),
                              ((2, 5), (0, 4), (1, 3)),
                              ((0, 4), (1, 3), (2, 5)))

    def restore_places(self):
        for place in self.places:
            if place is None:
                continue
            place.used = False
            place.canvas.setStyleSheet(f'background-color: rgb{(255, 0, 0)};')
            place.canvas.hide()

        for i in range(Config.COMPONENTS_ON_BOARD):

            def create_callback(idx):
                def callback():
                    component = Config.SELECTED_COMPONENT
                    if not component:
                        return
                    for place in self.places:
                        if place.id == component.id:
                            return
                        if not component.id in self.available_ids[self.id][idx]:
                            return
                    self.places[idx].id = component.id
                    self.places[idx].x = component.x
                    self.places[idx].q = component.q
                    self.places[idx].place_id = idx
                    self.places[idx].canvas.setStyleSheet(f'background-color: rgb{(0, 255, 0)};')
                    Config.SELECTED_COMPONENT.used = True
                    Config.SELECTED_COMPONENT = None
                return callback
                    
            place = Component(None, None, None)
            place.canvas = ClickableLabel(parent=self.wrap, callback=create_callback(i))
            place.canvas.setStyleSheet(f'background-color: rgb{(255, 0, 0)};')
            self.places[i] = place

            self.resize()
        
    def resize(self):
        main_w = self.main_window.geometry().width()
        main_h = self.main_window.geometry().height()        
        
        wrap_w = int(main_w * Config.BOARD_W)
        wrap_h = wrap_w
        wrap_x = int(main_w * Config.BOARD_X)
        wrap_y = int((main_h - wrap_h) / 2)
        self.wrap.setGeometry(wrap_x, wrap_y, wrap_w, wrap_h)

        self.clicks = (((0.095, 0.68), (0.69, 0.45), (0.46, 0.1)),
                       ((0.48, 0.055), (0.61, 0.51), (0.08, 0.54)),
                       ((0.414, 0.06), (0.68, 0.459), (0.062, 0.452)))

        for i, place in enumerate(self.places):
            if place is None:
                continue
            x = int(self.clicks[self.id][i][0] * wrap_w)
            y = int(self.clicks[self.id][i][1] * wrap_w)
            w = int(0.02 * wrap_w)
            h = int(0.02 * wrap_w)
            place.canvas.setGeometry(x, y, w, h)

        pixmap = QPixmap(f'/home/robot/abb/src/dynamic_navigation/yolo/aruco/5x5_1000-{self.id}.jpg')
        pixmap_board = QPixmap(f'/home/robot/abb/src/dynamic_navigation/yolo/boards/motherboard_{self.id}.png')
        
        aruco_w = int(0.2 * wrap_w)
        self.aruco_label.setGeometry(0, 0, aruco_w, aruco_w)
        self.board_label.setGeometry(0, 0, wrap_w, wrap_w)
        scaled_pixmap = pixmap.scaled(self.aruco_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        scaled_pixmap_board = pixmap_board.scaled(self.board_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.board_label.setPixmap(scaled_pixmap_board)
        self.aruco_label.setPixmap(scaled_pixmap)

    def show(self):
        self.wrap.show()

    def hide(self):
        self.wrap.hide()

    def __str__(self):
        s = f'Board: id: {self.id}, x: {self.x}, q: {self.q}\n'
        for place in self.places:
            s += ('\t' + place.__str__())
        return s
    
    def update(self, id, x, q):
        self.id = id
        self.x = x
        self.q = q

    def get_board_pose(self) -> str:
        return str(self.x) + ' ' + str(self.q) + '\n'
    
    def get_place_pose(self, idx):
        return str(self.places[idx].x) + ' ' + str(self.places[idx].q) + '\n'
    
    def is_full(self, node):
        if self.id is None:
            node.get_logger().info(f'null id: {self.id}')
            return False
        
        for place in self.places:
            if place.id is None or place.x is None or place.q is None:
                node.get_logger().info(f'null place: {place.id}, {place.x}, {place.q}')
                return False
            
        return True
