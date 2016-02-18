#!/usr/bin/env python

from ansible import utils, errors
import json
import credstash
import yaml
from ansible.module_utils.basic import *

def main():
  module = AnsibleModule(
    argument_spec = dict(
      secret = dict(required=True, type='str'),
      fact = dict(default=None, type='str'),
      fact_type = dict(default=None, choices=['yaml','json']),
      mode = dict(default='get', choices=['get', 'put']),
      value = dict(default=None, type='str'),
      key = dict(default='alias/credstash', type='str'),
      region = dict(default='us-east-1', type='str'),
      table = dict(default='credential-store', type='str'),
      version = dict(default='', type='str'),
      context = dict(default=None, type='dict')
    )
  )

  result = dict(changed=False, failed=False)

  if module.params.get('mode') == 'put':
    result['output'] = credstash.putSecret(module.params.get('secret'), module.params.get('value'), \
      module.params.get('version'), module.params.get('key'), module.params.get('region'), \
      module.params.get('table'), module.params.get('context'))
    result['changed'] = True

  try: 
    result['output'] = credstash.getSecret(module.params.get('secret'), module.params.get('version'), \
      module.params.get('region'), module.params.get('table'), module.params.get('context')) 
  except credstash.ItemNotFound:
    module.fail_json(msg="credstash secret not found")
  
  if module.params.get('fact') is not None:
    if module.params.get('fact_type') == 'yaml':
      result['ansible_facts'] = { module.params.get('fact'): yaml.safe_load(result['output']) }
    elif module.params.get('fact_type') == 'json':
      result['ansible_facts'] = { module.params.get('fact'): json.load(result['output']) } 
    else:
      result['ansible_facts'] = { module.params.get('fact'): result['output'] }

  module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *
main()
