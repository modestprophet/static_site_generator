import os
from block_markdown import *
from inline_markdown import *
from htmlnode import *


def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def heading_parent(text):
    leaf_nodes = []
    heading_size = len(text) - len(text.lstrip('#'))
    text_nodes = text_to_textnodes(text.lstrip('#'))
    for text_node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    out_node = ParentNode(f"h{heading_size}", leaf_nodes)
    return out_node


def quote_parent(text):
    leaf_nodes = []
    for leaf_node in leaf_nodes:
        text_nodes = text_to_textnodes(text)
        for text_node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(text_node))
    out_node = ParentNode("blockquote", leaf_nodes)
    return out_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if re.match(r'^#[^#]', line):
            return line[1:]
        elif line.startswith('#') and len(line) > 1 and line[1] == '#':
            pass
        else:
            raise Exception("No H1 header found.  All pages need a single header.  ")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as md_file:
        md = md_file.read()

    with open(template_path, 'r') as template_file:
        template = template_file.read()

    html_nodes = markdown_to_html_node(md)
    html = html_nodes.to_html()
    title = extract_title(md)

    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)

    with open(dest_path, 'w') as out:
        out.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        if os.path.isfile(content_path) and item.endswith('.md'):
            dest_file_path = os.path.join(dest_dir_path, item[:-3] + '.html')
            generate_page(content_path, template_path, dest_file_path)
        elif os.path.isdir(content_path):
            dest_subdir_path = os.path.join(dest_dir_path, item)
            os.makedirs(dest_subdir_path, exist_ok=True)
            generate_pages_recursive(content_path, template_path, dest_subdir_path)

