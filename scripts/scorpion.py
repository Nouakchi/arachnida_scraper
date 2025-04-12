import os
import sys
import piexif
from PIL.ExifTags import TAGS

SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

def display_exif(file_name):
    
    if not os.path.isfile(file_name):
        print(f"[!] File '{file_name}' does not exist or is not accessible.")
        return

    if not file_name.lower().endswith(SUPPORTED_FORMATS):
        print(f"[!] Unsupported file format: {file_name}")
        return
    
    try:
        exif_dict = piexif.load(file_name)
    except Exception as e:
        print(f"[!] Failed to load EXIF data: {e}")
        return

    thumbnail = exif_dict.pop("thumbnail")
    
    # if thumbnail is not None:
    #     with open("thumbnail.jpg", "wb+") as f:
    #         f.write(thumbnail)
    
    for ifd_name in exif_dict:
        print("\n<-----{0}----->".format(ifd_name))
        for key in exif_dict[ifd_name]:
            try:
                print(TAGS.get(key, f"Unknown-{key}") , " :", exif_dict[ifd_name][key][:10])
            except Exception as e:
                print(TAGS.get(key, f"Unknown-{key}") , " :", exif_dict[ifd_name][key])
    if thumbnail:
        print("\n<-----thumbnail----->\n", thumbnail[:10])

    
def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <FILE1> <FILE2> ...")
        return

    for file_name in sys.argv[1:]:
        print(f"\n******* Image: {file_name} *******")
        display_exif(file_name)
    
if __name__ == "__main__":
    main()

