import unittest
from src.TextNode import (
    TextNode,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_by_delimiter,
    split_links_on_nodes,
)

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

    def test_extract_images(self):
        cases = [
            (
                "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")],
            ),
            (
                "![](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("image", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")]
            ),
            (
                "![image]()",
                [("image", "image", "")]
            ),
            (
                "![](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [
                    ("image", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    ("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
                ]
            ),
        ]

        for case in cases:
            extracted_link = extract_markdown_images(case[0])
            self.assertEqual(extracted_link, case[1])

    def test_extract_hyperlinks(self):
        cases = [
            (
                "[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")],
            ),
            (
                "[](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("link", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")]
            ),
            (
                "[link]()",
                [("link", "link", "")]
            ),
            (
                "[](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [
                    ("link", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    ("link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
                ]
            ),
        ]

        for case in cases:
            extracted_link = extract_markdown_links(case[0])
            self.assertEqual(extracted_link, case[1])

    def test_split_links(self):
        cases = [
            (
                "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)",
                [
                    TextNode("This is ", "text"),
                    TextNode("text", "bold"),
                    TextNode(' with an ', "text", None),
                    TextNode('italic', "italic", None),
                    TextNode(' word and a ', "text", None),
                    TextNode('code block', "code", None),
                    TextNode(' and an ', "text", None),
                    TextNode('image', "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode('and a ', "text", None),
                    TextNode('link', "link", "https://boot.dev")
                ]
            ),
            (
                "![Marcianito](https://i.pinimg.com/736x/5b/49/fc/5b49fc68ece025aeb6cb8b8cd56fdf29.jpg) **ATTENTION** to *everyone* to see for `this lil fella` and [learn more here](www.google.com)",
                [
                    TextNode('Marcianito', "image", "https://i.pinimg.com/736x/5b/49/fc/5b49fc68ece025aeb6cb8b8cd56fdf29.jpg"),
                    TextNode("ATTENTION", "bold"),
                    TextNode(" to ", "text"),
                    TextNode('everyone', "italic", None),
                    TextNode(' to see for ', "text", None),
                    TextNode('this lil fella', "code", None),
                    TextNode(' and ', "text", None),
                    TextNode('learn more here', "link", "www.google.com")
                ]
            ),
        ]

        for case in cases:
            # print(f"\nTesting for: `{case[0]}`")
            result = split_nodes_by_delimiter(
                split_nodes_by_delimiter(
                    split_nodes_by_delimiter(
                        split_links_on_nodes([TextNode(case[0], "text")]), '**'
                    ), '*'
                ) , '`'
            )

            #print(result)
            for idx in range(len(result)):
                self.assertEqual(result[idx], case[1][idx])


if __name__ == "__main__":
    unittest.main()