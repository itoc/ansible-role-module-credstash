#!/usr/bin/env python

from ansible import utils, errors
import json
import credstash
import yaml
from ansible.module_utils.basic import *
class Arguments:
  def __init__(self, Args_dict):
    self.autoversion = Args_dict['autoversion']
    self.context = Args_dict['context']
    self.digest = Args_dict['digest']
    self.fact = Args_dict['fact']
    self.fact_type = Args_dict['fact_type']
    self.credential = Args_dict['credential']
    self.key = Args_dict['key']
    self.mode = Args_dict['mode']
    self.region = Args_dict['region']
    self.table = Args_dict['table']
    self.value = Args_dict['value']
    self.version = Args_dict['version']

def main():
  module = AnsibleModule(
    argument_spec = dict(
      autoversion = dict(default=False, type='bool'),
      context = dict(default=None, type='dict'),
      digest = dict(default='SHA256', type='str'),
      fact = dict(default=None, type='str'),
      fact_type = dict(default=None, choices=['yaml','json']),
      key = dict(default='alias/credstash', type='str'),
      mode = dict(default='get', choices=['get', 'put']),
      region = dict(default='us-east-1', type='str'),
      secret = dict(required=True, type='str'),
      table = dict(default='credential-store', type='str'),
      value = dict(default=None, type='str'),
      version = dict(default='', type='str'),
    )
  )

  args_dict = {
    'autoversion'   : module.params.get('autoversion'),
    'context'       : module.params.get('context'),
    'digest'        : module.params.get('digest'),
    'fact'          : module.params.get('fact'),
    'fact_type'     : module.params.get('fact_type'),
    'credential'    : module.params.get('secret'),
    'key'           : module.params.get('key'),
    'mode'          : module.params.get('mode'),
    'region'        : module.params.get('region'),
    'table'         : module.params.get('table'),
    'value'         : module.params.get('value'),
    'version'       : module.params.get('version'),
  }

  args = Arguments(args_dict)

  result = dict(changed=False, failed=False)

  if module.params.get('mode') == 'put':
    result['output'] = credstash.putSecretAction(args, args.region)
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

main()
