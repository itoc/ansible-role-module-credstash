# ansible-role-module-credstash
Credstash module which accepts PUT and GET commands.

# Variables

```
secrets: 
- secret:  <= required
  autoversion:
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
# Example

```
- hosts: servers
  vars:
    secrets:
      - secret: mypassword
        value: secret123
        mode: put
        autoversion: true
        region: ap-southeast-2
  tasks:
    - include: credstash.yml
```

# License

BSD
