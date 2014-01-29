#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Extracts URLs from a given Reddit thread.

from bot import fetch_submission, get_comments, extract_urls

import shelve


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

    urls = extract_urls(comment.body)
    if not urls:
        continue

    d[sub_id]['urls'].update(urls)
    d[sub_id]['comment_ids'].add(comment.id)

d.sync()
d.close()