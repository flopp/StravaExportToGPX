# StravaExportToGPX
Convert the activites in a Strava export to GPX files


## Requirements

This needs

- Python >= 3.6
- a working installation of `gpsbabel` in your `$PATH`,
- a full Strava export ;)


## Usage Examples

### Convert Activities to GPX

Convert all 2018 "Run" and "Hike" activities from a Strava export to GPX (`export_123456789` is a directory containing an unzipped Strava export):

```
./strava2gpx.py --input export_123456789 --output gpxfiles --filter-type Run --filter-type Hike --filter-year 2018
```

### List Activity Types

List activity types (to be used with the `--filter-type` option when actually converting):

```
./strava2gpx.py --input export_123456789 --list-types

->

Activity types found in export_123456789:
- Hike
- Ride
- Run
- Snowshoe
- Swim
- Walk
- Workout

```
