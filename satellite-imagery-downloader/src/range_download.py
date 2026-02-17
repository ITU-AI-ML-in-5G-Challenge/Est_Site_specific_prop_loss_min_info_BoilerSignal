import os
import json
import cv2
import numpy as np
import csv
from image_downloading import download_image  # your existing function

file_dir = os.path.dirname(__file__)
prefs_path = os.path.join(file_dir, 'preferences.json')

# --- Default preferences ---
default_prefs = {
    "url": "https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
    "tile_size": 256,
    "channels": 3,
    "dir": os.path.join(file_dir, "range_images"),
    "headers": {
        "cache-control": "max-age=0",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"99\", \"Google Chrome\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    },
    "zoom": 21
}

# --- Load preferences ---
if os.path.isfile(prefs_path):
    with open(prefs_path, "r", encoding="utf-8") as f:
        prefs = json.load(f)
else:
    prefs = default_prefs
    with open(prefs_path, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2, ensure_ascii=False)
    print(f"Preferences file created in {prefs_path}")

# --- Ensure output directory exists ---
os.makedirs(prefs["dir"], exist_ok=True)
print(f"Saving images to: {prefs['dir']}")

# --- Latitude/Longitude bounding box ---
lat_min = 35.65601
lat_max = 35.69912
lon_min = 139.75306
lon_max = 139.79820

# --- Grid divisions ---
num_x = 50  # along longitude (columns)
num_y = 50  # along latitude (rows)

lat_edges = np.linspace(lat_min, lat_max, num_y + 1)
lon_edges = np.linspace(lon_min, lon_max, num_x + 1)

zoom = int(prefs["zoom"])
channels = int(default_prefs["channels"])
tile_size = int(default_prefs["tile_size"])
url_template = prefs["url"]
headers = prefs["headers"]

# --- Prepare CSV file ---
csv_path = os.path.join(prefs["dir"], "patch_latlon_ranges.csv")
csv_file = open(csv_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["filename", "lat_min", "lat_max", "lon_min", "lon_max"])

# --- Download all patches with grid-based filenames ---
for i in range(num_x):
    for j in range(num_y):
        lat1 = lat_edges[j + 1]  # top
        lat2 = lat_edges[j]      # bottom
        lon1 = lon_edges[i]      # left
        lon2 = lon_edges[i + 1]  # right

        # Filename as x-column y-row (padded 2 digits)
        filename = f"x{i+1:02d}y{j+1:02d}.png"

        # Download the image patch
        try:
            img = download_image(lat1, lon1, lat2, lon2, zoom, url_template, headers, tile_size, channels)
            cv2.imwrite(os.path.join(prefs["dir"], filename), img)

            # Write lat/lon range to CSV
            csv_writer.writerow([filename, lat2, lat1, lon1, lon2])

            print(f"Saved {filename} with lat:({lat2},{lat1}) lon:({lon1},{lon2})")
        except Exception as e:
            print(f"Failed to download patch {filename} at ({lat1},{lon1}) -> ({lat2},{lon2}): {e}")

csv_file.close()
print(f"Downloaded all patches. Lat/Lon ranges saved to {csv_path}")
