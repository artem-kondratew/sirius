from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QMessageBox
from PyQt6.QtGui import QFont, QFontMetrics

from .camera import get_data
from .config import Config
from .Stack import Stack
from .Board import Board as MainBoard
from .Data import Data
from .data_to_abb import send_data_to_abb, test_send_data_to_abb


class MainWindow(QMainWindow):
    def __init__(self, node=None):
        super().__init__()

        self.node = node

        self.setWindowTitle('RoboPCBPlacer')

        self.setMinimumSize(QSize(640, 480))
        self.showMaximized()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.add_main_buttons()
        self.components_stack = Stack(self.central_widget, self)

        self.boards = []
        for i in range(Config.BOARDS_NUM):
           self.boards.append(MainBoard(self.central_widget, self, i))

        self.detected = False

    def add_main_buttons(self):
        self.buttons = list()
        y = 0

        detect_button_text = 'Detect'
        detect_button = QPushButton(detect_button_text, self.central_widget)
        detect_button.clicked.connect(self.on_detect_button_click)
        self.buttons.append({
            'object': detect_button,
            'text' : detect_button_text,
            'width': Config.MAIN_BUTTONS_SCALE_X, 
            'height': Config.MAIN_BUTTONS_SCALE_Y,
            'x' : 0,
            'y' : y})
        y += Config.MAIN_BUTTONS_SCALE_Y

        go_button_text = 'Go'
        go_button = QPushButton(go_button_text, self.central_widget)
        go_button.clicked.connect(self.on_go_button_click)
        self.buttons.append({
            'object': go_button,
            'text' : go_button_text,
            'width': Config.MAIN_BUTTONS_SCALE_X,
            'height': Config.MAIN_BUTTONS_SCALE_Y,
            'x' : 0,
            'y' : y})
        y += Config.MAIN_BUTTONS_SCALE_Y

        reset_button_text = 'Reset'
        reset_button = QPushButton(reset_button_text, self.central_widget)
        reset_button.clicked.connect(self.on_reset_button_click)
        self.buttons.append({
            'object': reset_button,
            'text' : reset_button_text,
            'width': Config.MAIN_BUTTONS_SCALE_X,
            'height': Config.MAIN_BUTTONS_SCALE_Y,
            'x' : 0,
            'y' : y})
        y += Config.MAIN_BUTTONS_SCALE_Y

        exit_button_text = 'Exit'
        exit_button = QPushButton(exit_button_text, self.central_widget)
        exit_button.clicked.connect(self.on_exit_button_click)
        self.buttons.append({
            'object': exit_button,
            'text' : exit_button_text,
            'width': Config.MAIN_BUTTONS_SCALE_X,
            'height': Config.MAIN_BUTTONS_SCALE_Y,
            'x' : 0,
            'y' : y})
        y += Config.MAIN_BUTTONS_SCALE_Y

        self.buttons_font = QFont()
        self.buttons_font.setPointSize(20)

        for button in self.buttons:
             button['object'].setFont(self.buttons_font)
        

    def elide_text(self, fm, text, available_width):
        elided_text = text
        while fm.horizontalAdvance(elided_text) > available_width and len(elided_text) > 0:
            elided_text = elided_text[:-1]
        return elided_text + '...'

    def resizeEvent(self, event):
        super().resizeEvent(event)

        w = self.geometry().width()
        h = self.geometry().height()

        if hasattr(self, 'buttons'):
            for button in self.buttons:
                button_width = int(w * button['width'])
                button_height = int(h * button['height'])

                button['object'].setFixedSize(button_width, button_height)
                button['object'].move(int(w * button['x']), int(h * button['y']))

                text = button['text']
                fm = QFontMetrics(self.buttons_font)
                available_width = button_width - 20

                if fm.horizontalAdvance(text) > available_width:
                    truncated_text = self.elide_text(fm, text, available_width)
                    button['object'].setText(truncated_text)
                else:
                    button['object'].setText(text)

        if hasattr(self, 'components_stack'):
            self.components_stack.resize()

        if hasattr(self, 'boards'):
            for board in self.boards:
                board.resize()

    def on_detect_button_click(self):
        self.on_reset_button_click()
        if Config.FRAME is None:
            return
        data = get_data(Config.FRAME, self.node.get_logger())
        if data is None or data.board is None:
            self.node.get_logger().info(f'empty {data}')
            return
        self.components_stack.show()
        if Config.SELECTED_BOARD is not None:
            Config.SELECTED_BOARD.hide()
        Config.SELECTED_BOARD = self.boards[data.board.id]
        Config.SELECTED_BOARD.update(data.board.id, data.board.x, data.board.q)
        Config.SELECTED_BOARD.show()
        for component in data.components:
            self.components_stack.stack[component.id].update(component.x, component.q, available=True, used=False)
            self.components_stack.resize()
        self.detected = True
        self.node.get_logger().info(f'{data}')
        print('board_wrap', self.boards[0].wrap.geometry())
        print('board_aruco', self.boards[0].aruco_label.geometry())

    def on_go_button_click(self):
        if not self.detected:
            return
        board : MainBoard = Config.SELECTED_BOARD
        if not board.is_full(self.node):
            self.node.get_logger().info(f'{board}')
            reply = QMessageBox.question(
                self,
                'Error',
                'Board info is empty',
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok
            )
            if reply == QMessageBox.StandardButton.Ok:
                return
        cool_data = Data(components=board.places, board=board)
        send_data_to_abb(cool_data, logger=self.node.get_logger())
        with open('/home/robot/abb/result.txt', 'w') as file:
            file.write(board.get_board_pose())
            for i in range(Config.COMPONENTS_ON_BOARD):
                file.write(board.get_place_pose(i))
        reply = QMessageBox.question(
            self,
            'Info',
            'Task is sent successfully',
            QMessageBox.StandardButton.Ok,
            QMessageBox.StandardButton.Ok
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.on_reset_button_click()

    def on_reset_button_click(self):
        if not self.detected:
            return
        self.detected = False
        self.components_stack_shown = False
        self.components_stack.hide()
        self.components_stack_shown = False
        print(Config.SELECTED_BOARD)
        Config.SELECTED_COMPONENT = None
        Config.SELECTED_BOARD = None
        for board in self.boards:
            board.hide()
            board.restore_places()

    def on_exit_button_click(self):
        reply = QMessageBox.question(
            self,
            'Exit Confirmation',
            'Do you really want to exit now?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def save_changes(self):
        pass
