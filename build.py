import os
import toml
import requests
import shutil

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from datetime import datetime
from rcssmin import cssmin

REDIRECTS_PATH = "redirects.toml"

TEMPLATE_FOLDER_PATH = "./template"
TEMPLATE_HTML = "index.j2"
TEMPLATE_CONF = "redirects.j2"
UNIA_CSS = "unia.css"

OUTPUT_FOLDER_PATH = "out"
RENDERED_HTML = "index.html"
RENDERED_CONF = "_redirects"
NEW_CSS_MIN = "new.min.css"
UNIA_CSS_MIN = "unia.min.css"


def parse_redirects():
    with open(REDIRECTS_PATH, "r", encoding="utf-8") as f:
        return toml.load(f)


def process_css():
    with open(os.path.join(OUTPUT_FOLDER_PATH, NEW_CSS_MIN), "wb") as f:
        f.write(
            requests.get(
                "https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.3/new.min.css"
            ).content
        )

    with open(UNIA_CSS, "r", encoding="utf-8") as source, open(
        os.path.join(OUTPUT_FOLDER_PATH, UNIA_CSS_MIN), "w", encoding="utf-8"
    ) as target:
        target.write(str(cssmin(source.read())))


def render_html(data, extensions=[], strict=False):
    env = Environment(
        loader=FileSystemLoader(os.path.basename(TEMPLATE_FOLDER_PATH)),
        extensions=extensions,
    )
    if strict:
        env.undefined = StrictUndefined

    env.globals["now"] = datetime.now().isoformat
    env.globals["len"] = len
    env.filters["anchor"] = lambda x: "".join(x.split()).lower()

    return env.get_template(TEMPLATE_HTML).render(data)


def render_conf(data, extensions=[], strict=False):
    env = Environment(
        loader=FileSystemLoader(os.path.basename(TEMPLATE_FOLDER_PATH)),
        extensions=extensions,
    )
    if strict:
        env.undefined = StrictUndefined

    return env.get_template(TEMPLATE_CONF).render(data)


def main():
    data = parse_redirects()
    if not os.path.isdir(OUTPUT_FOLDER_PATH):
        os.mkdir(OUTPUT_FOLDER_PATH)
    process_css()
    shutil.copyfile("favicon.svg", os.path.join(OUTPUT_FOLDER_PATH, "favicon.svg"))
    with open(
        os.path.join(OUTPUT_FOLDER_PATH, RENDERED_HTML), "w", encoding="utf-8"
    ) as f:
        f.write(render_html(data))

    with open(
        os.path.join(OUTPUT_FOLDER_PATH, RENDERED_CONF), "w", encoding="utf-8"
    ) as f:
        f.write(render_conf(data))


if __name__ == "__main__":
    main()
