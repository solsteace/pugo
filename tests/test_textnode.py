import unittest
from src.TextNode import TextNode

class TestTextNode(unittest.TestCase):
    def test_equality(self):
        _ = "It should be able to correctly identify 'equal' `TextNode`"
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_inequality(self):
        _ = "It should be able to correctly identify 'different' `TextNode`"
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_text_to_LeafNode(self):
        cases = [
            (
                "It should handle `plain` text conversion to `LeafNode` and correctly display its html representation",
                ("Plain text", "text"), 
                "Plain text",
            ),
            (
                "It should handle `bold` text conversion to `LeafNode` and correctly display its html representation",
                ("Bold text", "bold"), 
                "<b> Bold text </b>" 
            ),
            (
                "It should handle `italic` text conversion to `LeafNode` and correctly display its html representation",
                ("Italic text", "italic"), 
                "<i> Italic text </i>"),
            (
                "It should handle `code` text conversion to `LeafNode` and correctly display its html representation",
                ("console.log(1 == '1')", "code"), 
                "<code> console.log(1 == '1') </code>"
            )
        ]

        for idx in range(len(cases)):
            _, args, expected = cases[idx]
            textNode = TextNode(*args).to_leaf_node()
            self.assertEqual(textNode.to_html(), expected)

    def test_link_to_LeafNode(self):
        _ = "It should add `href` attribute on html representation of `link` text type"
        link_text = (TextNode("Chat with Bonzi Buddy today!", "link", "bonzibuddy.tk")
                        .to_leaf_node())
        self.assertEqual( 
            link_text.to_html(),
            '<a href="bonzibuddy.tk"> Chat with Bonzi Buddy today! </a>'
        )

    def test_image_to_LeafNode(self):
        _ = "It should add `src` attribute on html representation of `image` text type"
        image_text = (TextNode(None, "image", "https://i.kym-cdn.com/entries/icons/original/000/039/393/cover2.jpg")
                        .to_leaf_node())
        self.assertEqual( 
            image_text.to_html(), 
            '<img src="https://i.kym-cdn.com/entries/icons/original/000/039/393/cover2.jpg">  </img>'
        )

if __name__ == "__main__":
    unittest.main()