#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Extracts URLs from a given Reddit thread.

from bot import fetch_submission, get_comments

import re
import shelve


# Simple regex for markdown URLs.
re_md_link = re.compile(r'\(([^\)]+)\)')
re_schema = re.compile(r'https?://')

submission = fetch_submission()
comments = get_comments(submission)

# shelve doesn't support unicode keys
sub_id = submission.id.encode('utf-8')

d = shelve.open('cache/urls.data', writeback=True)
if sub_id not in d:
    d[sub_id] = {'urls': set(), 'comment_ids': set()}

for comment in comments:
    if comment.id in d[sub_id]['comment_ids'] or getattr(comment, 'body', None) is None:
        continue

    print('Parsing comment %s' % comment.id)

    urls = re.findall(re_md_link, comment.body)
    if urls:
        urls = filter(lambda s: re.search(re_schema, s), urls)

    if not urls:
        continue

    d[sub_id]['urls'].update(urls)
    d[sub_id]['comment_ids'].add(comment.id)

d.sync()
d.close()