from htmlnode import HtmlNode, LeafNode
from nodes_delimite import split_nodes_delimiter
from R import extract_markdown_images, extract_markdown_links
from nodes_delimite import split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, block_to_block_type
def test_htmlnode():
    node = HtmlNode("div", "Hello, World!", None, None)
    assert node.to_html() == "<div>Hello, World!</div>"
    assert node.props_to_html() == ""

    node = HtmlNode("div", "Hello, World!", None, {"class": "container"})
    assert node.props_to_html() == " class=container"

    node = HtmlNode("div", "Hello, World!", None, {"class": "container", "id": "main"})
    assert node.props_to_html() == " class=container id=main"

    node = HtmlNode("div", "Hello, World!", None, None)
    assert node.props_to_html() == ""

def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    node = LeafNode("p", "Hello, world!", {"class": "container"})
    self.assertEqual(node.to_html(), "<p class=container>Hello, world!</p>")

    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

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

def test_split_nodes_delimiter(self):
    node = TextNode("This is a text node", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], " ", TextType.BOLD)
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

def test_split_nodes_delimiter_with_multiple_parts(self):
    node = TextNode("This is a text node", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], " ", TextType.BOLD)
    self.assertEqual(len(new_nodes), 2)
    self.assertEqual(new_nodes[0].text_type, TextType.BOLD)
    self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_split_images(self):
    node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ],
        new_nodes,
    )

def test_split_links(self):
    node = TextNode(
        "This is text with a [link](https://www.example.com) and another [second link](https://www.example.com/second)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://www.example.com/second"),
        ],
        new_nodes,
    )

def test_text_to_textnodes(self):
    nodes = text_to_textnodes(
        "This is **text** with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
    )
    self.assertListEqual(
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        nodes,
    )

def test_markdown_to_blocks(self):
    blocks = markdown_to_blocks(
        "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\n\n"
    )
    self.assertListEqual(
        [],
        blocks,
    )

def test_block_to_block_type(self):
    self.assertEqual(
        BlockType.HEADING,
        block_to_block_type("# "),
    )
    self.assertEqual(
        BlockType.CODE,
        block_to_block_type("```"),
    )
    self.assertEqual(
        BlockType.QUOTE,
        block_to_block_type("> "),
    )
    self.assertEqual(
        BlockType.UNORDERED_LIST,
        block_to_block_type("* "),
    )
    self.assertEqual(
        BlockType.ORDERED_LIST,
        block_to_block_type("1. "),
    )
    self.assertEqual(
        BlockType.PARAGRAPH,
        block_to_block_type(""),
    )

def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )


def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
