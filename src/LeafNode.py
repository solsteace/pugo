from src.HTMLNode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=list(), attributes=dict()):
        super().__init__(tag, value, children, attributes)

    def to_html(self):
        if self._value == None:
            raise ValueError("LeafNode has no value")
        return (self._value if self._tag == None
                else f"<{self._tag}{self.attributes_to_html()}> {self._value} </{self._tag}>"
        )