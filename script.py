from google import genai
import os

API_KEY = "AIzaSyDvT_ujeSyNSGTm5f3qOawqV5aPMPZFHWk"

client = genai.Client(api_key=API_KEY)


def generate_script(topic):

    prompt = f"""
    Write a long-form YouTube documentary narration about:

    {topic}

    IMPORTANT:
    - 1500 to 2000 words
    - documentary style
    - engaging and conversational
    - written for audience retention
    - natural spoken narration

    DO NOT:
    - include titles
    - include markdown
    - include narrator labels
    - include stage directions
    - include music cues
    - include parentheses
    - include visual descriptions

    Output ONLY raw narration text.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text