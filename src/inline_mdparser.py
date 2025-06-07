from re import findall

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """split a list of textnodes into another list of nodes on the basis of the texttype provided;
    later used in a function"""
    if old_nodes:
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            split_nodes = []
            sections = node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown format, invalid input")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
        return new_nodes
    raise ValueError("Not a valid input")


def extract_markdown_images(text: str) -> list[str]:
    return findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[str]:
    return findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    """split a list of textnodes into another list of nodes if there is a image in the textnode;
    later used in a function"""
    if not old_nodes:
        raise ValueError("Not a valid input")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        all_images = extract_markdown_images(node.text)
        if not all_images:
            new_nodes.append(node)
            continue
        node_text = node.text
        for img_alt in all_images:
            alt_txt = node_text.split(f"![{img_alt[0]}]({img_alt[1]})", 1)
            if alt_txt[0] != "":
                new_nodes.extend(
                    [
                        TextNode(alt_txt[0], TextType.TEXT),
                    ]
                )
            new_nodes.append(TextNode(img_alt[0], TextType.IMAGE, img_alt[1]))
            node_text = alt_txt[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    """split a list of textnodes into another list of nodes if there is a link in the textnode;
    later used in a function"""
    if not old_nodes:
        raise ValueError("Not a valid input")
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        all_links = extract_markdown_links(node.text)
        if not all_links:
            new_nodes.append(node)
            continue
        node_text = node.text
        for link_alt in all_links:
            alt_txt = node_text.split(f"[{link_alt[0]}]({link_alt[1]})", 1)
            if alt_txt[0] != "":
                new_nodes.extend(
                    [
                        TextNode(alt_txt[0], TextType.TEXT),
                    ]
                )
            new_nodes.append(TextNode(link_alt[0], TextType.LINK, link_alt[1]))
            node_text = alt_txt[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    """form a text return a list of textnodes"""
    return split_nodes_images(
        split_nodes_links(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT)], "`", TextType.CODE
                    ),
                    "_",
                    TextType.ITALIC,
                ),
                "**",
                TextType.BOLD,
            )
        )
    )
