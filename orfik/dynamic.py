import bottle
from collections import defaultdict
from datetime import datetime
import peewee as pw
import bottle_tools as bt

db = pw.SqliteDatabase("data.sqlite3", pragmas={"journal_mode": "off"})


class Visit(pw.Model):
    userhash = pw.CharField(max_length=512)
    username = pw.CharField()
    url = pw.CharField()
    timestamp = pw.DateTimeField(default=datetime.utcnow)

    class Meta:
        database = db


db.connect()
db.create_tables([Visit])
app = bottle.Bottle()


@app.post("/userFoundQuestion")
@bt.fill_args
def user_found_question(userHash: str, userName: str, url: str):
    Visit.create(userhash=userHash, username=userName, url=url)
    return {"ok": True}


@app.get("/lb")
def get_lb_details():
    cursor = db.execute_sql(
        """
    select username, userhash, count(distinct url) as q_found, group_concat(timestamp)
    from visit
    group by userhash
    order by count(distinct url) desc, max(timestamp)
    """
    )
    ranks = defaultdict(list)
    current_rank, last_qf = 0, float("inf")
    for name, hsh, qf, ts in cursor:
        if qf < last_qf:
            current_rank += 1
            last_qf = qf
        ranks[current_rank].append(
            {
                "userName": name,
                "userHash": hsh[:5],
                "questionsFound": qf,
                "timestamps": ts,
            }
        )
    return {"rankings": ranks}


app = bt.add_cors(app)
