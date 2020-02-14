import os
import argparse
from orfik import static

parser = argparse.ArgumentParser()
parser.add_argument("cmd")
parser.add_argument("--api-base", default="https://orfikapi.compsoc.club")
parser.add_argument("--target-dir", default="public")
parser.add_argument("--templates-dir", default="templates")
args = parser.parse_args()

if args.cmd == "build":
    os.makedirs(args.target_dir, exist_ok=True)
    static.build(args)
