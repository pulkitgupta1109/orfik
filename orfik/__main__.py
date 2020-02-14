import os
import argparse
from orfik import static

parser = argparse.ArgumentParser()
parser.add_argument("cmd")
args = parser.parse_args()

if args.cmd == "build":
    os.makedirs("public", exist_ok=True)
    static.build()
