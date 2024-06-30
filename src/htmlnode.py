def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    match text_type:
        case "text":
            return LeafNode(tag=None, value=text_node.text)
        case "bold":
            return LeafNode(tag="b", value=text_node.text)
        case "italic":
            return LeafNode(tag="i", value=text_node.text)
        case "code":
            return LeafNode(tag="code", value=text_node.text)
        case "link":
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Unsupported text node type{text_type}")
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        html_props = " ".join(f'{tag}="{value}"' for tag, value in self.props.items())
        html_props = " " + html_props
        return html_props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

        
    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes require a value.")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes require a tag.")
        if self.children is None:
            raise ValueError("Must provide children nodes")
        if self.children is not None:
            html_children = ""
            for child in self.children:
                html_children += child.to_html()
            html_children = f"<{self.tag}{self.props_to_html()}>{html_children}</{self.tag}>"
            return html_children


    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"