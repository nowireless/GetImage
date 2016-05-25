#!/usr/bin/env python

# getimage.py
#
# Copyright (C) 2016 Ryan Sjostrand
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

import urllib
import sys
import os

try:
    import praw
except ImportError:
    print("The 'praw' library is required")
    print("Install praw: pip install praw")
    sys.exit(-1)


def make_direct_imgur_link(image):
    return image.replace("gallery/", "").replace("/new", "") + ".jpg"


def download_image(image, dest):
    url = make_direct_imgur_link(image)
    urllib.urlretrieve(url, dest)


def get_arguments():
    if len(sys.argv) != 3:
        return None, None
    return sys.argv[1], sys.argv[2]


def print_license():
    print "This program is covered under the MIT license"
    print "Written by: Ryan Sjostrand"


def usage():
    print "Downloads the first hot image from a given subreddit"
    print "Usage: ./%s subreddit destination" % os.path.basename(__file__)


if __name__ == "__main__":
    print_license()
    subreddit, destination = get_arguments()
    if subreddit is None:
        usage()
        sys.exit(-1)

    if not ".jpg" in destination:
        destination += ".jpg"

    r = praw.Reddit(user_agent="linux")
    sub = r.get_subreddit(subreddit)

    print "Retrieving the top five posts for subreddit %s" % subreddit
    hot = sub.get_hot(limit=5)

    for submission in hot:
        if "imgur" in submission.url:
            download_image(submission.url, destination)
            print "Downloaded: %s, by %s" % (submission.title, submission.author)
            sys.exit(0)

    print "No found image in the top 5"
