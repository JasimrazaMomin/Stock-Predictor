#!/bin/bash

pip freeze > uninstall_requirements.txt

pip uninstall -r uninstall_requirements.txt -y

pip install -r requirements.txt

#run this using ./reset_env.sh to reset virtual env pip dependencies