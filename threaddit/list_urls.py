#!/usr/bin/env python
# -*- coding: utf-8 -*-
# List saved URLs for a given Reddit thread.

from bot import get_submission_id

import shelve


sub_id = get_submission_id()

d = shelve.open('cache/urls.data')

print '\n'.join(d[sub_id]['urls'])

d.close()