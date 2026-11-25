#!/usr/bin/env python3
"""Ship entry.png to the grader's output directory, byte for byte."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
