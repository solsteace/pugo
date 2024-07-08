from src.LeafNode import LeafNode

TEXT_NODE_TYPES = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img"
}

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.__text = text
        self.__type = text_type
        self.__url = url
    
    def get_type(self): return self.__type
    def get_value(self): return self.__text
    def get_url(self): return self.__url

    def __eq__(self, other):
        return (
            self.__text == other.__text
            and self.__type == other.__type
            and self.__url == other.__url
        )

    def __repr__(self):
        return f"TextNode({self.__text}, {self.__type}, {self.__url})"

    def to_leaf_node(self):
        supported_types = TEXT_NODE_TYPES.keys()
        text_type = self.get_type()
        node_url = self.get_url()
        node_value = self.get_value()

        if not(text_type in supported_types):
            raise ValueError(f"Unknown text type. Use one of the following instead\n [{", ".join(supported_types)}]")

        if type(node_url) != str:
            raise ValueError(f"url should be a string containing a url")

        if self.get_type() == "image":
            return LeafNode( "", TEXT_NODE_TYPES["image"], { "src": node_url })
        elif text_type == "link":
            if (type(node_value) != str) and (len(node_value) < 1):
                raise ValueError(f"anchor text should at least be a single character")
            return LeafNode( node_value, TEXT_NODE_TYPES["link"], { "href": node_url })

        return LeafNode(node_value, TEXT_NODE_TYPES[text_type])
