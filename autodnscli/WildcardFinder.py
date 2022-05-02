import xml.etree.ElementTree as ET
import time
from ZoneInfo import ZoneInfo

class WildcardFinder:

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def run(self):
        response = self.getList()
        zones = response.findall('result/data/zone')
        print('Zone count: ' + str(len(zones)))
        for zone in zones:
            zone_name = zone.find('name').text
            records = ZoneInfo(self.apiClient).run(zone_name, False)
            for record in records:
                if record.name == '*':
                    print("Zone: ", zone_name)
                    print(record.name)
            time.sleep(1)


    def getList(self):
        request = self.apiClient.new_req('0205')
        task = request.find('task')

        view = ET.SubElement(task, 'view')

        limit = ET.SubElement(view, 'limit')
        limit.text = str(5000)

        children = ET.SubElement(view, 'children')
        children.text = '1'

        return self.apiClient.call_api(ET.tostring(request).decode())

