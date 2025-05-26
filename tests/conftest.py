#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-04-18
# @Filename: conftest.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import os
import pathlib
import subprocess

import pytest

TMP_TARFILE = "/tmp/ccd_reductions_data.tar.bz2"
TMP_DIR = "/tmp/ccd_reductions_data_pytest"


@pytest.fixture(scope="session")
def data_dir():
    """Fixture to download data for the tests."""

    if not os.path.exists(TMP_DIR):
        subprocess.run(
            f"curl -o {TMP_TARFILE} https://faculty.washington.edu/gallegoj/astr480/ccd_reductions_data.tar.bz2",
            shell=True,
        )

        os.mkdir(TMP_DIR)

        subprocess.run(
            f"tar -xvjf {TMP_TARFILE} -C {TMP_DIR}",
            shell=True,
        )

    data_path = pathlib.Path(f"{TMP_DIR}/ccd_reductions_data/")

    yield data_path

    if os.path.exists(TMP_TARFILE):
        os.unlink(TMP_TARFILE)

    if os.path.exists(data_path):
        subprocess.run(f"rm -rf {TMP_DIR}/ccd_reductions_data", shell=True)
