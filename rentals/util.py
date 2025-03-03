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
