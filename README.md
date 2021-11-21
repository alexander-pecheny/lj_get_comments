# LJ Get Comments

An utility to download comments from a Livejournal page programmatically.

## Installation

Install prerequisites: `pip install beautifulsoup4 requests html2text` before you run the program.

## Usage

```
usage: lj_get_comments.py [-h] --lj_url LJ_URL [--output OUTPUT] [--only_root]
                          [--only_author ONLY_AUTHOR] [--download_images]

optional arguments:
  -h, --help            show this help message and exit
  --lj_url LJ_URL, -u LJ_URL
  --output OUTPUT, -o OUTPUT
                        override auto-generated filename
  --only_root, -or      leave only root comments, not replies to them.
  --only_author ONLY_AUTHOR, -oa ONLY_AUTHOR
                        leave only comments by specified author
  --download_images, -di
                        download linked images from comments
```

Example: `python lj_get_comments.py -u 'https://monobor.livejournal.com/86642.html#comments' -or -oa monobor -di`
