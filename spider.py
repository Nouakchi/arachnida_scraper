import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin , urlparse


# List of supported image file extensions
supported_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

URL = "https://profile.intra.42.fr/users/onouakch"
page = requests.get(URL)

print(page)

soup = BeautifulSoup(page.content, 'html5lib')

images = soup.find_all("img")

# Directory where the images will be saved
image_dir = "./downloads"
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

for image in images:
    full_url = urljoin(URL, image["src"])

    image_name = os.path.basename(urlparse(full_url).path).split('?')[0]

    # Check if the file extension is one of the supported types
    if not image_name.lower().endswith(supported_extensions):
        print(f"Skipping {image_name} (unsupported file type)")
        continue

    image_path = os.path.join(image_dir, image_name)


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
