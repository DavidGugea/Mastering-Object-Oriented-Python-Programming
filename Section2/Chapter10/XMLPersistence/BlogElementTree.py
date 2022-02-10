import xml.etree.ElementTree as XML
from Blog import Blog
from PostElementTree import Post
from typing import cast


class Blog2(Blog):
    def xmlelt(self) -> XML.Element:
        blog = XML.Element("blog")
        title = XML.SubElement(blog, "title")
        title.text = self.title
        title.tail = "\n"
        entities = XML.SubElement(blog, "entries")
        entities.extend(cast("Post_2", c).xmlelt() for c in self.entries)
        blog.tail = "\n"
        return blog
