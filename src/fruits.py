class Fruit:
    def __init__(self):
        pass

    @property
    def icon(self):
        return self._icon


class Apple(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F34E"


class Banana(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F34C"


class Blueberry(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001FAD0"


class Kiwi(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F95D"


class Block(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001FAA8"


class Empty(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F532"
