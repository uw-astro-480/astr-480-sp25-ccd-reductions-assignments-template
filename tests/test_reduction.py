#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: test_reduction.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import os
import pathlib


def test_reduction(data_dir: pathlib.Path, tmp_path: pathlib.Path):
    """Test the main reduction script. Just checks that it runs without errors."""

    from ccd.reduction import run_reduction

    os.chdir(tmp_path / "test_reduction")

    # Run the reduction script
    run_reduction(str(data_dir))

    assert True  # To make sure the test is not skipped.
