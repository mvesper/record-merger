import xml.etree.ElementTree as ET
from plugnplay import Plugin
from plugins.pnp_interfaces import InternalConverterInterface

class InternalConverterA_B(Plugin):
    implements = [InternalConverterInterface]
    source1 = 'a'
    source2 = 'b'

    def convert(self, record):
        return self.get_json(ET.fromstring(record))
    
    def get_json(self, xml):
        json_dict = {}
        for child in xml.getchildren():
            if len(child.getchildren()) == 0:
                try:
                    if child.attrib['tag'] not in json_dict:
                        json_dict[child.attrib['tag']] = [child.text.strip()]
                    else:
                        json_dict[child.attrib['tag']].append(child.text.strip())
                except:
                    if child.attrib['code'] not in json_dict:
                        json_dict[child.attrib['code']] = [child.text.strip()]
                    else:
                        json_dict[child.attrib['code']].append(child.text.strip())
            else:
                json_dict[child.attrib['tag']] = self.get_json(child)

        return json_dict

