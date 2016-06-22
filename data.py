import json

def save(data):
  filename = input('Filename: ')
  filename = 'data/' + filename + '.json'
  with open(filename, 'w') as f:
    json.dump(data,f)
