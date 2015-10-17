"""Client for strava.

See README.md for instructions.
"""

import csv
from stravalib import client as client_mod

import sys

FIELD_NAMES = ('start_date', 'pr_rank', 'name', 'distance', 'elapsed_time', 'id')


def rank():
  input_filename = sys.argv[2]
  output_filename = sys.argv[3]
  efforts_by_distance = {}
  efforts_by_date_and_distance = {}
  with open(input_filename, 'r') as input_file:
    reader = csv.DictReader(input_file, FIELD_NAMES)
    for best_effort in reader:
      efforts_by_distance.setdefault(best_effort['distance'], []).append(
          best_effort)
      efforts_by_date_and_distance.setdefault(
          best_effort['start_date'], {})[best_effort['distance']] = best_effort

  for efforts in efforts_by_distance.itervalues():
    sorted_efforts = sorted(efforts, key=lambda e: e['elapsed_time'])
    for cur_rank, best_effort in enumerate(sorted_efforts):
      best_effort['cur_rank'] = cur_rank + 1

  with open(output_filename, 'w') as output_file:
    writer = csv.DictWriter(output_file, FIELD_NAMES + ('cur_rank',))
    writer.writeheader()
    for unused_date, distance_to_effort in sorted(
        efforts_by_date_and_distance.iteritems()):
      for unused_distance, best_effort in sorted(distance_to_effort.iteritems()):
        writer.writerow(best_effort)


def read():
  activities_limit = int(sys.argv[2])
  is_debug = bool(int(sys.argv[3]))
  client = client_mod.Client()
  client.access_token = sys.argv[4]
  activities = list(client.get_activities(limit=activities_limit))
  for index, summary_activity in enumerate(activities):
    sys.stderr.write('processing activity %s/%s\n' % (index, activities_limit))
    if summary_activity.type != 'Run':
      continue
    activity = client.get_activity(summary_activity.id)
    best_efforts = [
        best_effort for best_effort in activity.best_efforts
        if best_effort.pr_rank]
    if not best_efforts:
      continue
    if is_debug:
      print (
          'type: %s, start_date: %s, average_speed: %s, best_efforts: %s, '
          'splits_metric: %s, average_heartrate: %s, laps: %s') % (
          activity.type, activity.start_date, activity.average_speed,
          activity.best_efforts, activity.splits_metric,
          activity.average_heartrate, activity.laps)
    for best_effort in best_efforts:
      if is_debug:
        print (
            'name: %s, distance: %s, pr_rank: %s, elapsed_time: %s, '
            'average_heartrate: %s, max_heartrate: %s' % (
                best_effort.name, best_effort.distance, best_effort.pr_rank,
                best_effort.elapsed_time, best_effort.average_heartrate,
                best_effort.max_heartrate))
      print '%s, %s, %s, %s, %s, %s' % (
          activity.start_date, best_effort.pr_rank, best_effort.name,
          best_effort.distance.num, best_effort.elapsed_time, activity.id)


def main():
  actions = {
      'read': read,
      'rank': rank,
  }
  action = sys.argv[1]
  actions[action]()


if __name__ == '__main__':
  main()
