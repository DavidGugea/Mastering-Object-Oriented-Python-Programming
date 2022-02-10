import xml.etree.ElementTree as XML
from Post import Post
from typing import cast

class Post_2(Post):
    def xmlelt(self) -> XML.Element:
        post = XML.Element("entry")
        title = XML.SubElement(post, "title")
        title.text = self.title
        date = XML.SubElement(post, "date")
        date.text = str(self.date)
        tags = XML.SubElement(post, "tags")
        for t in self.tags:
            tag = XML.SubElement(post, "rst_text")
            tag.text = t

        text = XML.SubElement(post, "rst_text")
        text.text = self.rst_text
        post.tail = "\n"
        return post