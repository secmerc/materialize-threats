class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.top = y
        self.bottom = y + height
        self.left = x
        self.right = x + width

    def is_overlapping(self, inner):

        # TODO: make this handle any overlap case, inner or outer
        """      X
         0 1 2 3 4 
        -1    -----  <-- top
        -2    |   |
        -3    |   | <-- right
      Y -4    ----- <-- bottom
        """
        if self.top > inner.bottom or self.bottom < inner.top:
            return False
        if self.right < inner.left or self.left > inner.left:
            return False

        return True

    def x_ratio(self, search):
        if search < self.x:
            return 0
        elif search > self.x + self.width:
            return 1
        else:
            ratio = (search - self.x) / self.width
            return self._approx(ratio, 0.5, 0.1)

    def y_ratio(self, search):
        if search < self.y:
            return 0
        elif search > self.y + self.height:
            return 1
        else:
            ratio = (search - self.y) / self.height
            return self._approx(ratio, 0.5, 0.1)

    @staticmethod
    def _approx(value, center, delta):
        if abs(value - center) < delta:
            return center
        return value

    def to_dict_str(self):
        return {
            "x": str(self.x),
            "y": str(self.y),
            "width": str(self.width),
            "height": str(self.height),
        }
