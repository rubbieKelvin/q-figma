def text(string: str, tabs: int, newline=True) -> str:
    newline = "\n" if newline else ""
    return ("\t"*tabs) + string + newline
