#!/bin/sh
bench shell
cd ..
echo "Execute validation for all modules with tests..."
echo "Please wait, it takes a few minutes..."
python python run_debug.py --run module