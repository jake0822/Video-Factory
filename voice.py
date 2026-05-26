import asyncio
import edge_tts
import os


VOICE = "en-US-AndrewNeural"


async def generate():

    with open(
        "output/script.txt",
        "r",
        encoding="utf-8"
    ) as f:

        text = f.read()

    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate="+1%"
    )

    os.makedirs("audio", exist_ok=True)

    await communicate.save(
        "audio/narration.mp3"
    )

    print("Voice generated!")


def generate_voice():

    asyncio.run(generate())