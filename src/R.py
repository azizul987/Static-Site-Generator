import re
def extract_markdown_images(text):
    p=r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(p, text)
    return matches
def extract_markdown_links(text):
    p=r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(p,text)
    return matches
