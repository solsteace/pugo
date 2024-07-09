from src.HTMLNode import HTMLNode
from src.LeafNode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, children, tag, attributes=dict()):
        super().__init__(tag, children=children, attributes=attributes)

    def to_html(self):
        if type(self._tag) != str:
            raise ValueError("Invalid tag has been given")

        is_invalid_children = ( type(self._children) !=  list
                                or len(self._children) == 0)
        if is_invalid_children:
            raise ValueError("Children should be a list with at least one child")

        children_html = list(map(lambda child: child.to_html(), self._children))
        innerHTML = " ".join(children_html)

        if(self._tag != "pre"): # Band aid solution, fix this later
            return f"<{self._tag}{self.attributes_to_html()}> {innerHTML} </{self._tag}>"
        return f"<{self._tag}{self.attributes_to_html()}>{innerHTML}</{self._tag}>"

