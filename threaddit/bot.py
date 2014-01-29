# -*- coding: utf-8 -*-
# ThreadditBot functions.

from urlparse import urlparse
from markdown.inlinepatterns import LINK_RE

import argparse
import re

import praw


def get_submission_id_from_url(url):
    """Parse and return the submission ID from the Reddit URL."""

    parsed = urlparse(url)
    if parsed.netloc != 'www.reddit.com' or not parsed.path:
        return None
    dirs = parsed.path.split('/')
    if len(dirs) < 5:
        return None
    return dirs[4]


def get_submission_id():
    """Parse URL from CLI and return submission ID."""

    # FIXME make CLI configurable and give method better name
    parser = argparse.ArgumentParser(
        description='Threadit links - extract links from Reddit thread.')
    parser.add_argument('url')
    args = parser.parse_args()

    submission_id = get_submission_id_from_url(args.url)
    if submission_id is None:
        raise Exception('Given URL %s could not be parsed.' % args.url)

    return submission_id


def fetch_submission():
    """Fetch thread from Reddit."""

    r = praw.Reddit('Comment link extractor 1.0 by u/ThreaditBot see '
                    'https://praw.readthedocs.org/en/latest/'
                    'pages/comment_parsing.html')
    return r.get_submission(submission_id=get_submission_id())


def get_comments(submission, limit=None, threshold=0):
    """Return comments from submission.

    More comment links are expanded if no limit is given this may take long.
    """

    submission.replace_more_comments(limit=limit, threshold=threshold)
    return praw.helpers.flatten_tree(submission.comments)


def extract_urls(md):
    """Extract absolute URLs from markdown and return list of URLs."""

    urls = re.findall(LINK_RE, md)
    if urls:
        urls = [u[7].strip() for u in urls]

    return urls


def test_get_submission_id_from_url():
    url = 'http://www.reddit.com/r/AskReddit/comments/1w6ixc/what_is_the_best_website_that_nobody_knows_about/'
    assert '1w6ixc' == get_submission_id(url)