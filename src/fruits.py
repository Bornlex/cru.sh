class Fruit:
    def __init__(self):
        pass

    @property
    def icon(self):
        return self._icon


class GreenApple(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F34F"

    
class RedApple(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F34E"


class Pineapple(Fruit):
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F34D"


class Banana(Fruit):
    """
    This icon does not take the same space as others, so better not to use it for now.
    """
    def __init__(self):
        super().__init__()
        self._icon = "\U0001F34C"


class Blueberry(Fruit):
    """
    This icon does not take the same space as others, so better not to use it for now.
    """
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
