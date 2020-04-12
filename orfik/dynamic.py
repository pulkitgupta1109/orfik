import bottle
from collections import defaultdict
from datetime import datetime
import bottle_tools as bt


def build_app(db):
    app = bottle.Bottle()

    @app.hook("before_request")
    def _connect_db():
        db.connect()

    @app.hook("after_request")
    def _close_db():
        if not db.is_closed():
            db.close()

    @app.post("/userFoundQuestion")
    @bt.fill_args
    def user_found_question(userHash: str, userName: str, url: str, Visit):
        Visit.create(userhash=userHash, username=userName, url=url)
        return {"ok": True}

    @app.get("/lb")
    def get_lb_details():
        sql = """
        select
          array_agg(distinct username),
          userhash,
          count(distinct url) as q_found,
          array_agg(timestamp)
        from
          visit
        group by
          userhash
        order by
          count(distinct url) desc,
          max(timestamp)
        """
        ranks = defaultdict(list)
        current_rank, last_qf = 0, float("inf")
        for name, hsh, qf, ts in db.execute_sql(sql):
            if qf < last_qf:
                current_rank += 1
                last_qf = qf
            ranks[current_rank].append(
                {
                    "userName": name[0],
                    "userHash": hsh[:5],
                    "questionsFound": qf,
                    "timestamps": [str(t) for t in ts],
                }
            )
        return {"rankings": ranks}

    app = bt.add_cors(app)
    return app
