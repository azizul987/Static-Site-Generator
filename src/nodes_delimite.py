from tkinter.constants import E
from xxlimited import new

from textnode import TextNode, TextType

from enum import Enum

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
        if node.text_type == TextType.TEXT:
            text = node.text
            if delimiter in text:
                parts = text.split(delimiter)
                for i, part in enumerate(parts):
                    new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            if "!" in text:
                parts = text.split("!")
                for i, part in enumerate(parts):
                    new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text = node.text
            if "[" in text:
                parts = text.split("[")
                for i, part in enumerate(parts):
                    new_nodes.append(TextNode(part, TextType.TEXT if i % 2 == 0 else text_type))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text:str):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks=markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    if block.startswith("# "):
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
