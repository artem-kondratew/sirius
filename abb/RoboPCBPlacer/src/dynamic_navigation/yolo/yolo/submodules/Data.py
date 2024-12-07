from .config import Config


class Component:

    def __init__(self, id : int, x : list, q : list) -> None:
        self.id = id
        self.x = x
        self.q = q
        self.available = False
        self.used = False

    def callback(self):
        if self.used:
            return
        Config.SELECTED_COMPONENT = self

    def update(self, x, q, available, used):
        self.x = x
        self.q = q
        self.available = available
        self.used = used

    def __str__(self) -> str:
        s = f'Component: id: {self.id}, x: {self.x}, q: {self.q}\n'
        return s


class Board:

    def __init__(self, id : int, x : list, q : list) -> None:
        self.id = id
        self.x = x
        self.q = q


class Data:

    def __init__(self, components : list, board : Board) -> None:
        self.components = components
        self.board = board

    def __str__(self) -> str:
        s = 'Components:\n'
        for i, c in enumerate(self.components):
            s += (f'\tc{i}: id: {c.id}, x: {c.x}, q: {c.q} ' + (f'place_id: {c.place_id}' if hasattr(c, 'place_id') else 'no_place_id') + '\n')
        if self.board is not None:
            s += f'Board: id: {self.board.id}, x: {self.board.x}, q: {self.board.q}'
        return s


if __name__ == '__main__':
    c1 = Component(2, [0.5, 3, 4], [0.7, 0, 0, 0.7])
    c2 = Component(3, [-1, 0, 7], [1, 2, 3, 4])

    board = Board(1, [2, -2, 5], [1, 0, 0, 1])

    data = Data([c1, c2], board)
