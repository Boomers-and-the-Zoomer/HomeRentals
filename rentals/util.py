def escape(s, **kwargs):
    from html import escape

    return escape(str(s), **kwargs)


def dict_to_attr_string(dict: dict) -> str:
    string = ""
    for name, value in dict.items():
        if name == "klass":
            name = "class"
        if string != "":
            string += " "
        string += f'{escape(str(name))}="{escape(str(value))}"'
    return string


def dbg(value):
    import inspect
    from pprint import pformat
    from pathlib import Path

    parent_frame = inspect.currentframe().f_back
    frame_info = inspect.getframeinfo(parent_frame)
    pos = frame_info.positions
    line_number = parent_frame.f_lineno
    file_name = Path(parent_frame.f_code.co_filename).name
    expression = frame_info.code_context[0][pos.col_offset + 4 : pos.end_col_offset - 1]
    prefix = f"[{file_name}:{line_number}:{pos.col_offset}] "
    p = pformat(value, width=80 - len(prefix))
    p = f"\n[{ '=' * (len(prefix)-3)}] ".join(p.split("\n"))
    print(f"{prefix}{expression} = {p}")

    return value
