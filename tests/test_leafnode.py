import unittest
from src.LeafNode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_html_attributes(self):
        # No attribute, no tag
        node = LeafNode(value="Lorem ipsum sit dolor amet")
        self.assertEqual(node.to_html(), "Lorem ipsum sit dolor amet")

        # No attribute
        node = LeafNode(value="Lorem ipsum sit dolor amet", tag="p")
        self.assertEqual(node.to_html(), "<p> Lorem ipsum sit dolor amet </p>")

        # 1 attribute
        node = LeafNode(
            value="Google it!", 
            tag="a",
            attributes= {
                "href": "www.google.com",
            }
        )
        self.assertEqual(
            node.to_html(), 
            '<a href="www.google.com"> Google it! </a>'
        )

        # n attributes, n > 1
        node = LeafNode(
            value="Google it!", 
            tag="a",
            attributes= {
                "href": "www.google.com",
                "target": "_blank"
            }
        )
        self.assertEqual(
            node.to_html(), 
            '<a href="www.google.com" target="_blank"> Google it! </a>'
        )

if __name__ == "__main__":
    unittest.main()