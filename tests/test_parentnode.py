import unittest
from src.LeafNode import LeafNode
from src.ParentNode import ParentNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_single_child(self):
        _ = "It should correctly handle a single child"
        parent = ParentNode([LeafNode("Hell World", tag="p")], tag="div")
        self.assertEqual(parent.to_html(), '<div><p>Hell World</p></div>')

    def test_to_html_n_child(self):
        _ = "It should handle child with various tag and attributes",
        parent = ParentNode(
            [ 
                LeafNode("Lorem ipsum", tag="p"), 
                LeafNode(
                    "Sit dolor amet", 
                    tag="p",
                    attributes = {
                        "class" : "some__class",
                        "style" : "font-size: 16px"
                    }
                )
            ],
            tag="div",
            attributes= { "width": "100%" }
        )

        self.assertEqual(
            parent.to_html(),
            "".join([
                '<div width="100%">',
                    '<p>Lorem ipsum</p>',
                    '<p class="some__class" style="font-size: 16px">Sit dolor amet</p>',
                '</div>',
            ])
        )

    def test_to_html_nesting(self):
        _ = "It should handle nested child with various tag and attributes",
        parentl2 = ParentNode(
            [
                LeafNode("Insert text", tag="p"),
                LeafNode(
                    "Bottom text", 
                    tag="p",
                    attributes= { "style": "font-family: impact" }
                )
            ],
            tag="div",
            attributes= {
                "class": "content__text",
                "style": "display: flex"
            }
        )

        parentl1 = ParentNode(
            [parentl2, LeafNode("Another bottom text", tag="p")],
            tag="section",
            attributes = { "style": "border: 1px solid black" }
        )

        parent = ParentNode( [parentl1 ], tag="body")

        self.assertEqual(
            parent.to_html(),
            "".join([
                '<body>',
                    '<section style="border: 1px solid black">',
                        '<div class="content__text" style="display: flex">',
                            '<p>Insert text</p>',
                            '<p style="font-family: impact">Bottom text</p>',
                        '</div>',
                        '<p>Another bottom text</p>',
                    '</section>',
                '</body>'
            ])
        )

if __name__ == "__main__":
    unittest.main()