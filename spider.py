import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin , urlparse


args_length = len(sys.argv)
options = sys.argv
is_recursive = False
depth = 5
path = "./data/"
target = None

def is_integer (value):
    try:
        if int(value):
            return True
    except ValueError:
        return False

i = 1
while i < args_length:
    if options[i] == '-r':
        is_recursive = True
    elif options[i] == '-l':
        if i + 1 < args_length and is_integer(options[i + 1]):
            depth = int(options[i + 1])
            i += 1
        else:
            print("Invalid depth value for -l. Please provide a valid integer.")
            exit(1)
    elif options[i] == '-p':
        if i + 1 < args_length and os.path.isdir(options[i + 1]):
            path = options[i + 1]
            i += 1
        else:
            print("Invalid path for -p. The specified path must be a directory.")
            exit(1)
    else:
        if target is None:
            target = options[i]
        else:
            print("Multiple URLs provided. Only one target URL is allowed.")
            exit(1)
    i += 1

# Final checks
if target is None:
    print("Error: No target URL provided.")
    exit(1)

# At this point, `is_recursive`, `depth`, `path`, and `target` are set.
print(f"Recursive: {is_recursive}, Depth: {depth}, Save Path: {path}, Target URL: {target}")


# List of supported image file extensions
supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

# URL = "https://www.hola.com/"
page = requests.get(target)

soup = BeautifulSoup(page.content, 'html5lib')

images = soup.find_all("img")

# Directory where the images will be saved
image_dir = "./downloads"
if not os.path.exists(path):
    os.makedirs(path)

for image in images:
    full_url = urljoin(target, image["src"])

    image_name = os.path.basename(urlparse(full_url).path).split('?')[0]

    # Check if the file extension is one of the supported types
    if not image_name.lower().endswith(supported_extensions):
        print(f"Skipping {image_name} (unsupported file type)")
        continue

    image_path = os.path.join(path, image_name)


    img_response = requests.get(full_url)

    try:
        if img_response.status_code == 200:
            with open(image_path, "wb") as file:
                file.write(img_response.content)
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download {full_url} {image_name}. HTTP status code: {img_response.status_code}")
    except Exception as e:
        print(f"Error downloading {image_name}: {e}")
