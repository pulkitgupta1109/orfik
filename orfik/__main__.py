import os
import argparse
from orfik import static, dynamic, questions, database

parser = argparse.ArgumentParser()
parser.add_argument("cmd")
parser.add_argument("--port", default=8080, type=int)
parser.add_argument("--api-base", default="https://orfikapi.herokuapp.com")
parser.add_argument("--target-dir", default="public")
parser.add_argument("--templates-dir", default="templates")
parser.add_argument("--questions-dir", default="questions")
args = parser.parse_args()

if args.cmd == "build":
    questions.questions_dir = args.questions_dir
    os.makedirs(args.target_dir, exist_ok=True)
    static.build(args)
elif args.cmd == "api":
    app = dynamic.build_app(database.build_db(os.environ.get("DATABASE_URL")))
    app.run(host="0.0.0.0", port=args.port)
