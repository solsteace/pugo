class HTMLNode:
    def __init__(self, tag=None, value=None, children=list(), attributes=dict()):
        """
            The following assumptions are used:
            * Node with no tag would be rendered as raw text
            * Node with no value would have children
            * Node with no children would have a value
        """

        self._tag = tag
        self._value = value
        self._children = children
        self._attributes = attributes

    def to_html(self):
        raise NotImplementedError()
    
    def attributes_to_html(self):
        mapped_attributes = [f' {key}=\"{value}\"' for (key, value) in self._attributes.items()]
        return "".join(mapped_attributes)

    def __repr__(self):
        tag_repr = ( "raw text" if self._tag == None 
                    else self._tag)

        value_repr = ( "-" if self._value == None 
                        else self._value)

        children_repr = (
            "-" if self._children == None 
            else "\n" + "\n".join([f"\tHTMLNode({child.__tag})" for child in self._children])
        )

        attributes_repr = (
            "-" if self._attributes == None 
            else "\n" + "\n".join([f"\t{key}: {value}" for (key, value) in self._attributes])
        )

        return "\n".join([
            f"HTMLNode({tag_repr})",
            f"value: '{value_repr}'",
            f"children: {children_repr}",
            f"attributes: {attributes_repr}",
        ])
