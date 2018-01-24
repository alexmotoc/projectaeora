from __future__ import print_function
import json

class Share:
    def __init__(self, code, name, current, price, diff, per_diff):
        self.code = code
        self.name = name
        self.current = current
        self.price = price
        self.diff = diff
        self.per_diff = per_diff

    def get_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return '{}, {}, {}, {}, {}, {}'.format(
                self.code, self.name, self.current,
                self.price, self.diff, self.per_diff)
