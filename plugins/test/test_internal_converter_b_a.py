import xml.etree.ElementTree as ET
from plugnplay import Plugin
from plugins.pnp_interfaces import InternalConverterInterface

class InternalConverterB_A(Plugin):
    implements = [InternalConverterInterface]
    source1 = 'b'
    source2 = 'a'

    translate_dict = {'101': '100'}

    def convert(self, record):
        return self.get_json(ET.fromstring(record))
    
    def get_json(self, xml):
        json_dict = {}
        for child in xml.getchildren():
            if len(child.getchildren()) == 0:
                try:
                    if child.attrib['tag'] in self.translate_dict.keys():
                        tag = self.translate_dict[child.attrib['tag']]
                    else:
                        tag = child.attrib['tag']

                    if tag  not in json_dict:
                        json_dict[tag] = [child.text.strip()]
                    else:
                        json_dict[tag].append(child.text.strip())
                except:
                    if child.attrib['code'] in self.translate_dict.keys():
                        tag = self.translate_dict[child.attrib['code']]
                    else:
                        tag = child.attrib['code']

                    if tag not in json_dict:
                        json_dict[tag] = [child.text.strip()]
                    else:
                        json_dict[tag].append(child.text.strip())
            else:
                if child.attrib['tag'] in self.translate_dict.keys():
                    tag = self.translate_dict[child.attrib['tag']]
                else:
                    tag = child.attrib['tag']

                json_dict[tag] = self.get_json(child)

        return json_dict


