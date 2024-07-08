from src.LeafNode import LeafNode
import re

TEXT_NODE_TYPES = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img"
}

OPERATORS = {
    "**": "bold",
    "*": "italic",
    "`": "code"
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
        return f"TextNode('{self.__text}', {self.__type}, {self.__url})"

    def to_leaf_node(self):
        supported_types = TEXT_NODE_TYPES.keys()
        text_type = self.get_type()
        node_url = self.get_url()
        node_value = self.get_value()

        if not(text_type in supported_types):
            raise ValueError(f"Unknown text type. Use one of the following instead\n [{", ".join(supported_types)}]")

        if text_type == "image":
            if type(node_url) != str:
                raise ValueError(f"url should be a string containing a url")
            return LeafNode( "", TEXT_NODE_TYPES["image"], { "src": node_url })
        elif text_type == "link":
            if type(node_url) != str:
                raise ValueError(f"url should be a string containing a url")
            elif (type(node_value) != str) and (len(node_value) < 1):
                raise ValueError(f"anchor text should at least be a single character")
            return LeafNode( node_value, TEXT_NODE_TYPES["link"], { "href": node_url })

        return LeafNode(node_value, TEXT_NODE_TYPES[text_type])

def split_nodes_by_delimiter(nodes, delimiter):
    splitted_nodes = []
    for node in nodes:
        if node.get_type() != "text":
            splitted_nodes.append(node)
            continue

        sections = node.get_value().split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Found unclosed delimiter")
        
        for (idx, section) in enumerate(sections):
            text_type = "text" if idx % 2 == 0 else OPERATORS[delimiter]
            if len(section) > 0:
                splitted_nodes.append(TextNode(section, text_type))

    return splitted_nodes
            
def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return [("image", *match) for match in matches]

def extract_markdown_links(text):
    matches = re.findall(r"[^!]?\[(.*?)\]\((.*?)\)", text)
    return [("link", *match) for match in matches]

def split_links_on_nodes(nodes):
    splitted_nodes = []
    for node in nodes:
        buffer = []
        node_text = node.get_value()
        links = extract_markdown_images(node_text)
        links.extend(extract_markdown_links(node_text))

        for section in node_text.split(" "):
            buffer.append(section)
            buffer_text = " ".join(buffer)
            for link in links:
                link_text = (
                    ("!" if link[0] == "image" else "")
                    + f"[{link[1]}]({link[2]})"
                )

                found_match = ( 
                    len(buffer_text) >= len(link_text) 
                    and (buffer_text[-len(link_text):] == link_text)
                )
                
                if found_match:
                    splitted_nodes.append(TextNode(
                        buffer_text[:len(buffer_text) - len(link_text)],
                        "text"
                    ))
                    splitted_nodes.append(TextNode(link[1], link[0], link[2]))
                    buffer = []
                    break

    return splitted_nodes