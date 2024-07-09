import unittest
from src.BlockMarkdown import (
    get_block_type,
    markdown_to_blocks,
    markdown_to_html
)

class TestBlockMarkdown(unittest.TestCase):
    def test_split_blocks(self):
        cases = [
            (
                "It should handle a single block",
                """ A single block contains a single paragraph """,
                [ ["A single block contains a single paragraph"] ]
            ),
            (
                "It should handle multiple blocks",
                """
                    This is **bolded** paragraph

                    This is another paragraph with *italic* text and `code` here
                    This is the same paragraph on a new line

                    * This is a list
                    * with items
                """,
                [
                    ["This is **bolded** paragraph"],
                    [
                        "This is another paragraph with *italic* text and `code` here",
                        "This is the same paragraph on a new line"
                    ],
                    [
                        "* This is a list", 
                        "* with items"
                    ]
                ]
            ),
            (
                "It should handle multiple blocks",
                """
                    # This is a heading

                    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                    * This is a list item
                    * This is another list item
                """,
                [
                    ["# This is a heading"],
                    ["This is a paragraph of text. It has some **bold** and *italic* words inside of it."],
                    [
                        "* This is a list item",
                        "* This is another list item"
                    ]
                ]
            ),
        ]

        for idx in range(len(cases)):
            _, args, expected = cases[idx]
            self.assertEqual(markdown_to_blocks(args), expected)

    def test_detect_block_type(self):
        cases = [
            (
                "It should handle a single block",
                """ A single block contains a single paragraph """,
                [ "paragraph" ]
            ),
            (
                "It should handle multiple blocks",
                """
                    This is **bolded** paragraph

                    This is another paragraph with *italic* text and `code` here
                    This is the same paragraph on a new line

                    * This is a list
                    * with items
                """,
                ["paragraph", "paragraph", "unordered_list" ]
            ),
            (
                "It should handle multiple blocks",
                """
                    # This is a heading

                    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                    * This is a list item
                    * This is another list item
                """,
                [ "heading_1", "paragraph", "unordered_list" ]
            ),
        ]

        for idx in range(len(cases)):
            _, args, expected = cases[idx]
            block_types = list(map(lambda b: get_block_type(b[0]), markdown_to_blocks(args)))
            self.assertEqual(block_types, expected)
    
    def test_markdown_to_html(self):
        _ = "It should properly handle conversion from raw markdown to html"
        markdown = """
            ## Hello

            This is **bolded** paragraph

            This is another paragraph with *italic* text and `code` here
            This is the same paragraph on a new line

            * *This* is a list
            * with **items**

            > Lorem ipsum sit dolor amet asjklasja asd adas
            > Lorem ipsum sit dolor amet asjklasja asd adas
            > Lorem ipsum sit dolor amet asjklasja asd adas

            ```
            Lorem 
            ipsum 
            sit 
            dolor 
            amet
            ```
        """
        expected = [
            "<div> <h2> Hello </h2> </div>",
            "<div> This is  <b> bolded </b>  paragraph </div>",
            "<div> This is another paragraph with  <i> italic </i>  text and  <code> code </code>  here This is the same paragraph on a new line </div>",
            "<div> <ul> <li> <i> This </i>  is a list </li> <li> with  <b> items </b> </li> </ul> </div>",
            "<div> <blockquote> Lorem ipsum sit dolor amet asjklasja asd adas Lorem ipsum sit dolor amet asjklasja asd adas Lorem ipsum sit dolor amet asjklasja asd adas </blockquote> </div>",
            "<div> <pre><code> Lorem\nipsum\nsit\ndolor\namet </code></pre> </div>",
        ]

        self.assertEqual(markdown_to_html(markdown), expected)

if __name__ == "__main__":
    unittest.main()