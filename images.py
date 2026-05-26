import requests
import os

PEXELS_API_KEY = "7QBz4i1PFFerov0HCDDaPDQM3TfNIPiKn9c6AfvmARtSFeQ8fH4OF7nD"

HEADERS = {
    "Authorization": PEXELS_API_KEY
}


def search_images(query, limit=5):

    url = "https://api.pexels.com/v1/search"

    params = {
        "query": query,
        "per_page": limit
    }

    print(f"\nPexels search: {query}")

    response = requests.get(
        url,
        headers=HEADERS,
        params=params
    )

    print("STATUS:", response.status_code)

    try:
        data = response.json()

    except Exception as e:

        print("JSON ERROR")
        print(e)

        return []

    image_urls = []

    if "photos" not in data:

        print("NO RESULTS")
        return []

    for photo in data["photos"]:

        image_url = photo["src"]["large"]

        print("FOUND:", image_url)

        image_urls.append(image_url)

    return image_urls


def download_images(image_urls):

    from PIL import Image
    from io import BytesIO

    os.makedirs("images", exist_ok=True)

    image_count = 0

    for url in image_urls:

        try:

            response = requests.get(
                url,
                timeout=15
            )

            image = Image.open(
                BytesIO(response.content)
            )

            # normalize image
            image = image.convert("RGB")

            filepath = f"images/img_{image_count}.jpg"

            image.save(
                filepath,
                "JPEG",
                quality=95
            )

            print(f"Downloaded: {filepath}")

            image_count += 1

        except Exception as e:

            print("FAILED DOWNLOAD")
            print(e)