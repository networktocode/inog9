#!/usr/bin/env python

# Copyright 2015 Jason Edelman <jason@networktocode.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---

module: oc_bgp
short_description: Configure BGP according to the OC-BGP model
description:
    - Manages ASN and router ID
author: Jason Edelman (@jedelman8)
requirements:
    - ncclient
notes:
    - When state is set to absent, the existing BGP configuration
      regardless if ASN matches what is in the playbook, will be
      removed from the switch.
options:
    asn:
        description:
            - BGP ASN
        required: true
    router_id:
        description:
            - BGP router ID
        required: false

    host:
        description:
            - IP Address or hostname (resolvable by Ansible control host)
        required: true
    port:
        description:
            - Port used to connect to NETCONF sub-system
        required: false
        default: 830
    username:
        description:
            - Username used to login to the network device
        required: true
    password:
        description:
            - Password used to login to the network device
        required: true
    state:
        description:
            - Manage state of global BGP ASN configuration
        required: false
        default: present
        choices: ['present','absent']
'''

EXAMPLES = '''

'''

RETURN = '''

neighbors:
    description:
        - information about LLDP/CDP neighbors
    returned: always
    type: list of dict or null
    sample: {"local_interface": "mgmt0", "neighbor": "PERIMETER",
            "neighbor_interface": "FastEthernet1/0/10"}

'''
import socket
from lxml import etree
from ncclient import manager
from ncclient.xml_ import qualify
import ncclient

def remove_namespaces(xml):
    """Remove the namespaces from an
    ``etree.Element`` object and return
    the modified object.
    """
    for elem in xml.getiterator():
        split_elem = elem.tag.split('}')
        if len(split_elem) > 1:
            elem.tag = split_elem[1]
    return xml

def config_filter(module, delta, existing, state):
    """
    Hack for now.  Need to use native XML objects
    to more easily add sub-elements.  Will do after iNOG!
    """

    if state == 'present':
        operation = 'merge'
    elif state == 'absent':
        operation = 'delete'

    asn = delta.get('as') or existing.get('as')
    router_id = delta.get('router_id')

    if (asn and router_id) or router_id:
        # asn = asn or
        nc_filter = """
                        <config>
                         <bgp xmlns="http://openconfig.net/yang/bgp" nc:operation="{0}">
                          <global>
                           <config>
                            <as>{1}</as>
                            <router-id>{2}</router-id>
                           </config>
                          </global>
                         </bgp>
                        </config>
                        """.format(operation, asn, router_id)
    elif asn:
        nc_filter = """
                        <config>
                         <bgp xmlns="http://openconfig.net/yang/bgp" nc:operation="{0}">
                          <global>
                           <config>
                            <as>{1}</as>
                           </config>
                          </global>
                         </bgp>
                        </config>
                        """.format(operation, asn)

    return nc_filter

def get_filter():

    get_filter = """

                     <bgp xmlns="http://openconfig.net/yang/bgp">
                      <global>
                       <config>
                         <as></as>
                         <router-id></router-id>
                       </config>
                      </global>
                     </bgp>

                    """
    return get_filter

def main():
    module = AnsibleModule(
        argument_spec=dict(
            asn=dict(required=True),
            router_id=dict(required=False),
            port=dict(required=False, type='int', default=830),
            state=dict(required=False, default='present', choices=['present', 'absent']),
            host=dict(required=True),
            platform=dict(required=False, default='iosxr'),
            username=dict(type='str'),
            password=dict(type='str'),
        ),
        supports_check_mode=True
    )

    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    platform = module.params['platform']
    asn = module.params['asn']
    router_id = module.params['router_id']
    state = module.params['state']
    host = socket.gethostbyname(module.params['host'])

    args = {'as': asn, 'router_id': router_id }
    proposed = dict((k, v) for k, v in args.items() if v is not None)

    with manager.connect(host=host, port=port, username=username, password=password,
                         hostkey_verify=False,
                         allow_agent=False, look_for_keys=False) as device:

        nc_get_reply = device.get(('subtree', get_filter()))

        response = remove_namespaces(nc_get_reply.data_ele)

        existing_asn = response.find('.//as')
        existing_rid = response.find('.//router-id')
        existing = {}
        if existing_asn is not None:
            existing['as'] = existing_asn.text
        if existing_rid is not None:
            existing['router_id'] = existing_rid.text

        delta = dict(set(proposed.items()).difference(existing.items()))
        changed = False
        xml_filter = ''

        if state == 'present':

            if delta or not existing:
                if delta.get('as') and delta.get('as') != existing.get('as') and existing.get('as'):
                    module.fail_json(msg='cannot change ASN. Use state=absent to remove first',
                                     existing=existing.get('as'), proposed=asn)
                else:
                    xml_filter = config_filter(module, delta, existing, state)
        elif state == 'absent':
            if existing:
                xml_filter = config_filter(module, delta, existing, state)

        if xml_filter:
            if module.check_mode:
                changed = True
            else:
                try:
                    nc_reply = device.edit_config(target='candidate', config=xml_filter)
                    device.commit()
                    changed = True
                except ncclient.operations.rpc.RPCError as err:
                    module.fail_json(msg='unsuccessful change', error=str(err))

    results = {}
    results['changed'] = changed
    results['existing'] = existing
    results['xml_filter'] = xml_filter
    module.exit_json(**results)


from ansible.module_utils.basic import *
if __name__ == "__main__":
    main()
