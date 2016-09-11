import os
import time
import json
import fnmatch

def save(data):
  if not os.path.exists('data'):
    os.makedirs('data')

  filename = 'data/' + time.strftime("%b%d-%H%M%S") + '.json'
  with open(filename, 'w') as f:
    json.dump(data,f)

def read():
  d = []
  for file in os.listdir('data'):
    if fnmatch.fnmatch(file, '*.json'):
      with open('data/' + file) as f:
        data = json.load(f)
      d.append(data)
  return d

