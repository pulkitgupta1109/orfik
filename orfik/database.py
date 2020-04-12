from playhouse.db_url import connect
import peewee as pw
import bottle_tools as bt


def build_db(db_url):
    db = None
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
    bt.common_kwargs.update({"Visit": Visit})
    return db
