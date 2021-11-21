#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import re
import html2text
import requests
from bs4 import BeautifulSoup

h2t = html2text.HTML2Text()
h2t.body_width = 0

def get_text(text):
    try:
        return h2t.handle(text)
    except:
        import pdb; pdb.set_trace()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lj_url", "-u", required=True)
    parser.add_argument("--output", "-o")
    parser.add_argument("--only_root", "-or", action="store_true")
    parser.add_argument("--only_author", "-oa")
    args = parser.parse_args()

    req = requests.get(args.lj_url)
    page = re.search("Site.page = (.+?);\n", req.text).group(1)
    page = json.loads(page)

    comments = page["comments"]
    if args.only_root:
        comments = [x for x in comments if not x["below"] and x["article"]]
    if args.only_author:
        comments = [x for x in comments if x["uname"] == args.only_author]
    texts = [get_text(x["article"]) for x in comments]
    output_file_name = args.output or re.sub("[^a-zA-Z0-9]", "_", args.lj_url) + ".txt"
    with open(output_file_name, "w", encoding="utf8") as f:
        f.write("\n\n".join(texts))


if __name__ == "__main__":
    main()
