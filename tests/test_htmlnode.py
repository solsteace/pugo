import unittest
from src.HTMLNode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_html_attributes(self):
        # No attribute
        node = HTMLNode()
        self.assertEqual( node.attributes_to_html(), "")

        # 1 attribute
        node = HTMLNode(attributes={
            "href": "www.google.com",
        })
        self.assertEqual(
            node.attributes_to_html(), 
            ' href="www.google.com"'
        )

        # n attributes, n > 1
        node = HTMLNode(attributes={
            "href": "www.google.com",
            "target": "_blank",
        })
        self.assertEqual(
            node.attributes_to_html(), 
            ' href="www.google.com" target="_blank"'
        )

if __name__ == "__main__":
    unittest.main()