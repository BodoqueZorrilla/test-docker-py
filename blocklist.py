""""
blocklist.py

This file just contains the blocklist of the JWT tokens.
It will be imported by app and the logut resource so that tokens can be added to the blocklist when
the users logs out.
"""

BLOCK_LIST = set()