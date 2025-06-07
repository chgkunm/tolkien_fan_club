import unittest

from block_mdparser import BlockType, block_to_block_type, markdown_to_blocks


class BlockMDParsertest(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_para(self):
        text = "This is a paragraph on a new line"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_block_to_heading1(self):
        text = "# This is a heading 1 on a new line"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_to_heading2(self):
        text = "## This is a heading 2 on a new line"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_to_heading3(self):
        text = "### This is a heading 3 on a new line"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_block_to_heading4(self):
        text = "#### This is a heading 4 on a new line"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)


if __name__ == "__main__":
    unittest.main()
