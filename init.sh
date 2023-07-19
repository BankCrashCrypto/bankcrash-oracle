#!/bin/bash

git reset --hard
git pull origin main
sed -i '1d;2d' oracle.py
