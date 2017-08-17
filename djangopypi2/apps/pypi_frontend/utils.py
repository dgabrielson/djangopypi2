#######################
from __future__ import unicode_literals, print_function
#######################
def debug(func):
    # @debug is handy when debugging distutils requests
    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            import pdb
            pdb.pm()
    return _wrapped
