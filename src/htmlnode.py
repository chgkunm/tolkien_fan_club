from textnode import TextNode, TextType


class HTMLNode:
    """parent class; class to define a html tag"""

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """implemented in a child class"""
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self) -> str:
        """return a string of the props value"""
        if self.props is not None:
            new_str = ""
            for key in self.props:
                new_str += f' {key}="{self.props[key]}"'
            return new_str
        return ""

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"Element:{self.tag},Content:{self.value},\n    Children: {self.children},\nProperties: {self.props}\n"


class LeafNode(HTMLNode):
    """child class of HTMLNode; a html tag that doesn't have any children"""

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return f"{self.value}"
        if self.value is None:
            raise ValueError("All LeafNodes must have values")
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """child class of HTMLNode; a html tag that have children"""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All ParentNodes must have a tag")
        if self.children is None:
            raise ValueError("All ParentNodes must have a child/children")
        new_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            new_str += child.to_html()
        new_str += f"</{self.tag}>"
        return new_str


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """check the type of textnode and return a appropriate leafnode"""
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Not a valid TextType")
