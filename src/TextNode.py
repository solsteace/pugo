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

def text_node_to_leaf_node(text_node):
    supported_types = TEXT_NODE_TYPES.keys()
    text_type = text_node.get_type()
    if not(text_type in supported_types):
        raise ValueError(f"Unknown text type. Use one of the following instead\n [{", ".join(supported_types)}]")

    node_url = text_node.get_url()
    node_value = text_node.get_value()
    if text_node.get_type() == "image":
        if not(isinstance(node_url, str)):
            raise ValueError(f"url should be a string containing a url")

        return LeafNode(
            "",
            TEXT_NODE_TYPES["image"],
            { "src": node_url }
        )

    if text_type == "link":
        if not(isinstance(node_url, str)):
            raise ValueError(f"url should be a string containing a url")
        
        is_invalid_anchor_text = (
            not(isinstance(node_url, str))
            and len(node_url) < 1
        )
        if is_invalid_anchor_text:
            raise ValueError(f"anchor text should at least be a single character")

        return LeafNode(
            node_value,
            TEXT_NODE_TYPES["link"],
            { "href": text_node.get_url()}
        )

    return LeafNode(node_value, TEXT_NODE_TYPES[text_type])