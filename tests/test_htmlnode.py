import unittest
from src.HTMLNode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_html_attributes(self):
        cases = [
            (   
                "It should correctly handle no attribute",
                { "href": "www.google.com", },
                ' href="www.google.com"'
            ),
            ( 
                "It should correctly generate a single attribute",
                { "href": "www.google.com", },
                ' href="www.google.com"'
            ),
            ( 
                "It should correctly generate more than one attribute",
                { 
                    "href": "www.google.com",
                    "target": "_blank",
                },
                ' href="www.google.com" target="_blank"'
            ),
        ]

        for idx in range(len(cases)):
            _, args, expected = cases[idx]
            node = HTMLNode(attributes=args)
            self.assertEqual(node.attributes_to_html(), expected)

if __name__ == "__main__":
    unittest.main()