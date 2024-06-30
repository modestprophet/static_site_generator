import unittest
from block_markdown import (
    markdown_to_block,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ordered_list,
    block_type_unordered_list
)


class TestBlockMakrdown(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        markdown_blocks = markdown_to_block(markdown)
        self.assertListEqual(
            ["This is **bolded** paragraph",
             "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
             "* This is a list\n* with items"
             ],
            markdown_blocks
        )

    def test_so_many_newlines_to_blocks(self):
        markdown = """
This is the first paragraph.
Maybe it has some `code` in it.





This second paragraph follows after like, a half a dozen newlines.
"""
        markdown_blocks = markdown_to_block(markdown)
        self.assertListEqual(
            ["This is the first paragraph.\nMaybe it has some `code` in it.",
             "This second paragraph follows after like, a half a dozen newlines."],
            markdown_blocks
        )



    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)


if __name__ == "__main__":
    unittest.main()

