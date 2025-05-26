#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: test_reduction.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import os
import pathlib
import shutil


def test_reduction(data_dir: pathlib.Path, tmp_path: pathlib.Path):
    """Test the main reduction script. Just checks that it runs without errors."""

    from ccd.reduction import run_reduction

    os.chdir(tmp_path)

    try:
        # Run the reduction script
        run_reduction(str(data_dir))
    finally:
        if tmp_path.exists():
            shutil.rmtree(tmp_path)

    assert True  # To make sure the test is not skipped.
