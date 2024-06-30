# import unittest

# from htmlnode import HTMLNode, LeafNode


# class TestHTMLNode(unittest.TestCase):
#     def test_eq(self):
#         child = HTMLNode("p", "Heading")
#         node = HTMLNode("a", "Linky", child, {"href": "https://www.boot.dev"})
#         node2 = HTMLNode("a", "Linky", child, {"href": "https://www.boot.dev"})
#         self.assertEqual(node, node2)
# 
#     def test_props(self):
#         node = HTMLNode(tag="a", value="Linky", props={"href": "https://www.google.com", "target": "_blank"})
#         self.assertEqual(
#             ' href="https://www.google.com" target="_blank"', node.props_to_html()
#         )
# 
#     def test_repr(self):
#         node = HTMLNode(tag="a", value="Linky", props={"href": "https://www.boot.dev"})
#         self.assertEqual(
#             "HTMLNode(a, Linky, None, {'href': 'https://www.boot.dev'})", repr(node)
#         )
import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node = LeafNode(value="Linky", tag="a", props={"href": "https://www.boot.dev"})
        self.assertEqual(
            "LeafNode(a, Linky, {'href': 'https://www.boot.dev'})", repr(node)
        )

    def test_no_value(self):
        node = LeafNode(value=None, tag="a", props={"href": "https://www.boot.dev"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html(self):
        node = LeafNode(value="Click me!", tag="a", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click me!</a>')

if __name__ == "__main__":
    unittest.main()
