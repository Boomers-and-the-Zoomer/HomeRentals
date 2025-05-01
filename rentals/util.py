from urllib.parse import quote, unquote, urlsplit

from bottle import request, response


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


def get_return_url_or(default="/"):
    return_to = request.query.get("return-to")
    if return_to == None:
        return default
    return return_to


def chain_return_url(url_str):
    return_to = request.query.get("return-to")
    if return_to == None:
        return url_str
    return construct_return_url(url_str, return_to).geturl()


def push_return(url_to, url_from=None):
    if url_from != None:
        p = urlsplit(url_from)
    else:
        p = request.urlparts
    return_to = p.path
    if p.query != "":
        return_to += "?" + p.query
    return_to = quote(return_to)

    to = construct_return_url(url_to, return_to)

    response.status = 303
    response.add_header("Location", to.geturl())


def construct_return_url(url_to, return_to):
    to = urlsplit(url_to)
    query = to.query
    if query != "":
        query += "&"
    query += f"return-to={return_to}"
    to = to._replace(query=query)
    return to


def pop_return(default="/"):
    return_to = request.query.get("return-to", "")
    if return_to != "":
        return_to = unquote(return_to)
    else:
        return_to = default

    response.status = 303
    response.add_header("Location", dbg(return_to))


def error(msg: str, target_id="error-target"):
    response.add_header("HX-Retarget", f"#{target_id}")
    response.add_header("HX-Reswap", "outerHTML")
    return f"""
        <div class="error-msg"
             id="{target_id}"
             hx-on:htmx:load='document.querySelectorAll(".error-msg").forEach((elem, _, __) => {{ if (elem.id != "{target_id}") {{ elem.innerHTML = "" }} }})'
        >
             {msg}
        </div>"""


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
