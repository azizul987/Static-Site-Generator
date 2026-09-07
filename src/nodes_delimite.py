import re
from enum import Enum

from textnode import TextNode, TextType
from htmlnode import HtmlNode, LeafNode, ParentNode, text_node_to_html_node
from R import extract_markdown_images, extract_markdown_links


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown, unmatched delimiter: {delimiter}")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        for alt, url in images:
            before, text = text.split(f"![{alt}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        for anchor, url in links:
            before, text = text.split(f"[{anchor}]({url})", 1)
            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks


def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("* ") or block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    text = block[4:-3]  # buang ```\n di depan dan ``` di belakang
    code_leaf = LeafNode(None, text)
    return ParentNode("pre", [ParentNode("code", [code_leaf])])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(content))


def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]  # buang "- " / "* "
        html_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.split(". ", 1)[1]  # buang "1. ", "2. ", dst
        html_items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", html_items)


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", text_to_children(paragraph))


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        else:
            children.append(paragraph_to_html_node(block))
    return ParentNode("div", children)


def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block.startswith("# "):
            return block[2:].strip()
    raise ValueError("No title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(template)
