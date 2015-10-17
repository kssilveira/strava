# strava

Read strava distance PRs and calculate current ranks. See best.csv and best_with_ranks.csv for example outputs.

## Install

```
$ pip install stravalib
```

## Usage

```
$ python strava.py read 500 0 ACCESS_TOKEN >> best.csv
$ python strava.py rank best.csv best_with_ranks.csv
```

## Reference

https://strava.github.io/api/
