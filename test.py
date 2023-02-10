import requests

def get_data(file):
  output = []
  f = open(f"src/{file}.txt", "r")
  plaintext = f.read()
  for line in plaintext.splitlines():
    output.append(line)
  return output

key = get_data("key")[0]

resp = requests.post('https://textbelt.com/text', {
  'phone': '5037528477',
  'message': 'Hello world',
  'key': key,
})

print(resp.json())