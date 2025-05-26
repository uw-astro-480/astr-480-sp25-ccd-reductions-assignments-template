#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Filename: test_flats.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import inspect
import os
import pathlib

import numpy
import pytest
from astropy.io import fits


@pytest.mark.parametrize("with_dark", [True, False])
def test_median_flat(
    data_dir: pathlib.Path,
    tmp_path: pathlib.Path,
    with_dark: bool,
):
    """Test the creation of a median flat frame."""

    from ccd.bias import create_median_bias
    from ccd.flats import create_median_flat

    median_bias_file = tmp_path / "median_bias.fits"
    median_dark_file = tmp_path / "median_dark.fits"
    median_flat_file = tmp_path / "median_flat.fits"

    # Get the list of bias files
    bias_files = sorted(pathlib.Path(data_dir).glob("Bias*.fit*"))

    # Get the list of flat files
    flat_files = sorted(pathlib.Path(data_dir).glob("AutoFlat*.fit*"))

    # Create the median bias frame
    median_bias = create_median_bias(bias_files, str(median_bias_file))
    assert median_bias_file.exists(), "The median bias file was not created."
    assert median_bias is not None, "The median bias frame is None."

    # If we are passing a dark frame, create it.
    if with_dark:
        from ccd.darks import create_median_dark

        dark_files = sorted(pathlib.Path(data_dir).glob("Dark*.fit*"))
        median_dark = create_median_dark(
            dark_files,
            str(median_bias_file),
            str(median_dark_file),
        )

        assert median_dark_file.exists(), "The median dark file was not created."
        assert median_dark is not None, "The median dark frame is None."

    # Create the median flat frame
    median_flat = create_median_flat(
        flat_files,
        str(median_bias_file),
        str(median_flat_file),
        dark_filename=str(median_dark_file) if with_dark else None,
    )

    assert median_flat_file.exists(), "The median flat file was not created."

    assert isinstance(median_flat, numpy.ndarray), "The median flat is not an array."
    assert median_flat.ndim == 2, "The median flat is not 2D."

    assert median_flat.min() >= -5, "The median flat has values below -5."
    assert median_flat.max() <= 5, "The median flat has values above 5."


def test_plot_flat(tmp_path: pathlib.Path):
    """Test the plotting of a median flat frame."""

    from ccd.flats import plot_flat

    # Create a dummy median flat file for testing
    median_flat = numpy.ones((1024, 1024))

    median_flat_hdul = fits.HDUList([fits.PrimaryHDU(data=median_flat)])
    median_flat_hdul.writeto(str(tmp_path / "median_flat.fits"), overwrite=True)

    # Call the plot_flat function
    output_filename = tmp_path / "median_flat.png"
    profile_output_filename = tmp_path / "median_flat_profile.png"

    os.chdir(tmp_path)  # Change to the temporary directory

    # Make sure I get the correct argument since some students have fixed the typo
    # for ouput_filename to output_filename
    spec = inspect.getfullargspec(plot_flat)
    if "output_filename" in spec.args:
        output_filename_arg = "output_filename"
    else:
        output_filename_arg = "ouput_filename"

    plot_flat(
        median_flat_filename=str(tmp_path / "median_flat.fits"),
        profile_ouput_filename=str(profile_output_filename),
        **{output_filename_arg: str(output_filename)},
    )

    # Check if the plot file was created
    assert output_filename.exists(), "The plot file was not created."
    assert profile_output_filename.exists(), "The profile plot file was not created."
