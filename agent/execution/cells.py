"""Cell scripts: plain Python files split into cells by `# %%` lines (percent format)"""

MARKER = "# %%"


def split_cells(text: str) -> list[str]:
    """Cell bodies without markers; code before the first marker is a cell too"""
    chunks: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if line.startswith(MARKER):
            if current is not None:
                chunks.append(current)
            current = []
        else:
            if current is None:
                current = []
            current.append(line)
    if current is not None:
        chunks.append(current)
    bodies = ["\n".join(chunk).strip("\n") for chunk in chunks]
    return [body for body in bodies if body]


def join_cells(cells: list[str]) -> str:
    return "\n\n".join(f"{MARKER}\n{cell.strip(chr(10))}" for cell in cells) + "\n"
