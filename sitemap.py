import os
from datetime import datetime
from pytz import timezone

HEADER = """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">"""
OUTPUT_DIR = '{}/{}/'.format(os.getcwd(), 'output')
DOMAIN = 'http://mattcamilli.com/'

ENTRY = """
<url>
<loc>{}</loc>
<lastmod>{}</lastmod>
</url>
"""


def sitemap():
    lastmod = timezone('US/Eastern').localize(datetime.now()).isoformat()
    with open(OUTPUT_DIR + 'sitemap.xml', 'w') as sitemap:
        sitemap.seek(0)
        sitemap.write(HEADER)
        dirs = os.walk(OUTPUT_DIR)
        for folder in dirs:
            files = folder[2]
            folder_name = folder[0].replace(OUTPUT_DIR, '')
            folder_name = folder_name + '/' if folder_name else folder_name
            for f in files:
                if f.endswith('.html'):
                    f = '' if f == 'index.html' else f
                    loc = '{}{}{}'.format(DOMAIN, folder_name, f)
                    sitemap.write(ENTRY.format(loc, lastmod))
        sitemap.write('</urlset>')
        sitemap.truncate()

if __name__ == '__main__':
    sitemap()
