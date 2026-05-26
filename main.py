from script import generate_script
from searches import generate_searches
from images import search_images, download_images
from voice import generate_voice
from video import build_video

import os

topic = input("Enter topic: ")

# ------------------------
# SCRIPT
# ------------------------

generate_new_script = input(
    "Generate new script? (y/n): "
).lower()

if generate_new_script == "y":

    print("Generating script...")

    script = generate_script(topic)

    os.makedirs("output", exist_ok=True)

    with open(
        "output/script.txt",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(script)

else:

    print("Using existing script...")

    with open(
        "output/script.txt",
        "r",
        encoding="utf-8"
    ) as f:

        script = f.read()

# ------------------------
# IMAGES
# ------------------------

generate_new_images = input(
    "Generate new images? (y/n): "
).lower()

if generate_new_images == "y":

    print("Generating image searches...")

    image_searches = generate_searches(topic)

    print("\nImage searches generated:")

    for search in image_searches:

        print("-", search)

    all_images = []

    print("\nSearching images...")

    for search in image_searches:

        print(f"Searching: {search}")

        results = search_images(search)

        all_images.extend(results)

    print(f"\nFound {len(all_images)} images")

    # clear old images
    if os.path.exists("images"):

        for file in os.listdir("images"):

            os.remove(
                os.path.join("images", file)
            )

    print("\nDownloading images...")

    download_images(all_images)

else:

    print("Using existing images...")

# ------------------------
# VOICE
# ------------------------

generate_new_voice = input(
    "Generate new voice? (y/n): "
).lower()

if generate_new_voice == "y":

    print("\nGenerating voice...")

    generate_voice()

else:

    print("Using existing voice...")

# ------------------------
# VIDEO
# ------------------------

print("\nBuilding video...")

build_video()

print("\nDONE!")