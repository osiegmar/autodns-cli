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

REC_FMT = '{}\t{}\tIN\t{}\t{}'


class ZoneInfo:

    def __init__(self, apiClient):
        self.apiClient = apiClient

    def run(self, a_zone_name):
        request = self.apiClient.new_req('0205')
        task = request.find('task')

        task_zone = ET.SubElement(task, 'zone')
        zone_name = ET.SubElement(task_zone, 'name')
        zone_name.text = a_zone_name

        response = self.apiClient.call_api(ET.tostring(request).decode())

        ignored_records = ['changed', 'comment', 'created', 'domainsafe', 'name', 'ns_action',
                           'owner', 'soa', 'system_ns', 'updated_by']

        for zone in response.findall('result/data/zone'):
            for rec in list(zone):
                if rec.tag in ignored_records:
                    pass
                elif rec.tag == 'nserver':
                    self.print_nserver(rec, zone)
                elif rec.tag == 'main':
                    self.print_main(rec)
                elif rec.tag == 'www_include':
                    self.print_www_include(rec, zone)
                elif rec.tag == 'rr':
                    self.print_rr(rec, zone)
                else:
                    print("Unsupported element: " + rec.tag)
                    ET.dump(rec)

    def print_nserver(self, rec, zone):
        soa_rec = zone.find('soa')
        print(REC_FMT.format(
            '@', soa_rec.find('default').text, 'NS', rec.find('name').text) + '.')

    def print_main(self, rec):
        print(REC_FMT.format(
            '@', rec.find('ttl').text, 'A', rec.find('value').text))

    def print_www_include(self, rec, zone):
        if rec.text == '1':
            main_rec = zone.find('main')
            if main_rec is not None \
                    and main_rec.find('ttl') is not None \
                    and main_rec.find('value') is not None:
                print(REC_FMT.format(
                    'www', main_rec.find('ttl').text, 'A', main_rec.find('value').text))

    def print_rr(self, rec, zone):
        name = rec.find('name').text if rec.find('name').text is not None else '@'
        pref = rec.find('pref').text + " " if rec.find('pref') is not None else ''
        if rec.find('ttl') is not None:
            ttl = rec.find('ttl').text
        else:
            soa_rec = zone.find('soa')
            ttl = soa_rec.find('default').text

        print(REC_FMT.format(
            name,
            ttl,
            rec.find('type').text,
            pref + rec.find('value').text))
