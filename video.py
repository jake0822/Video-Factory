from moviepy import *
import os
import random


def build_video():

    audio = AudioFileClip("audio/narration.mp3")

    image_files = []

    for f in os.listdir("images"):

        if f.lower().endswith((
            ".jpg",
            ".jpeg",
            ".png"
        )):

            image_files.append(
                os.path.join("images", f)
            )

    if len(image_files) == 0:

        print("NO IMAGES FOUND")
        return
    
    # limit total images
    max_images = 35

    if len(image_files) > max_images:
        image_files = image_files[:max_images]

    duration_per_image = (
        audio.duration / len(image_files)
    )
    

    clips = []

    for image in image_files:

        try:

            print(f"Loading: {image}")

            clip = (
                ImageClip(image)
                .with_duration(duration_per_image)
                .resized(height=900)
            )

            # smoother zoom
            zoom = random.uniform(1.02, 1.05)

            clip = clip.resized(
                lambda t:
                1 + (zoom - 1)
                * (t / duration_per_image)
            )

            # center crop to 1280x720
            clip = clip.cropped(
                x_center=clip.w / 2,
                y_center=clip.h / 2,
                width=1280,
                height=720
            )

            clips.append(
                clip
            )

        except Exception as e:

            print(f"SKIPPED BAD IMAGE: {image}")
            print(e)

    if len(clips) == 0:

        print("NO VALID IMAGES")
        return

    video = concatenate_videoclips(
        clips,
        method="compose"
    )

    video = video.with_audio(audio)

    video.write_videofile(
        "output/final_video.mp4",
        fps=24
    )


if __name__ == "__main__":
    build_video()