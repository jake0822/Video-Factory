from google import genai

API_KEY = "AIzaSyDvT_ujeSyNSGTm5f3qOawqV5aPMPZFHWk"

client = genai.Client(api_key=API_KEY)


def generate_searches(topic):

    prompt = f"""
    Generate 15 short image search terms for:

    {topic}

    RULES:
    - short phrases only
    - 1 to 3 words
    - visually searchable
    - concrete subjects

    Return one search term per line.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    searches = response.text.splitlines()

    searches = [
        s.strip("- ").strip()
        for s in searches
        if s.strip()
    ]

    return searches