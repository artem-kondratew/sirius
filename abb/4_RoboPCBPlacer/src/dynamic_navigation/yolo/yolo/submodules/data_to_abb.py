import socket

from .Data import Component, Board, Data
import time


def test_send_data_to_abb(data : Data, logger=None):
    logger.info(f'test_send_data_to_abb checker:\n{data}')

def send_data_to_abb(data : Data , ip="192.168.125.1", port=5000, logger=None):
    """
    Отправляет данные через TCP/IP сокет.
    :param data: Строка данных в формате "x;y;z;qw;qx;qy;qz"
    :param ip: IP-адрес робота
    :param port: Порт TCP
    """
    #[[[1,2,3],[1,0,0,0]], [comp1], [wobj2]

    data.board.x = list(data.board.x)
    data.board.x.append(0)
    data.board.q = list(data.board.q)
    for i, x in enumerate(data.board.x):
        data.board.x[i] = round(x, 4) * 1000
    for i, q in enumerate(data.board.q):
        logger.info(f'{i} {data.board.q[i]}')
        data.board.q[i] = round(q, 4)
        logger.info(f'{i} {data.board.q[i]}')
    str_board = f'[{data.board.id},[{data.board.x},{data.board.q}]]'
    logger.info(f'{str_board}')

    str_list = []
    for comp in data.components:
        comp.x = list(comp.x)
        comp.x.append(0)
        for i, x in enumerate(comp.x):
            comp.x[i] = round(x, 4) * 1000
        for i, q in enumerate(comp.q):
            comp.q[i] = round(q, 4)
        string = f"[{comp.place_id},{list(comp.x)},{list(comp.q)}]"
        str_list.append(string)
        logger.info(string)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            t = 0.2
            s.connect((ip, port))
            time.sleep(t)
            s.sendall(str_board.encode('utf-8'))
            time.sleep(t)
            for comp in str_list:
                s.sendall(comp.encode('utf-8'))
                time.sleep(t)
            s.close()
        except:
            logger.warn('sending error')
