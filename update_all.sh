#!/bin/bash -exv
python update_problems.py
python show_unsolved_problems.py > unsolved_problems.txt
python show_problems.py > human_readable_problems.txt
