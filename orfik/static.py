import os
import logging
from hashlib import sha512
from pathlib import Path

import htmlmin
from jinja2 import Environment, FileSystemLoader, Template
from orfik.questions import questions


def build(templates_dir="templates", target="public"):
    target = Path(target)
    env = Environment(loader=FileSystemLoader(templates_dir))
    html = env.get_template("index.html").render()
    with open(target / "index.html", "w") as fl:
        fl.write(htmlmin.minify(html))
    # ---------------
    previous_hashes = [sha512("orfik".encode()).hexdigest()]
    for q in questions:
        tpl = env.get_template("question.html")
        html = htmlmin.minify(tpl.render(q=q))
        for previous_hash in previous_hashes:
            with open(target / f"{previous_hash}.html", "w") as fl:
                fl.write(html)
        previous_hashes = [sha512(ans.encode()).hexdigest() for ans in q.answers]
    # ----------------
