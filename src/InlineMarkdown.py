import re
from src.TextNode import (
    TextNode,
    OPERATORS
)

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

        if len(buffer) > 0:
            splitted_nodes.append(TextNode(" ".join(buffer), "text"))
    return splitted_nodes