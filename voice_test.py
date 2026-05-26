import asyncio
import edge_tts

TEXT = """
The used sailboat market is quietly changing.
"""

VOICE = "en-US-GuyNeural"

OUTPUT_FILE = "test.mp3"


async def main():

    communicate = edge_tts.Communicate(
        TEXT,
        VOICE,
        rate="+15%"
    )

    await communicate.save(OUTPUT_FILE)

    print("DONE")


asyncio.run(main())