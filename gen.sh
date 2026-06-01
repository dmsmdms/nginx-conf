#!/bin/bash

source venv/bin/activate
exec ./gen.py apps_srv.toml nginx.srv.conf.j2 nginx.conf
