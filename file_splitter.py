#!/usr/bin/env python
# -*-coding:utf-8 -*-
# File    :   file_splitter.py
# Time    :   22.06.2022
# Author  :   Daniel Weston
# Contact :   dtw545@bham.ac.uk

from pathlib import Path
import numpy as np
from tqdm import tqdm

folders = ["c-glutamicum", "m-bovis", "r-erythropolis"]
directory = "data"
save_dir = "split-data"


for folder in (pbar := tqdm(folders)):
    pbar.set_description(f"Reading {folder}...")
    path = Path(directory, folder)
    files = path.glob("*.txt")
    save_path = Path(save_dir, folder)
    # remove old files
    for file in (pbar2 := tqdm(save_path.glob("*.txt"), leave=False)):
        pbar2.set_description(f"Cleaning {file}")
        file.unlink()
    save_path.mkdir(parents=True, exist_ok=True)
    repeat = 1
    for file in (pbar3 := tqdm(files, leave=False)):
        pbar3.set_description(f"Reading {file}")
        data = np.loadtxt(file)[:, 2:]
        # get indices where the next point is larger, i.e. the run has restarted
        # assuming that raman wavenumber monotonically decreases
        indices = np.nonzero(np.diff(data[:, 0]) > 0)
        split_data = list(np.array_split(data, indices[0].ravel() + 1, axis=0))
        suffix = 0
        for arr in split_data:
            np.savetxt(
                Path(save_path, f"sample_{suffix}-rep_{repeat}.txt"),
                arr,
                header="wavenumber  intensity",
            )
            suffix += 1
        repeat += 1
