from textnode import TextNode,TextType
import os
import shutil
import sys
from nodes_delimite import generate_page

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    source="static"
    dest="docs"
    if os.path.exists(dest):
        shutil.rmtree(dest)
    copy_files_recursive(source, dest)
    generate_pages_recursive("content", "template.html", "docs", basepath)

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_path = dest_path[:-3] + ".html"
                generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

main()
