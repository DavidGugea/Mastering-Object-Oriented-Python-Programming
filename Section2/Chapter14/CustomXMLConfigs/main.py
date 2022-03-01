import xml.etree.ElementTree as XML


class Configuration:
    def read_file(self, file):
        self.config = XML.parse(file)

    def read(self, filename):
        self.config = XML.parse(filename)

    def read_string(self, text):
        self.config = XML.fromstring(text)

    def get(self, qual_name, default):
        section, _, item = qual_name.partition(".")
        query = "./{0}/{1}".format(section, item)
        node = self.config.find(query)
        if node is None:
            return default

        return node.text

    def __getitem__(self, section):
        query = "./{0}".format(section)
        parent = self.ocnfig.find(query)
        return dict((item.tag, item.text) for item in parent)