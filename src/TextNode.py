class TextNode:
    def __init__(self, text, text_type, url=None):
        self.__text = text
        self.__type = text_type
        self.__url = url
    
    def __eq__(self, other):
        return (
            self.__text == other.__text
            and self.__type == other.__type
            and self.__url == other.__url
        )

    def __repr__(self):
        return f"TextNode({self.__text}, {self.__type}, {self.__url})"
