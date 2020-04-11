import os
from pathlib import Path
from collections import namedtuple

questions_dir = None
Question = namedtuple("Question", "number statement image answers")


def get_questions():
    questions = []
    qlist_dir = Path(questions_dir)
    for qno in sorted(os.listdir(qlist_dir), key=lambda x: int(x)):
        qpath = qlist_dir / qno
        statement, image, answers = "", None, []
        for fname in os.listdir(qpath):
            if fname.strip() == "answers.txt":
                with open(qpath / fname, "r") as fl:
                    answers += [line.strip().lower() for line in fl.readlines()]
            elif fname.strip() == "statement.txt":
                with open(qpath / fname, "r") as fl:
                    statement = fl.read().strip()
            elif "image" in fname.strip():
                image = qpath / fname
        if statement and answers:
            yield Question(qno, statement, image, answers)
