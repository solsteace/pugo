import unittest
from src.LeafNode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_html_attributes(self):
        cases = [
            (
                "It should be able to return html when no attribute nor tag were given",
                (
                    ("Lorem ipsum sit dolor amet", ), 
                    {}
                ),
                "Lorem ipsum sit dolor amet"
            ),
            (
                "It should be able to return html when given a tag, but no attribute",
                (
                    ("Lorem ipsum sit dolor amet", ), 
                    {"tag": "p"}
                ),
                "<p> Lorem ipsum sit dolor amet </p>"
            ),
            (
                "It should be able to return html given an attribute and a tag",
                (
                    ("Google it!", ), 
                    {
                        "tag": "a",
                        "attributes": {"href": "www.google.com"}
                    }
                ),
                '<a href="www.google.com"> Google it! </a>'
            ),
            (
                "It should be ablt to return html given a tag and multiple attributes",
                (
                    ("Google it!", ), 
                    {
                        "tag": "a",
                        "attributes": {
                            "href": "www.google.com",
                            "target": "_blank"
                        }
                    }
                ),
                '<a href="www.google.com" target="_blank"> Google it! </a>'
            ),
        ]

        for idx in range(len(cases)):
            _, args, expected = cases[idx]
            args_list, kwargs_list = args

            node = LeafNode(*args_list, **kwargs_list)
            self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()