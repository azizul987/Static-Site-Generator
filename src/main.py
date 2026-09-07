from textnode import TextNode,TextType
import os
import shutil
from nodes_delimite import generate_page

def main():
    source="static"
    dest="public"
    if os.path.exists(dest):
        shutil.rmtree(dest)
    copy_files_recursive(source, dest)
    generate_page("content/index.md", "template.html", "public/index.html")
def copy_files_recursive(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        if os.path.isdir(src_path):
            copy_files_recursive(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)
        print(f"Copied {src_path} to {dest_path}")

main()
