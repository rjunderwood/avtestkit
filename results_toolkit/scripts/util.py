


import os

def path_slash():
    if os.name == 'nt':
        return "\\"
    else:
        return "/"