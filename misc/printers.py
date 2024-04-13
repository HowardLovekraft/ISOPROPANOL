from icecream import ic # FOR DEBUG ONLY


def state_printer(text: str, max_len: int, alive_expr="WORKS", fillchar="."):
    return text.ljust(max_len, fillchar) +" --> " + alive_expr


class StatePrinter:
    def __init__(self, max_len: int, alive_expr="WORKS", fillchar="."):
        self._alive_expr = alive_expr
        self.max_len = max_len
        self._fillchar = fillchar

    def print_status(self, text: str) -> str:
        return text.ljust(self.max_len, self._fillchar) + " --> " + self._alive_expr
