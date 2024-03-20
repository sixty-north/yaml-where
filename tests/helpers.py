def clean_yaml(s: str) -> str:
    lines = s.split("\n")
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())

    trimmed = [line[min_indent:] for line in lines]
    if trimmed[0] == "":
        trimmed = trimmed[1:]
    if trimmed[-1] == "":
        trimmed = trimmed[:-1]

    return "\n".join(trimmed)