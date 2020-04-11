import os
import argparse
from orfik import static, dynamic, questions

parser = argparse.ArgumentParser()
parser.add_argument("cmd")
parser.add_argument("--port", default=8080, type=int)
parser.add_argument("--api-base", default="https://orfikapi.compsoc.club")
parser.add_argument("--target-dir", default="public")
parser.add_argument("--templates-dir", default="templates")
parser.add_argument("--questions-dir", default="questions")
args = parser.parse_args()

if args.cmd == "build":
    questions.questions_dir = args.questions_dir
    os.makedirs(args.target_dir, exist_ok=True)
    static.build(args)
elif args.cmd == "api":
    dynamic.app.run(host="0.0.0.0", port=args.port)
