import unittest

from textnode import TextNode, TextType


class TextTestNode(unittest.TestCase):
    def testeq(self):
        node1 = TextNode("This is a TextNode", TextType.BOLD)
        node2 = TextNode("This is a TextNode", TextType.BOLD)
        self.assertEqual(node1, node2)

    def testnoteq(self):
        node1 = TextNode("This is a TextNode", TextType.ITALIC)
        node2 = TextNode("This is a TextNode", TextType.LINK)
        self.assertNotEqual(node1, node2)
        node3 = TextNode("This is a TextNode", TextType.BOLD)
        node4 = TextNode("This is a TextNode", TextType.BOLD)
        self.assertEqual(node3.text_type, node4.text_type)

    def testurl(self):
        node1 = TextNode("This is a TextNode", TextType.IMAGE, "https://img.com/1234")
        node2 = TextNode(
            "This is a TextNode", TextType.LINK, "https://www.newgg.com/home"
        )
        self.assertNotEqual(node1, node2)
        node3 = TextNode("This is a TextNode", TextType.BOLD)
        self.assertEqual(node3.url, None)


if __name__ == "__main__":
    unittest.main()
