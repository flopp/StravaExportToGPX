#!/usr/bin/env python3

import argparse
import csv
import fileinput
import gzip
import pathlib
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional


def matches_filter_types(activity: Dict, filter_types: Optional[List]) -> bool:
    if not filter_types:
        return True
    activity_type = activity["type"].lower()
    for filter_type in filter_types:
        if filter_type.lower() == activity_type:
            return True
    return False


def matches_filter_years(activity: Dict, filter_years: Optional[List]) -> bool:
    if not filter_years:
        return True
    activity_year = activity["date"][0:4]
    if activity_year in filter_years:
        return True
    return False


GPSBABEL_FILE_TYPE = {
    "fit": "garmin_fit",
    "tcx": "gtrnctr",
}


def gpsbabel_convert(input_file_path, output_file_path, file_type):
    subprocess.run(
        [
            "gpsbabel",
            "-i",
            GPSBABEL_FILE_TYPE[file_type],
            "-f",
            input_file_path,
            "-o",
            "gpx",
            "-F",
            output_file_path,
        ]
    )


def strip_whitespaces_from_file(input_file_path):
    with fileinput.FileInput(files=(input_file_path,), inplace=True) as file:
        for line in file:
            print(line.strip())


def convert_activity(activity_file_name: str, target_gpx_file_name: str):
    # gpsbabel support both fit and fit.gz
    if activity_file_name.endswith(".fit") or activity_file_name.endswith(".fit.gz"):
        gpsbabel_convert(
            activity_file_name,
            target_gpx_file_name,
            'fit',
        )

    elif activity_file_name.endswith(".tcx"):
        with tempfile.NamedTemporaryFile() as fp:
            shutil.copyfile(activity_file_name, fp)
            # As gpsbabel does not support tcx files with trailing spaces, remove them
            strip_whitespaces_from_file(fp.name)
            gpsbabel_convert(
                fp.name,
                target_gpx_file_name,
                'tcx',
            )

    # As gpsbabel does not support tcx compressed file, gunzip first
    elif activity_file_name.endswith(".tcx.gz"):
        with gzip.open(activity_file_name, "rb") as gzip_file:
            with tempfile.NamedTemporaryFile() as fp:
                shutil.copyfileobj(gzip_file, fp)
                # As gpsbabel does not support tcx files with trailing spaces, remove them
                strip_whitespaces_from_file(fp.name)
                gpsbabel_convert(
                    fp.name,
                    target_gpx_file_name,
                    'tcx'
                )

    # For GPX files, nothing to do, just copy the file
    elif activity_file_name.endswith(".gpx"):
        shutil.copyfile(activity_file_name, target_gpx_file_name)

    # For compressed GPX files, just uncompress and copy the file
    elif activity_file_name.endswith(".gpx.gz"):
        with gzip.open(activity_file_name, "rb") as gzip_file:
            with open(target_gpx_file_name, "wb") as gpx_file:
                shutil.copyfileobj(gzip_file, gpx_file)
    else:
        print(
            f"Unrecognized/unsupported file format: {activity_file_name}\n"
        )


def print_usage_error(args_parser: argparse.ArgumentParser, message: str):
    args_parser.print_usage()
    sys.stderr.write(message)
    sys.exit(2)


def main():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        "--input",
        "-i",
        dest="strava_export",
        metavar="DIR",
        type=str,
        required=True,
        help="Directory containing the unzipped Strava export to work on.",
    )
    args_parser.add_argument(
        "--output",
        "-o",
        dest="output_dir",
        metavar="DIR",
        type=str,
        help="Put generated GPX files into this directory.",
    )
    args_parser.add_argument(
        "--filter-type",
        "-f",
        dest="filter_types",
        metavar="ACTIVITY_TYPE",
        type=str,
        action="append",
        help="Only convert activities with the given ACTIVITY_TYPE. May be used multiple times. Use --list-types to find out what types exist.",
    )
    args_parser.add_argument(
        "--list-types",
        "-l",
        dest="list_types",
        action="store_true",
        help="List all activity types found in the Strava export directory.",
    )
    args_parser.add_argument(
        "--filter-year",
        "-y",
        dest="filter_years",
        metavar="YEAR",
        type=str,
        action="append",
        help="Only convert activities with the given YEAR. May be used multiple times.",
    )

    args_parser.add_argument(
        "--verbose", "-v", dest="verbose", action="store_true", help="Verbose output."
    )

    args = args_parser.parse_args()

    strava_export_path = pathlib.Path(args.strava_export)
    activities_csv_path = strava_export_path / "activities.csv"

    if args.list_types:
        if args.output_dir or args.filter_types:
            print_usage_error(
                args_parser,
                "error: you cannot use --output or --filter-type together with --list.types\n",
            )
        activity_types = set()
        with activities_csv_path.open() as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for activity in csv_reader:
                activity_types.add(activity["type"])
        print(f"Activity types found in {args.strava_export}:")
        for activity_type in sorted(list(activity_types)):
            print(f"- {activity_type}")
    else:
        if not args.output_dir:
            print_usage_error(
                args_parser,
                "error: either --output or --list-types must be specified\n",
            )
        output_path = pathlib.Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        with activities_csv_path.open() as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for activity in csv_reader:
                activity_file_name = str(strava_export_path / activity["filename"])

                if not matches_filter_years(activity, args.filter_years):
                    if args.verbose:
                        print(
                            f'Skipping {activity_file_name}, year={activity["date"][0:4]}.'
                        )
                    continue

                if not matches_filter_types(activity, args.filter_types):
                    if args.verbose:
                        print(
                            f'Skipping {activity_file_name}, type={activity["type"]}.'
                        )
                    continue
                gpx_file_name = f"{activity['date']}_{activity['type']}_{activity['id']}.gpx"
                gpx_file_path = str(output_path / gpx_file_name)
                if args.verbose:
                    print(f"Converting {activity_file_name} to {gpx_file_path}.")
                convert_activity(activity_file_name, gpx_file_path)


if __name__ == "__main__":
    main()
