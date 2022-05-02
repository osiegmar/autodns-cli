# autodns-cli

Command line utility for [AutoDNS by InternetX](https://www.internetx.com/en/domains/autodns/).

This project is **WORK IN PROGRESS**.

## Credentials

    export AUTODNS_USERNAME='<YOUR AUTODNS USERNAME>'
    export AUTODNS_PASSWORD='<YOUR AUTODNS PASSWORD>'


## List all zones

    autodns zone-list


## List zone records

    autodns zone-info --zone <zone-name>


## Find wildcard records

    autodns find-wildcard-records

## Copyright

Copyright 2018 Oliver Siegmar

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
