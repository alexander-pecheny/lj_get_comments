#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import re
import os
import html2text
import requests
from bs4 import BeautifulSoup

h2t = html2text.HTML2Text()
h2t.body_width = 0


def generate_name(url, ext):
    return re.sub("[^a-zA-Z0-9]", "_", url) + ext


def get_text(text, args):
    soup = BeautifulSoup(text, "html.parser")
    for tag in soup.find_all("img"):
        tag.insert_before(tag["src"])
        if args.download_images:
            url, ext = os.path.splitext(tag["src"])
            filename = generate_name(url, ext)
            with open(filename, "wb") as f:
                f.write(requests.get(tag["src"]).content)
        tag.extract()
    for tag in soup.find_all("b"):
        tag.unwrap()
    for tag in soup.find_all("span", {"class": "lj-spoiler-head"}):
        tag.extract()
    result = h2t.handle(str(soup))
    result = re.sub("([0-9])\\\\.", "\\1.", result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lj_url", "-u", required=True)
    parser.add_argument("--output", "-o", help="override auto-generated filename")
    parser.add_argument("--only_root", "-or", action="store_true", help="leave only root comments, not replies to them.")
    parser.add_argument("--only_author", "-oa", help="leave only comments by specified author")
    parser.add_argument("--download_images", "-di", action="store_true", help="download linked images from comments")
    args = parser.parse_args()

    req = requests.get(args.lj_url)
    page = re.search("Site.page = (.+?);\n", req.text).group(1)
    page = json.loads(page)

    comments = page["comments"]
    if args.only_root:
        comments = [x for x in comments if not x["below"] and x["article"]]
    if args.only_author:
        comments = [x for x in comments if x["uname"] == args.only_author]
    texts = [get_text(x["article"], args) for x in comments]
    output_file_name = args.output or generate_name(args.lj_url, ext=".txt")
    with open(output_file_name, "w", encoding="utf8") as f:
        f.write("\n\n".join(texts))


if __name__ == "__main__":
    main()
