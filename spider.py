import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin , urlparse
from pprint import pprint

args_length = len(sys.argv)
options = sys.argv
is_recursive = False
depth = 5
path = "./data/"
target = None
images = None
links = None

def get_links_of_links(target, depth):
    
    if depth <= 0:
        return
    
    for link in target:
        if link.startswith("http"):
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html5lib')
            tmp_target = [a['href'] for a in soup.find_all('a', href=True)]
            images = soup.find_all("img", src=True)
            download_images(link, images)
            if not is_recursive:
                return
            get_links_of_links(tmp_target, depth - 1)

def is_integer (value):
    try:
        int(value)
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
    elif options[i] == '-p':
        if i + 1 < args_length and os.path.isdir(options[i + 1]):
            path = options[i + 1]
            i += 1
        else:
            print("Invalid path for -p. The specified path must be a directory.")
            exit(1)
    else:
        if target is None:
            target = [options[i]]
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

# Create data folder for storing images if no path is provided
if not os.path.exists(path):
    os.makedirs(path)

# List of supported image file extensions
supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def download_images(link, images):

    for image in images:
        full_url = urljoin(link, image["src"])

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

    
get_links_of_links(target, depth)



