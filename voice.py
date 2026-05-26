from gtts import gTTS


def generate_voice():

    with open("output/script.txt", "r", encoding="utf-8") as f:
        script = f.read()

    tts = gTTS(
        text=script,
        lang="en",
        slow=False
    )

    tts.save("audio/narration.mp3")

    print("Voice generated!")