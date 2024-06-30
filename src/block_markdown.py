block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_block(markdown):
    blocks = markdown.split("\n\n")  # split on double newlines to separate blocks
    blocks = [block.strip() for block in blocks]  # strip leading/trailing whitespace from each block
    blocks = [block for block in blocks if block]  # remove empty blocks
    return blocks

def block_to_block_type(block):
    if block.startswith("#"):
        return block_type_heading
    elif block.startswith("```"):
        return block_type_code
    elif block.startswith(">"):
        return block_type_quote
    elif block.startswith(("*", "-")):
        return block_type_unordered_list
    elif block.startswith(("1. ", "2. ", "3. ")):
        return block_type_ordered_list
    else:
        return block_type_paragraph

