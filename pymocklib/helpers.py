import random

# helpers to polyfill haskell's vast Data.Text library with
# helper functions for various string operations, as well
# as adding iterators to polyfill capabilities of repeat
# note that python's functools technically provides a "repeat"
# function with capabilities for infinite iterators,
# though we could not get it to work as smoothly as implementing
# the two relevant iterators ourselfes

def intersperse(char: str, text: str) -> str:
    """
    The intersperse function takes a character and places it between the characters of a Text.
    """
    if char and text:
        return char.join(text[i:i+1] for i in range(0, len(text), 1))
    else:
        return text

def intercalate(glue: str, strings: list[str]) -> str:
    """
    Aliases Haskell's intercalate (which is just python's join) with join
    """
    return glue.join(strings)

def alternating_mask_iterator(n: int | None = None):
    """
    Creates an iterator that returns alternating booleans,
    either n times or infinite, if not specified
    """
    v = False
    i = 0
    while True:
        if n != None and i >= n:
            break
        yield v
        v = not v
        i += 1

def random_mask_iterator(seed, n: int | None = None):
    """
    Creates an iterator that, based on a seed, samples random booleans
    either n times or infinite, if not specified
    """
    random.seed(seed)
    i = 0
    while True:
        if n != None and i >= n:
            break
        yield not not random.getrandbits(1)
        i += 1
