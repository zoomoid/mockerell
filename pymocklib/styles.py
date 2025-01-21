from typing import Callable, Tuple
from pymocklib.transformers import from_double, to_alternating, to_alternating_alt, to_b, to_cc, to_clap, to_double, to_fraktur, to_interspersed_flag, to_lines, to_pray, to_pseudo_cyrillic, to_random, to_small_caps, to_space, to_square, to_strikethrough, to_sub_super, to_word_lines, sub
"""
All available flavors of this library exported
"""
styles: list[Tuple[str, Callable[[str], str]]] = [
    ("random", to_random),
    ("alternating", to_alternating),
    ("alternating2", to_alternating_alt),
    ("strikethrough", to_strikethrough),
    ("double", to_double),
    ("dedouble", from_double),
    ("smallcaps", to_small_caps),
    ("lower", str.lower),
    ("upper", str.upper),
    ("cyrillic", to_pseudo_cyrillic),
    ("fraktur", to_fraktur),
    ("subsuper", to_sub_super),
    ("cc", to_cc),
    ("b", to_b),
    ("pray", to_pray),
    ("clap", to_clap),
    ("cum", sub("cum", "😳")),
    ("sus", sub("sus", "😳")),
    ("space", to_space(1)),
    ("space2", to_space(2)),
    ("space3", to_space(3)),
    ("lines", to_lines),
    ("wordlines", to_word_lines),
    ("square", to_square),
    ("indian", to_interspersed_flag("🇮🇳")),
    ("turkish", to_interspersed_flag("🇹🇷"))
]

def style_doc(key: str) -> str:
    """
    maps a descriptive text to each style
    """
    match key:
        case "random": return "Flips lowercase characters pseudo-randomly into uppercase letters."
        case "alternating": return "Flips every second letter into an uppercase one, starting with the second character."
        case "alternating2": return "Like alternate, but ignores case in the input. Equivalent to lower|alternate."
        case "strikethrough": return "Turns the input into strikethrough using Unicode combinators (e̶x̶a̶m̶p̶l̶e̶)."
        case "double": return "Turns characters (latin letters and numbers) into their double-struck variants (𝕖𝕩𝕒𝕞𝕡𝕝𝕖). Also known as blackboard bold."
        case "dedouble": return "Turns double-struck characters (like from the \"double\" style) back into normal ones."
        case "smallcaps": return "Turns lowercase letters into small capitals."
        case "lower": return "Turns all characters into lowercase ones."
        case "upper": return "Turns all characters into UPPERCASE ones."
        case "cyrillic": return "Turns the text into a stereotypical fake russian looking variant."
        case "fraktur": return "Turns the input into 𝔉𝔯𝔞𝔨𝔱𝔲𝔯𝔰𝔠𝔥𝔯𝔦𝔣𝔱."
        case "subsuper": return "Alternatingly put letters into sub- and superscript, where possible."
        case "cc": return "Replaces all occurences of lowercase \"c\", \"ck\" and \"k\" with \"cc\"."
        case "b": return "Replaces all occurences of Bs (lower- and uppercase) with B-button emojis (🅱)."
        case "pray": return "Puts pray emojis (🙏) between all words."
        case "clap": return "Puts clap emojis (👏) between all words."
        case "cum": return "Replaces every occurence of 'cum' with 😳."
        case "sus": return "Replaces every occurence of 'sus' with 😳."
        case "space": return "Inserts a  s p a c e  between every two characters."
        case "space2": return "Inserts two   s  p  a  c  e  s   between every two characters."
        case "space3": return "Inserts three    s   p   a   c   e   s    between every two characters."
        case "lines": return "Puts each character on a single line."
        case "wordlines": return "Puts each word on a single line."
        case "square": return "Shows the input spaced in the first line and the tail of the input lined afterwards."
        case "indian": return "Replaces all vowels with the indian flag"
        case "turkish": return "Replaces all vowels with the turkish flag"
        case _: return "No documentation available."
