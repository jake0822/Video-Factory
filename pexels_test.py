import requests

API_KEY = "7QBz4i1PFFerov0HCDDaPDQM3TfNIPiKn9c6AfvmARtSFeQ8fH4OF7nD"

headers = {
    "Authorization": API_KEY
}

query = "sailboat"

url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"

response = requests.get(
    url,
    headers=headers
)

print("STATUS:", response.status_code)

data = response.json()

photo = data["photos"][0]

image_url = photo["src"]["large"]

print("\nIMAGE URL:")
print(image_url)

img = requests.get(image_url)

with open("test.jpg", "wb") as f:
    f.write(img.content)

print("\nDONE")