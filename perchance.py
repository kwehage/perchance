#!/usr/bin/env python

import argparse
import yaml
import sys
import re
import random


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="user script")
    return parser.parse_args()


def random_choice(item, config):
    if item not in config:
        raise Exception(f"Item {item} not found in script")
    return config[item][random.randint(0, len(config[item]) - 1)]


def replace(script):
    s = script["output"]
    newstring = ''
    start = 0
    for m in re.finditer(r"\[(.*?)\]", s, re.MULTILINE):
        end, newstart = m.span()
        newstring += s[start:end]
        rep = random_choice(m.groups(0)[0], script)
        newstring += rep
        start = newstart
    newstring += s[start:]
    return newstring


if __name__ == "__main__":
    args = parse_args()
    script = None
    with open(args.script, "r") as f:
        try:
            script = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(-1)
    output = script.get("output", None)
    if not output:
        raise Exception("No 'output' block in yaml file")
    print(replace(script))
