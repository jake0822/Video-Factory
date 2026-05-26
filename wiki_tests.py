import requests

SEARCH_TERM = "sailboat"

HEADERS = {
    "User-Agent": "VideoFactoryBot/1.0"
}

url = "https://commons.wikimedia.org/w/api.php"

params = {
    "action": "query",

    "generator": "search",

    "gsrnamespace": "6",

    "gsrsearch": SEARCH_TERM,

    "gsrlimit": "1",

    "prop": "imageinfo",

    # IMPORTANT
    "iiurlwidth": "1280",

    "iiprop": "url",

    "format": "json"
}

print("Searching Wikimedia...")

response = requests.get(
    url,
    params=params,
    headers=HEADERS
)

data = response.json()

pages = data["query"]["pages"]

first_page = list(pages.values())[0]

print("\nFOUND FILE:")
print(first_page["title"])

# IMPORTANT CHANGE
image_url = first_page["imageinfo"][0]["thumburl"]

print("\nTHUMB URL:")
print(image_url)

print("\nDownloading thumbnail...")

img_response = requests.get(
    image_url,
    headers=HEADERS
)

print("IMAGE STATUS:", img_response.status_code)

with open("test.jpg", "wb") as f:
    f.write(img_response.content)

print("\nDONE")
print("Saved as test.jpg")