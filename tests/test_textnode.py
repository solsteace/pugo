import unittest
from src.TextNode import TextNode

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
        plain_text = TextNode("Plain text", "text").to_leaf_node()
        bold_text = TextNode("Bold text", "bold").to_leaf_node()
        italic_text = TextNode("Italic text", "italic").to_leaf_node()
        code_block = TextNode("js\nconsole.log(1 == '1')", "code").to_leaf_node()

        self.assertEqual(plain_text.to_html(), "Plain text")
        self.assertEqual(bold_text.to_html(), "<b> Bold text </b>")
        self.assertEqual(italic_text.to_html(), "<i> Italic text </i>")
        self.assertEqual(code_block.to_html(), "<code> js\nconsole.log(1 == '1') </code>")

    def test_link_to_LeafNode(self):
        link_text = (TextNode("Chat with Bonzi Buddy today!", "link", "bonzibuddy.tk")
                        .to_leaf_node())
        self.assertEqual( 
            link_text.to_html(),
            '<a href="bonzibuddy.tk"> Chat with Bonzi Buddy today! </a>'
        )

    def test_image_to_LeafNode(self):
        image_text = (TextNode(None, "image", "https://i.kym-cdn.com/entries/icons/original/000/039/393/cover2.jpg")
                        .to_leaf_node())
        self.assertEqual( 
            image_text.to_html(), 
            '<img src="https://i.kym-cdn.com/entries/icons/original/000/039/393/cover2.jpg">  </img>'
        )


if __name__ == "__main__":
    unittest.main()