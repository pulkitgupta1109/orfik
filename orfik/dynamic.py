import os
import bottle
from collections import defaultdict
from datetime import datetime
import peewee as pw
import bottle_tools as bt
from playhouse.db_url import connect


db_url = os.environ.get("DATABASE_URL", "sqlite:///data.sqlite3")
protocol, db_url = db_url.split("://", 1)
if protocol == "postgres":
    protocol += "+pool"
db_url = protocol + "://" + db_url
db = connect(db_url)


class Visit(pw.Model):
    userhash = pw.CharField(max_length=512)
    username = pw.CharField()
    url = pw.CharField()
    timestamp = pw.DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


with db:
    db.create_tables([Visit])
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
def user_found_question(userHash: str, userName: str, url: str):
    Visit.create(userhash=userHash, username=userName, url=url)
    return {"ok": True}


@app.get("/lb")
def get_lb_details():
    sql = """
    select username, userhash, count(distinct url) as q_found, group_concat(timestamp)
    from visit
    group by userhash
    order by count(distinct url) desc, max(timestamp)
    """
    if "postgres" in protocol:
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
    cursor = db.execute_sql(sql)
    ranks = defaultdict(list)
    current_rank, last_qf = 0, float("inf")
    for name, hsh, qf, ts in cursor:
        if qf < last_qf:
            current_rank += 1
            last_qf = qf
        ranks[current_rank].append(
            {
                "userName": list(name[0]),
                "userHash": hsh[:5],
                "questionsFound": qf,
                "timestamps": list(ts),
            }
        )
    return {"rankings": ranks}


app = bt.add_cors(app)
