1 - create database named `test` on your mysql server  
  
2 - seed dabase with random records  
`mycli -P <db-server-port> -p <password-for-root-host> -D test < ./db/employees_enlarged.sql`  
  
3 - create a python virtual env  
`uv venv`  
  
4 - install deps  
`uv pip install -r pyproject.toml`  
  
5 - run a smoke test to test if everything works fine  
`bash scripts/run_servers.sh smoke 2`  
  
if everything works fine, run the main tests  
`bash scripts/run_servers.sh load 5`  
  
the above test will take aproximately 42 minutes
