from src.LeafNode import LeafNode
from src.ParentNode import ParentNode
from src.TextNode import TextNode
from src.InlineMarkdown import (
    split_links_on_nodes,
    split_nodes_by_delimiter
)

PRECEDING_PATTERNS = {
    "###### ": "heading_6",
    "##### ": "heading_5",
    "#### ": "heading_4",
    "### ": "heading_3",
    "## ": "heading_2",
    "# ": "heading_1",
    "```": "block_code",
    "1. ": "ordered_list",
    "> ": "block_quote",
    "* ": "unordered_list",
    "- ": "unordered_list",
}

def markdown_to_blocks(markdown):
    cleaned_markdown = markdown.strip().split("\n")
    blocks = []
    buffer = []
    for line in cleaned_markdown:
        line = line.strip()
        if line == "" and len(buffer) > 0:
            blocks.append(buffer)
            buffer = []
        elif line != "":
            buffer.append(line)

    if len(buffer) > 0:
        blocks.append(buffer)
    return blocks

def get_block_type(block):
    block_type = "paragraph"
    patterns = PRECEDING_PATTERNS.keys()
    for pattern in patterns:
        if pattern == block[:len(pattern)]:
            block_type = PRECEDING_PATTERNS[pattern]
            break
    
    return block_type

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    block_types = list(map(lambda b: get_block_type(b[0]), blocks))

    result = []
    for idx in range(len(blocks)):
        children = []
        block = blocks[idx]
        block_type = block_types[idx]
        if block_type == "paragraph": 
            children.append(handle_paragraph(block))
        elif block_type == "block_code":
            children.append(handle_block_code(block))
        elif block_type == "block_quote":
            children.append(handle_block_quote(block))
        elif block_type == "unordered_list":
            children.append(handle_unordered_list(block))
        elif block_type == "ordered_list":
            children.append(handle_ordered_list(block))
        else:
            children.append(handle_heading(block, block_type))

        result.append(ParentNode(children, "div"))
    return [res.to_html() for res in result]

def handle_paragraph(blocks):
    paragraph_contents = split_nodes_by_delimiter(
        split_nodes_by_delimiter(
            split_nodes_by_delimiter(
                split_links_on_nodes([TextNode(" ".join(blocks), "text")]), '**'
            ), '*'
        ), '`'
    )
    return ParentNode(
        [content.to_leaf_node() for content in paragraph_contents],
        "p"
    )

def handle_heading(blocks, block_type):
    heading_level = int(block_type[-1])
    content = " ".join(blocks)[heading_level + 1:]
    return LeafNode(content, f"h{heading_level}")

def handle_block_code(blocks):
    if blocks[-1][:3] != "```":
        raise ValueError("Block quote wasn't closed")

    children = TextNode(f"{'\n'.join(blocks[1: -1])}", "text").to_leaf_node()
    return ParentNode( [ ParentNode([children], "code") ], "pre")

def handle_block_quote(blocks):
    block_quote_contents = [block[2:] for block in blocks]
    quote = " ".join(block_quote_contents)
    return ParentNode( [ LeafNode(quote) ], "blockquote")

def handle_unordered_list(blocks):
    children = []
    for block in blocks:
        list_item_content = split_nodes_by_delimiter(
            split_nodes_by_delimiter(
                split_nodes_by_delimiter(
                    split_links_on_nodes( [TextNode(block[2:], "text")]), '**'
                ), '*'
            ), '`'
        )

        list_item_content = [item.to_leaf_node() for item in list_item_content]
        children.append(ParentNode(list_item_content, "li"))
    return ParentNode(children, "ul")

def handle_ordered_list(blocks):
    children = []
    counter = 1
    for block in blocks:
        preceding_counter = f"{counter}. "
        order_count = block[:len(preceding_counter)]
        if order_count != preceding_counter:
            raise ValueError(f"Wrong list item ordering (expected: `{preceding_counter}`, got: '{order_count}')")

        list_item_content = split_nodes_by_delimiter(
            split_nodes_by_delimiter(
                split_nodes_by_delimiter(
                    split_links_on_nodes(
                        [TextNode(block[len(preceding_counter):], "text")]), '**'
                ), '*'
            ), '`'
        )

        list_item_content = [item.to_leaf_node() for item in list_item_content]
        children.append(ParentNode(list_item_content, "li"))
        counter += 1
    return ParentNode(children, "ol")