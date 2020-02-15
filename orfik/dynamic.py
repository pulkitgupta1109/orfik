import bottle
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


@bt.fill_args
@app.post("/userFoundQuestion")
def user_found_question(userHash: str, userName: str, url: str):
    Visit.create(userhash=userHash, username=userName, url=url)
    return ""


@app.get("/lb")
def get_lb_details():
    cursor = db.execute_sql(
        """
    select username, userhash, count(url) as q_found, group_concat(timestamp)
    from visit
    group by userhash
    order by count(url) desc, max(timestamp)
    """
    )
    ranks = []
    current_rank, last_qf = 0, float("inf")
    for name, hsh, qf, ts in cursor:
        if qf < last_qf:
            current_rank += 1
            last_qf = qf
        ranks.append(
            {
                "userName": name,
                "userHash": hsh[:5],
                "questionsFound": qf,
                "timestamps": ts,
                "rank": current_rank,
            }
        )
    return {"rankings": ranks}
