"""
This module processes resting-state fMRI data from the HCP-Young-Adult-2025 release.
It extracts timeseries from brain regions using an atlas, computes the connectome,
and saves the results along with the masker report.
"""

import re
import click
import pandas as pd
from pathlib import Path

from nilearn.connectome import ConnectivityMeasure
from nilearn.maskers import NiftiLabelsMasker


HCP_2025_PATTERN = re.compile(
    r"^.*/(?P<participant_id>[0-9]{6})/MNINonLinear/Results/"
    r"rfMRI_REST(?P<run>[12])_(?P<pe>LR|RL)/"
    r"rfMRI_REST(?P=run)_(?P=pe)_hp2000_clean_rclean_tclean\.nii\.gz$"
)


class RestingState:

    def __init__(self, path: Path, output: str = "results"):
        # Check if the path is from the HCP-Young-Adult-2025 release
        hcp_match = HCP_2025_PATTERN.match(path.as_posix())
        if not hcp_match:
            raise ValueError(
                f"Invalid HCP-Young-Adult-2025 rs-fMRI path:\n  {path}\n"
                "Expected: <participant_id>/MNINonLinear/Results/rfMRI_REST{1,2}_{LR,RL}/rfMRI_REST{1,2}_{LR,RL}_hp2000_clean_rclean_tclean.nii.gz"
            )
        output = Path(output)

        pid = f"sub-{hcp_match.group('participant_id')}"
        run = f"run-{hcp_match.group('pe')}{hcp_match.group('run')}"
        basename = f"{pid}_task-rest_{run}_seg-SENSAAS"

        # HCP-Young-Adult-2025
        self.path = path
        self.brainmask = path.parent / "brainmask_fs.2.nii.gz"

        # Define output filenames
        self.output_folder = output / pid / "func"
        self.timeseries = self.output_folder / f"{basename}_timeseries.tsv"
        self.report = self.output_folder / f"{basename}_report.html"
        self.relmat = (
            self.output_folder / f"{basename}_meas-PearsonCorrelation_relmat.tsv"
        )

    def make_output_folder(self):
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def save_timeseries(self, timeseries):
        pd.DataFrame(timeseries).to_csv(self.timeseries, sep="\t", index=False)

    def save_report(self, masker):
        masker.generate_report().save_as_html(self.report)

    def save_connectome(self, connectome):
        pd.DataFrame(connectome).to_csv(self.relmat, sep="\t", index=False)


@click.command()
@click.argument("atlas_path", nargs=1, type=click.Path(exists=True))
@click.argument("lut_path", nargs=1, type=click.Path(exists=True))
@click.argument("rs_path", nargs=1, type=click.Path(exists=True))
def main(atlas_path, lut_path, rs_path):
    """
    Process resting-state fMRI data to extract connectome.

    This command-line tool:
    1. Validates input resting-state fMRI data structure
    2. Extracts timeseries using an atlas
    3. Computes Pearson correlations connectome
    4. Saves timeseries, connectome, and visualization report

    Args:
        atlas_path (str): Path to atlas NIfTI file defining brain regions
        lut_path (str): Path to lookup table file for atlas labels
        rs_path (str): Path to resting-state fMRI NIfTI file
    """
    resting_state = RestingState(Path(rs_path))

    atlas_masker = NiftiLabelsMasker(
        labels_img=atlas_path,
        lut=lut_path,
        mask_img=resting_state.brainmask,
        smoothing_fwhm=5.0,
        standardize="zscore_sample",
        t_r=0.72,
    )

    correlation_measure = ConnectivityMeasure(
        kind="correlation",
        standardize="zscore_sample",
        vectorize=False,
    )

    # Extract timeseries and connectomes
    timeseries = atlas_masker.fit_transform(resting_state.path)
    connectome = correlation_measure.fit_transform([timeseries])[0]

    # Save results
    resting_state.make_output_folder()
    resting_state.save_timeseries(timeseries)
    resting_state.save_report(atlas_masker)
    resting_state.save_connectome(connectome)
