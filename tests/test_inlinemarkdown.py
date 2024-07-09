import unittest
from src.TextNode import TextNode
from src.InlineMarkdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_by_delimiter,
    split_links_on_nodes,
)

class TestInlineMarkdown(unittest.TestCase):
    def test_extract_images(self):
        cases = [
            (
                "It should handle `image` text type consists of the url and alt text",
                "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")],
            ),
            (
                "It should handle `image` text type consists only the url",
                "![](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("image", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")]
            ),
            (
                "It should handle `image` text type consists only the alt text",
                "![image]()",
                [("image", "image", "")]
            ),
            (
                "It should handle multiple `image` text type in one string",
                "![](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [
                    ("image", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    ("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
                ]
            ),
        ]

        for idx in range(len(cases)):
            _, args, expected = cases[idx]
            extracted_link = extract_markdown_images(args)
            self.assertEqual(extracted_link, expected)

    def test_extract_hyperlinks(self):
        cases = [
            (
                "It should handle `link` text type consists of the url and alt text",
                "[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")],
            ),
            (
                "It should handle `link` text type consists only the url",
                "[](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [("link", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")]
            ),
            (
                "It should handle `link` text type consists only the alt text",
                "[link]()",
                [("link", "link", "")]
            ),
            (
                "It should handle multiple `link` text type in one string",
                "[](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                [
                    ("link", "", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    ("link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
                ]
            ),
        ]

        for idx in range(len(cases)):
            _, args, expected = cases[idx]
            extracted_link = extract_markdown_links(args)
            self.assertEqual(extracted_link, expected)

    def test_split_links(self):
        _ = "It should correctly split raw text with a mix of `text`, `bold`, `italic`, `image`, and `link` text type"
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
            result = split_nodes_by_delimiter(
                split_nodes_by_delimiter(
                    split_nodes_by_delimiter(
                        split_links_on_nodes([TextNode(case[0], "text")]), '**'
                    ), '*'
                ) , '`'
            )

            for idx in range(len(result)):
                self.assertEqual(result[idx], case[1][idx])
    
if __name__ == "__main__":
    unittest.main()