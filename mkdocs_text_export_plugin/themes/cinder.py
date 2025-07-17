from bs4 import BeautifulSoup


def get_stylesheet() -> str:
    return ""


def modify_html(html: str, href: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    sm_wrapper = soup.new_tag("small")

    a = soup.new_tag("a", href=href, title="Text export", download=None)
    a["class"] = "txt-download"
    a.string = "Open text"

    sm_wrapper.append(a)
    if soup.body:
        footer = getattr(soup.body, "footer", None)
        if footer:
            footer.insert(0, sm_wrapper)

    return str(soup)
