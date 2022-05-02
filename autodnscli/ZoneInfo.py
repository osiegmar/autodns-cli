# Copyright 2018 Oliver Siegmar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import xml.etree.ElementTree as ET

class ZoneInfo:

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def run(self, a_zone_name, printout=True):
        request = self.apiClient.new_req('0205')
        task = request.find('task')

        task_zone = ET.SubElement(task, 'zone')
        zone_name = ET.SubElement(task_zone, 'name')
        zone_name.text = a_zone_name

        response = self.apiClient.call_api(ET.tostring(request).decode())

        ignored_records = ['changed', 'comment', 'created', 'domainsafe', 'name', 'ns_action',
                           'owner', 'soa', 'system_ns', 'updated_by', 'dnssec', 'idn', 'ns_group']

        record_array = []

        for zone in response.findall('result/data/zone'):
            # ET.dump(zone)
            for rec in list(zone):
                if rec.tag not in ignored_records:
                    parsed_record = self.parse_record(rec, zone)

                    if parsed_record is None:
                        continue

                    if printout is True:
                        parsed_record.print_out()
                    else:
                        record_array.append(parsed_record)
        return record_array

    def parse_record(self, rec, zone):
        if rec.tag == 'nserver':
            return self.parse_nserver(rec, zone)
        if rec.tag == 'main':
            return self.parse_main(rec, zone)
        if rec.tag == 'www_include':
            return self.parse_www_include(rec, zone)
        if rec.tag == 'rr':
            return self.parse_rr(rec, zone)

        raise Exception("Unsupported element: " + rec.tag)

    def parse_nserver(self, rec, zone):
        return ZoneRecord('@', zone.findtext('soa/default'), 'NS', rec.find('name').text + '.')

    def parse_main(self, rec, zone):
        ttl = rec.find('ttl').text if rec.find('ttl') is not None else zone.findtext('soa/default')
        return ZoneRecord('@', ttl, 'A', rec.find('value').text)

    def parse_www_include(self, rec, zone):
        if rec.text != '1':
            return None

        main_rec = zone.find('main')
        if main_rec is None or main_rec.find('ttl') is None or main_rec.find('value') is None:
            return None

        return ZoneRecord('www', main_rec.find('ttl').text, 'A', main_rec.find('value').text)

    def parse_rr(self, rec, zone):
        name = rec.find('name').text or '@'
        ttl = rec.find('ttl').text if rec.find('ttl') is not None else zone.findtext('soa/default')
        pref = rec.find('pref').text + " " if rec.find('pref') is not None else ''
        type = rec.find('type').text
        value = pref + rec.find('value').text
        if type == 'TXT':
            value = '"' + value + '"'
        return ZoneRecord(name, ttl, type, value)


class ZoneRecord:

    def __init__(self, name, ttl, type, value):
        self.name = name
        self.ttl = ttl
        self.type = type
        self.value = value

    def print_out(self):
        print('{}\t{}\tIN\t{}\t{}'.format(self.name, self.ttl, self.type, self.value))
