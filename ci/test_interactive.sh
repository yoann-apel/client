#!/bin/bash

source venv/bin/activate
export GPAO_API_URL=lhd-dev-gpao
python -m pytest -s test/test_interactive.py \
 --log-cli-level=INFO --log-format="%(asctime)s %(levelname)s %(message)s" \
 --log-date-format="%Y-%m-%d %H:%M:%S"
