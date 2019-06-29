# StravaExportToGPX
Convert the activites in a Strava export to GPX files


## Requirements

This needs

- Python >= 3.6
- a working installation of `gpsbabel` in your `$PATH`,
- a full [Strava export ZIP file](#getting-your-strava-export-zip-file) ;)


## Usage Examples

### Convert Activities to GPX

Convert all 2018 "Run" and "Hike" activities from a Strava export to GPX (`export_123456789.zip` is a Strava export ZIP file):

```
./strava2gpx.py --input export_123456789.zip --output gpxfiles --filter-type Run --filter-type Hike --filter-year 2018
```

### List Activity Types

List activity types (to be used with the `--filter-type` option when actually converting):

```
./strava2gpx.py --input export_123456789.zip --list-types

->

Activity types found in export_123456789.zip:
- Hike
- Ride
- Run
- Snowshoe
- Swim
- Walk
- Workout

```

## Getting your Strava Export ZIP File

The process for bulk exporting activity data from Strava is described in detail on [Strava's support pages](https://support.strava.com/hc/en-us/articles/216918437-Exporting-your-Data-and-Bulk-Export#Bulk).

Here's the short version:

1. Log in to Strava.
2. Go to the "[Download or Delete Your Account](https://www.strava.com/athlete/delete_your_account)" page.
3. Click the "Request Your Archive" button in the "Download Request" section.
4. Strava will send a download link for an `export_123456789.zip` file via email. This may take some time.
