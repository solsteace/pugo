import unittest
from src.TextNode import TextNode, text_node_to_leaf_node

class TestTextNode(unittest.TestCase):
    def test_equality(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_inequality(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_text_to_LeafNode(self):
        plain_text = text_node_to_leaf_node(TextNode("Plain text", "text"))
        bold_text = text_node_to_leaf_node(TextNode("Bold text", "bold"))
        italic_text = text_node_to_leaf_node(TextNode("Italic text", "italic"))
        code_block = text_node_to_leaf_node(TextNode("js\nconsole.log(1 == '1')", "code"))

        self.assertEqual(plain_text.to_html(), "Plain text")
        self.assertEqual(bold_text.to_html(), "<b> Bold text </b>")
        self.assertEqual(italic_text.to_html(), "<i> Italic text </i>")
        self.assertEqual(code_block.to_html(), "<code> js\nconsole.log(1 == '1') </code>")

    def test_link_to_LeafNode(self):
        link_text = text_node_to_leaf_node(
            TextNode("Chat with Bonzi Buddy today!", "link", "bonzibuddy.tk")
        )
        self.assertEqual( 
            link_text.to_html(),
            '<a href="bonzibuddy.tk"> Chat with Bonzi Buddy today! </a>'
        )

    def test_image_to_LeafNode(self):
        image_text = text_node_to_leaf_node(
            TextNode(None, "image", "https://i.kym-cdn.com/entries/icons/original/000/039/393/cover2.jpg")
        )
        self.assertEqual( 
            image_text.to_html(), 
            '<img src="https://i.kym-cdn.com/entries/icons/original/000/039/393/cover2.jpg">  </img>'
        )


if __name__ == "__main__":
    unittest.main()