import os
import json
import time

def save(data):
  if not os.path.exists('data'):
    os.makedirs('data')

  filename = 'data/' + time.strftime("%Y%m%d-%H%M%S") + '.json'
  with open(filename, 'w') as f:
    json.dump(data,f)
