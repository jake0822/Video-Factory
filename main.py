from script import generate_script
from searches import generate_searches
from images import search_images, download_images
from voice import generate_voice
from video import build_video

import os
import json

topic = input("Enter topic: ")

os.makedirs("temp", exist_ok=True)

cache_file = "temp/content.json"

# ------------------------
# LOAD CACHE
# ------------------------

if os.path.exists(cache_file):

    use_cache = input(
        "Use cached script/searches? (y/n): "
    ).lower()

else:

    use_cache = "n"

# ------------------------
# USE CACHE
# ------------------------

if use_cache == "y":

    print("Using cached content...")

    with open(cache_file, "r", encoding="utf-8") as f:

        data = json.load(f)

        script = data["script"]
        image_searches = data["image_searches"]

# ------------------------
# GENERATE NEW CONTENT
# ------------------------

else:

    print("Generating script...")

    script = generate_script(topic)

    print("Generating image searches...")

    image_searches = generate_searches(topic)

    # save cache
    with open(cache_file, "w", encoding="utf-8") as f:

        json.dump({
            "script": script,
            "image_searches": image_searches
        }, f, indent=4)

# ------------------------
# CLEAN SCRIPT
# ------------------------

script = clean_script(script)

# ------------------------
# SAVE SCRIPT
# ------------------------

os.makedirs("output", exist_ok=True)

with open(
    "output/script.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(script)

# ------------------------
# SHOW SEARCHES
# ------------------------

print("\nImage searches generated:")

for search in image_searches:

    print("-", search)

# ------------------------
# SEARCH IMAGES
# ------------------------

all_images = []

print("\nSearching images...")

for search in image_searches:

    print(f"Searching: {search}")

    results = search_images(search)

    all_images.extend(results)

print(f"\nFound {len(all_images)} images")

# ------------------------
# DOWNLOAD IMAGES
# ------------------------

print("\nDownloading images...")

download_images(all_images)

# ------------------------
# GENERATE VOICE
# ------------------------

print("\nGenerating voice...")

generate_voice()

# ------------------------
# BUILD VIDEO
# ------------------------

print("\nBuilding video...")

build_video()

print("\nDONE!")