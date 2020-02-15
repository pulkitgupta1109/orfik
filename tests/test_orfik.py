from orfik import __version__
from orfik.dynamic import user_found_question, get_lb_details

ufq = user_found_question
lb = get_lb_details


def test_version():
    assert __version__ == "0.1.0"


def test_lb():
    ufq("uh1", "uh", "q1")
    ufq("uh2", "uh", "q1")
    ranks = lb()["rankings"]
    uh1 = [u["rank"] for u in (ranks) if u["userHash"] == "uh1"][0]
    uh2 = [u["rank"] for u in (ranks) if u["userHash"] == "uh2"][0]
    assert uh1 == uh2
    ufq("uh3", "uh3", "q1")
    ufq("uh3", "uh3", "q2")
    ranks = lb()["rankings"]
    uh1 = [u["rank"] for u in (ranks) if u["userHash"] == "uh1"][0]
    uh2 = [u["rank"] for u in (ranks) if u["userHash"] == "uh2"][0]
    uh3 = [u["rank"] for u in (ranks) if u["userHash"] == "uh3"][0]
    assert uh3 < uh1 and uh1 == uh2
