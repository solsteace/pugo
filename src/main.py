from TextNode import TextNode
from HTMLNode import HTMLNode
from LeafNode import LeafNode

l1 = LeafNode(
    value="slajds", 
    tag="a", 
    attributes={
        "href": "google.com"
    }
)

print(l1.to_html())
