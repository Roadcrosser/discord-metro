import re

emoji = re.compile(
    "("
    # Modifiers
    "[\uFE0F\uFE0E" # VS15 & VS16
    "\U0001F3FB-\U0001F3FF" # Fitzpatrick Scale
    "\u20E3" # Combining Enclosing Keycap
    
    # Mahjong Tiles
    "\U0001F004"
    
    # Emoticons
    # 80 Code Points, 80 Used, 80 Emoji
    "\U0001F600-\U0001F64F"
    
    # Dingbats
    # 192 Code Points, 192 Used, 33 Emoji
    # "\u2700-\u27BF|" # Entire Block
    "\u2702\u2705\u2708-\u270D\u270F\u2712\u2714\u2716"
    "\u271D\u2721\u2728\u2733-\u2734\u2744\u274C\u274E"
    "\u2753-\u2755\u2757\u2763-\u2764\u2795-\u2797"
    "\u27A1\u27B0\u27BF"
    
    # Transport and Map Symbols
    # 128 Code Points, 103 Used, 92 Emoji
    # "\U0001F680-\U0001F6FF|" # Entire block
    "\U0001F680-\U0001F6C5\U0001F6CB-\U0001F6D2"
    "\U0001F6E0-\U0001F6E5\U0001F6E9"
    "\U0001F6EB-\U0001F6EC\U0001F6F0"
    "\U0001F6F3-\U0001F6F6"
    
    # Miscellaneous Symbols
    # 256 Code Points, 256 Used, 80 Emoji
    # "\u2600-\u26FF|" # Entire block
    "\u2600-\u2604\u260E\u2611\u2614-\u2615\u2618"
    "\u261D\u2620\u2622-\u2623\u2626\u262A\u262E-\u262F"
    "\u2638-\u263A\u2640\u2642\u2648-\u2653\u2660"
    "\u2663\u2665-\u2666\u2668\u267B\u267F\u2692-\u2697"
    "\u2699\u269B-\u269C\u26A0-\u26A1\u26AA-\u26AB"
    "\u26B0-\u26B1\u26BD-\u26BE\u26C4-\u26C5\u26C8"
    "\u26CE-\u26CF\u26D1\u26D3-\u26D4\u26E9-\u26EA"
    "\u26F0-\u26F5\u26F7-\u26FA\u26FD"
    
    # Miscellaneous Symbols and Pictographs
    # 768 Code Points, 768 Used, 637 Emoji
    # "\U0001F300-\U0001F5FF|" # Entire Block
    "\U0001F300-\U0001F321\U0001F324-\U0001F393"
    "\U0001F396-\U0001F397\U0001F399-\U0001F39B"
    "\U0001F39E-\U0001F3F0\U0001F3F3-\U0001F3F5"
    "\U0001F3F7-\U0001F4FD\U0001F4FF-\U0001F53D"
    "\U0001F549-\U0001F54E\U0001F550-\U0001F567"
    "\U0001F56F-\U0001F570\U0001F573-\U0001F57A"
    "\U0001F587\U0001F58A-\U0001F58D"
    "\U0001F590\U0001F595-\U0001F596"
    "\U0001F5A4-\U0001F5A5\U0001F5A8"
    "\U0001F5B1-\U0001F5B2\U0001F5BC"
    "\U0001F5C2-\U0001F5C4\U0001F5D1-\U0001F5D3"
    "\U0001F5DC-\U0001F5DE\U0001F5E1"
    "\U0001F5E3\U0001F5E8\U0001F5EF\U0001F5F3"
    "\U0001F5FA-\U0001F5FF"
    
    # Supplemental Symbols and Pictographs
    # 256 Code Points, 82 Used, 80 Emoji
    # "\U0001F900-\U0001F9FF|" # Entire Block
    "\U0001F910-\U0001F91E\U0001F920-\U0001F927"
    "\U0001F930\U0001F933-\U0001F93A"
    "\U0001F93C-\U0001F93E\U0001F940-\U0001F945"
    "\U0001F947-\U0001F94B\U0001F950-\U0001F95E"
    "\U0001F980-\U0001F991\U0001F9C0"
    
    # Emoji Code Points in Other Blocks
    "\u2194-\u2199\u21A9-\u21AA" # Arrows (8)
    "\u3030\u303D" # CJK Symbols (2)
    "\u24C2" # Enclosed (1)
    "\U0001F170-\U0001F171\U0001F17E-\U0001F17F"
    "\U0001F18E\U0001F191-\U0001F19A"
    "\U0001F1E6-\U0001F1FF" # Enclosed Suppliment (41)
    "\u3297\u3299" # Enclosed CJK (2)
    "\U0001F201-\U0001F202\U0001F21A"
    "\U0001F22F\U0001F232-\U0001F23A"
    "\U0001F250-\U0001F251" # Enclosed Idographic (15)
    "\u203C\u2049" # General Punctuation (2)
    "\u25AA-\u25AB\u25B6\u25C0\u25FB-\u25FE" # Shapes (8)
    "\u2B05-\u2B07\u2B1B-\u2B1C\u2B50\u2B55" # Misc Symbols (7)
    "\u231A-\u231B\u2328\u23CF\u23E9-\u23F3"
    "\u23F8-\u23FA" # Misc Technical (18)
    "\u2934\u2935]" # Arrow Suppliment B (2)
    ")", re.UNICODE
)

def clean_emoji(text):
    return emoji.sub(r"\\\1", text) if emoji.search(text) else text