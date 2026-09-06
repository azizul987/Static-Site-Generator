from htmlnode import HtmlNode, LeafNode
from nodes_delimite import split_nodes_delimiter
from R import extract_markdown_images, extract_markdown_links
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
