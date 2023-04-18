#! /usr/bin/env python3

import re

def parse_plan(planfile):
    with open(planfile) as stream:
        lines = stream.readlines()
    plan = [act.strip() for act in lines[:-1]]
    total_cost = int(re.match(r"; cost = (\d+) \(.+ cost\)", lines[-1]).group(1))
    return plan, total_cost