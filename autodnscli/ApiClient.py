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

import requests
import xml.etree.ElementTree as ET


class ApiClient:

    def __init__(self, username, password, context):
        self.username = username
        self.password = password
        self.context = context

    def new_req(self, code):
        request = ET.Element('request')
        auth = ET.SubElement(request, 'auth')

        user = ET.SubElement(auth, 'user')
        user.text = self.username

        password = ET.SubElement(auth, 'password')
        password.text = self.password

        context = ET.SubElement(auth, 'context')
        context.text = self.context

        task = ET.SubElement(request, 'task')
        task_code = ET.SubElement(task, 'code')
        task_code.text = code

        return request

    def call_api(self, xml_str):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = ET.fromstring(
            requests.post('https://gateway.autodns.com/', data=xml_str, headers=headers).text)

        if response.find('result/status/type').text != 'success':
            raise Exception('Response not successful: ' + response.find('result/status/type').text
                            + '; ' + response.find('result/status/text').text)

        return response
