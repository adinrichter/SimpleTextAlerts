import requests

def get_data(file):
  output = []
  f = open(f"src/{file}.txt", "r")
  plaintext = f.read()
  for line in plaintext.splitlines():
    output.append(line)
  return output

def send_alerts():
  for number in get_data("numbers"):
    print(number)





if __name__ == "__main__":
  send_alerts()



#requests.post('https://textbelt.com/text', {
#  'phone': '5037528477',
#  'message': 'Hello world',
#  'key': 'textbelt',
#})
