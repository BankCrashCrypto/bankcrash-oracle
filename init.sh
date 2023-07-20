#!/bin/bash

ssh -i "~/.ssh/hm_notebook.pem" ubuntu@api.bankcrash.gg '(cd bankcrash-oracle && git reset --hard)'
ssh -i "~/.ssh/hm_notebook.pem" ubuntu@api.bankcrash.gg '(cd bankcrash-oracle && git pull origin main)'
ssh -i "~/.ssh/hm_notebook.pem" ubuntu@api.bankcrash.gg 'rm ~/bankcrash-oracle/config_accounts.py'
scp -i "~/.ssh/hm_notebook.pem" ~/repo/bankcrash-oracle/config_accounts.py ubuntu@api.bankcrash.gg:~/bankcrash-oracle
