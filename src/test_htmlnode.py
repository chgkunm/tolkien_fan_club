import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

nodes = [
    TextNode("This is a Italics TextNode", TextType.ITALIC),
    TextNode("This is a Link TextNode", TextType.LINK, "https://www.worldwideweb.com"),
    TextNode("This is a Bold TextNode", TextType.BOLD),
    TextNode("This is a TextNode", TextType.TEXT),
]


class HTMLTestNode(unittest.TestCase):
    def testeq1(self):
        htmlnode1 = HTMLNode("h1", nodes[3])
        htmlnode2 = HTMLNode("h1", nodes[3])
        self.assertEqual(htmlnode1, htmlnode2)

    def testeq2(self):
        htmlnode1 = HTMLNode("li", nodes[0])
        htmlnode2 = HTMLNode("ul", None, [htmlnode1, htmlnode1])
        htmlnode3 = HTMLNode("p", nodes[3], [htmlnode2], {"color": "red"})
        htmlnode4 = HTMLNode("p", nodes[3], [htmlnode2], {"color": "red"})
        self.assertEqual(htmlnode3, htmlnode4)

    def testnoteq(self):
        htmlnode1 = HTMLNode("a", nodes[2], None, {"color": "lightblue"})
        imagenode = TextNode(
            "This is a Image TextNode", TextType.IMAGE, "https://worldwideweb.com/icon"
        )
        htmlnode2 = HTMLNode("a", nodes[2], None, {"text-decoration": "none"})
        htmlnode3 = HTMLNode("a", imagenode, None, {"text-decoration": "none"})
        self.assertNotEqual(htmlnode1, htmlnode2)
        self.assertNotEqual(htmlnode2, htmlnode3)

    def test_props_to_html(self):
        htmlnode = HTMLNode(
            "a",
            nodes[2],
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            htmlnode.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_parent_to_html(self):
        parentnode1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            parentnode1.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
        )

    def test_nested_parent_to_html(self):
        listnode = LeafNode("li", "list item")
        unorderedlist = ParentNode(
            "ul", [listnode, listnode, listnode], {"list-style-type": "circle"}
        )
        orderedlist = ParentNode(
            "ol", [unorderedlist, unorderedlist], {"list-style-type": "upper-roman"}
        )
        self.assertEqual(
            orderedlist.to_html(),
            '<ol list-style-type="upper-roman"><ul list-style-type="circle"><li>list item</li><li>list item</li><li>list item</li></ul><ul list-style-type="circle"><li>list item</li><li>list item</li><li>list item</li></ul></ol>',
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italics(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode(
            "This is a text node", TextType.LINK, "https://www.worldwideweb.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://www.worldwideweb.com"})

    def test_image(self):
        node = TextNode(
            "This is a text node",
            TextType.IMAGE,
            "https://www.worldwideweb.com/icon.png",
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://www.worldwideweb.com/icon.png",
                "alt": "This is a text node",
            },
        )


if __name__ == "__main__":
    unittest.main()
