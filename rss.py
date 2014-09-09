import os
from datetime import datetime
from pytz import timezone

OUTPUT_DIR = '{}/{}/'.format(os.getcwd(), 'output')
CONTENT_DIR = '{}/{}/'.format(os.getcwd(), 'content')
DOMAIN = 'http://mattcamilli.com/'

BODY = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
  <title>Matt Camilli's Blog</title>
  <link>http://mattcamilli.com</link>
  <description>It's Something</description>
  <pubDate>{}</pubDate>
  {}
</channel>
</rss>
"""


ENTRY = """
<item>
<title>{}</title>
<link>{}</link>
<description>{}</description>
<pubDate>{}</pubDate>
</item>
"""


def _get_post_details(text):
    # Get Title
    details = []
    for item in ['Title', 'Slug', 'Description', 'Date']:
        i_start = text.find('{}:'.format(item))
        i_end = i_start + text[i_start:].find('\n')
        detail = text[i_start:i_end].replace('{}:'.format(item), '').strip()
        if item == 'Slug':
            detail = '{}{}.html'.format(DOMAIN, detail)
        details.append(detail.strip())
    return details


def rss():
    lastmod = timezone('US/Eastern').localize(
        datetime.now()).strftime('%Y-%m-%d')
    with open(OUTPUT_DIR + 'rss.xml', 'w') as feed:
        feed.seek(0)
        items = []
        files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
        for f in files:
            with open(CONTENT_DIR + f, 'r') as post:
                item = ENTRY.format(*_get_post_details(post.read()))
                items.append(item)

        feed.write(BODY.format(lastmod, '\n'.join(items)))
        feed.truncate()

if __name__ == '__main__':
    rss()
