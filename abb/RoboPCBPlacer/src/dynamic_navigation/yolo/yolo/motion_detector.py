#!/usr/bin/env python3


import cv2 as cv
import numpy as np
from threading import Thread

import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

from PyQt6.QtWidgets import QApplication

from .submodules.MainWindow import MainWindow
from .submodules.config import Config


clicked_points = []

mtx = np.array([[612.64599609375, 0, 327.8221130371094],
                [0, 611.58642578125, 234.41448974609375],
                [0, 0, 1]])

h, w = 480, 640


def init_app(motion_detector):
    app = QApplication([])
    window = MainWindow(motion_detector)
    window.show()
    app.exec()

class YoloRos(Node):
    def __init__(self):
        super().__init__('yolo')
        self.declare_parameters(namespace='', parameters=[('input_topic', ''),
                                                          ('output_topic', '')])
        self.input_topic_ = self.get_parameter('input_topic').value
        self.output_topic_ = self.get_parameter('output_topic').value
        self.subscription_ = self.create_subscription(
            Image, self.input_topic_, self.callback, 1
        )
        self.publisher_ = self.create_publisher(Image, self.output_topic_, 10)
        self.bridge_ = CvBridge()
        self.get_logger().info('Node initialized')
        self.cv_frame = None  # Для хранения последнего кадра

    def callback(self, msg):
        cv_frame = self.bridge_.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        cv_frame = cv.cvtColor(cv_frame, cv.COLOR_BGR2RGB)
        Config.FRAME = cv_frame
        # self.get_logger().info('ok')


def main(args=None):
    rclpy.init(args=args)
    motion_detector = YoloRos()

    # Создаем GUI в главном потоке
    app = QApplication([])
    window = MainWindow(motion_detector)

    window.show()

    # Запуск ROS в отдельном потоке
    ros_thread = Thread(target=rclpy.spin, args=(motion_detector,))
    ros_thread.start()

    # Запуск GUI
    app.exec()

    # Завершение
    ros_thread.join()
    motion_detector.destroy_node()
    rclpy.shutdown()
    cv.destroyAllWindows()
