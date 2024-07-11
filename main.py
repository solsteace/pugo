from os import (
    listdir,
    path,
    mkdir
)
from shutil import copy
from src.BlockMarkdown import (
    markdown_to_blocks,
    get_block_type,
    markdown_to_html
)

DESTINATION_BASE = path.join(".", "public")
def log(pre_message, post_message):
    def do_log(func):
        def wrapper(*args, **kwargs):
            print(f"LOG: {pre_message(args)}")
            func(*args)
            print(f"LOG: {post_message(args)}")

        return wrapper
    return do_log

@log(lambda x: f"copying items in `{x[0]}`...", lambda x: f"Items `{x[0]}` copied!")
def copy_static_files(base_directory, current_path=""):
    if not(path.exists(base_directory)):
        raise ValueError(f"`{base_directory}` directory doesn't exist")

    current_relpath = path.join(".", base_directory)
    directory_items = listdir(current_relpath)
    for item in directory_items:
        item_relpath = path.join(current_relpath, item)
        if path.isfile(item_relpath):
            dest_path = path.join(DESTINATION_BASE, current_path, item)

            if not(path.exists(path.dirname(dest_path))):
                mkdir(path.dirname(dest_path))
            copy(item_relpath, dest_path)
        else:
            copy_static_files(
                path.join(base_directory, item), 
                path.join(current_path, item)
            )

def extract_title(markdown_blocks):
    title = None
    idx = 0
    while title is None and idx < len(markdown_blocks):
        block = markdown_blocks[idx][0]
        if get_block_type(block) == "heading_1":
            title = block[2:]
        idx += 1
    return title

@log(lambda x: f"Converting {x[0]}...", lambda x: f"{x[0]} conversion done!")
def generate_page(source, template_path, dest):
    with open(source, "r") as f:
        file_content = "".join(f.readlines())

        markdown_blocks = markdown_to_blocks(file_content)
        title = extract_title(markdown_blocks)
        if title is None:
            raise ValueError("This markdown file doesn't have a title in it (`heading_1` block not found)")

        content = "".join(markdown_to_html(file_content))
        rendered_content = None
        with open(template_path, "r") as tf:
            rendered_content = "".join(tf.readlines())
            rendered_content = rendered_content.replace("{{ Title }}", title)
            rendered_content = rendered_content.replace("{{ Content }}", content)

        if not(path.exists(path.dirname(dest))):
            mkdir(path.dirname(dest))
        with open(f"{dest[:-2]}html", "w") as wf:
            wf.write(rendered_content)

def generate_from_directory(base_directory, template_path, current_path=""):
    if not(path.exists(base_directory)):
        raise ValueError(f"`{base_directory}` doesn't exist")

    current_relpath = path.join(".", base_directory)
    directory_items = listdir(current_relpath)
    for item in directory_items:
        item_relpath = path.join(current_relpath, item)
        if path.isfile(item_relpath):
            if item[-3:] == ".md":
                destination = path.join(DESTINATION_BASE, current_path, item)
                generate_page(item_relpath, template_path, destination)
        else:
            generate_from_directory(
                path.join(base_directory, item), 
                template_path,
                path.join(current_path, item),
            )

if __name__ == "__main__":
    if not(path.exists(DESTINATION_BASE)):
        mkdir(DESTINATION_BASE)
    try:
        copy_static_files("static")
        generate_from_directory( "content", path.join("content", "template.html"))
    except ValueError as e:
        print(f"=== Exception raised! Check the following info to learn more ===\n{e}")