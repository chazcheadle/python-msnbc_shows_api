import requests
import sys
import json

# Convert numeric day of week to name
def weekday_name(dow):
  try:
    d = int(dow)
  except r:
    print(e)
    sys.exit(1)
  if d == 0:
    return 'sunday'
  if d == 1:
    return 'monday'
  if d == 2:
    return 'tuesday'
  if d == 3:
    return 'wednesday'
  if d == 4:
    return 'thursday'
  if d == 5:
    return 'friday'
  if d == 6:
    return 'saturday'

# Retrieve JSON feed    
def fetch_url():
  url = 'http://msnbc.com/api/1.0/shows.json'
  
  # Try to get response (r), from server
  try:
    r = requests.get(url)
  except requests.exceptions.RequestException as e:
    print(e)
    sys.exit(1)

  if (r.status_code == 200):
    try:
      # Convert response to JSON
      data = r.json()
    except e:
      print(e)
      sys.exit(1)

    for show in data['shows']:
      # Rename element for convenience.
      s = show['show']
      
      # Get issues/topics
      i_titles = []
      for issues in s['issues']:
        # Add new item to the list. (PHP's myArray[] = newItem).
        i_titles.append(issues['title'])
      # Create a comma separated string from list (PHP's implode()).
      i_titles = ", ". join(i_titles)

      # Build list of show times by day.
      s_times = {}
      for times in s['show_times']:
        # This check is here due to dirty data.
        if len(times['days_of_week']) > 0:
          for time in times['days_of_week']:
            # Only add unique day and times to the list.
            if time not in s_times:
              s_times[time] = [times['show_time']]
            else:
              s_times[time].append(times['show_time'])
            # Sort by show times.
            s_times[time].sort()            

      # Only display MSNBC shows not Shift.
      print(s['title'])
      # Print issues
      if i_titles:
        print(i_titles)
  
      # Print day of week and show times.
      if s_times:
        for day in s_times:
          print(weekday_name(day) + ': ' + ", ".join(s_times[day]))

fetch_url()
