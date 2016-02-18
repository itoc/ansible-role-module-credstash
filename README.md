# ansible-role-module-credstash
ansible role which embeds module for credstash lookups

Role Variables

```
secrets: 
  secret:  <= required
  fact: 
  fact_type: 
  mode: 
  value: 
  key: 
  region: 
  table: 
  version: 
  context: 
```
  

Dependencies

None

Module Requirements/Dependencies

Python: yaml/json

Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```
- hosts: servers
  roles: 
     - { role: ansible-role-module-credstash, secrets: [{"secret": "mysecret", "fact": "mysecret_fact", "fact_type":"yaml" }] }
```

License

BSD
