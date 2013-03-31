"""
Named HTML entities are much easier to comprehend than numeric entities. This
module helps convert between the more typical numerical entiies and the more
attractive named entities.
"""

# Primarily a packaging of Ian Beck's work from
# http://beckism.com/2009/03/named_entities_python/

# Given the many little differences between Python 2 and Python 3 string handling
# syntax and symantics, easier to have two very similar, parallel implementations.
# They are multiplexed here into one logical ``namedentities`` package.

import sys
if sys.version_info[0] >= 3:
    from namedentities.namedentities3 import named_entities, encode_ampersands
else:
    from namedentities.namedentities2 import named_entities, encode_ampersands
