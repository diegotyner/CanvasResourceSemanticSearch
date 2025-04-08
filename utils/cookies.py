import json


# Use a cookie.json file, can be created with a cookie saving chrome extension

def load_cookie_dict(file):
  with open(file, "r") as f:
    cookies_list = json.load(f)

    cookies_dict = {}
    for cookie in cookies_list:
      cookies_dict[cookie['name']] = cookie['value']
    return cookies_dict  # Return the dictionary
  
def load_cookie_list(file):
  with open(file, "r") as f:
    cookie_list = json.load(f)
  return cookie_list

if __name__ == '__main__':
  print("Running main file")