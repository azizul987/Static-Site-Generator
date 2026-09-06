from xxlimited import new

from textnode import TextNode, TextType

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
