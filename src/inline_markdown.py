import re
from textnode import (TextNode,
                      text_type_text,
                      text_type_bold,
                      text_type_italic,
                      text_type_code,
                      text_type_image,
                      text_type_link
                      )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    extracted = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return extracted


def extract_markdown_links(text):
    extracted = re.findall(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)", text)
    return extracted


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        split_nodes = []
        image_tuples = extract_markdown_images(old_node.text)

        if len(image_tuples) == 0:
            new_nodes.append(old_node)
            continue
        image_tuple = image_tuples[0]
        sections = old_node.text.split(f"![{image_tuple[0]}]({image_tuple[1]})", 1)

        if sections[0] != "":
            split_nodes.append(TextNode(sections[0], text_type_text))

        split_nodes.append(TextNode(image_tuple[0], text_type_image, image_tuple[1]))
        if sections[1] != "":
            remainder = [TextNode(sections[1], text_type_text)]
            split_nodes.extend(split_nodes_image(remainder))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        split_nodes = []
        link_tuples = extract_markdown_links(old_node.text)

        if len(link_tuples) == 0:
            new_nodes.append(old_node)
            continue
        link_tuple = link_tuples[0]
        sections = old_node.text.split(f"[{link_tuple[0]}]({link_tuple[1]})", 1)

        if sections[0] != "":
            split_nodes.append(TextNode(sections[0], text_type_text))

        split_nodes.append(TextNode(link_tuple[0], text_type_link, link_tuple[1]))
        if sections[1] != "":
            remainder = [TextNode(sections[1], text_type_text)]
            split_nodes.extend(split_nodes_link(remainder))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

