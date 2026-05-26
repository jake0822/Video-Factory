import os
import subprocess


def build_video():

    image_folder = "images"
    temp_folder = "temp_clips"

    os.makedirs(temp_folder, exist_ok=True)

    image_files = sorted([
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith((
            ".jpg",
            ".jpeg",
            ".png"
        ))
    ])

    if len(image_files) == 0:

        print("NO IMAGES FOUND")
        return

    max_images = 35

    if len(image_files) > max_images:
        image_files = image_files[:max_images]

    # ------------------------
    # GET AUDIO LENGTH
    # ------------------------

    probe = subprocess.check_output([
        "ffprobe",
        "-v", "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        "audio/narration.mp3"
    ])

    audio_duration = float(
        probe.decode().strip()
    )

    duration_per_image = (
        audio_duration / len(image_files)
    )

    print(
        f"{duration_per_image:.2f} sec per image"
    )

    # ------------------------
    # CREATE CLIPS
    # ------------------------
    print("\nRendering final video...\n")
    clip_paths = []

    for i, image in enumerate(image_files):

        output_clip = (
        os.path.abspath(
            f"{temp_folder}/clip_{i}.mp4"
        )
)

        percent = int(
            ((i + 1) / len(image_files)) * 100
        )

        bar_length = 30

        filled = int(
            bar_length * (i + 1)
            / len(image_files)
        )

        bar = (
            "█" * filled
            + "-"
            * (bar_length - filled)
        )

        print(
            f"\r[{bar}] "
            f"{percent}% "
            f"({i+1}/{len(image_files)})",
            end="",
            flush=True
        )

        cmd = [
            "ffmpeg",
            "-y",
            "-loglevel", "error",

            "-framerate", "24",
            "-loop", "1",
            "-i", image,

            "-vf",

            (
                "scale=-2:1440,"
                "zoompan="
                "z='zoom+0.00025':"
                f"d={int(duration_per_image * 24)}:"
                "s=2560x1440:fps=24"
            ),

            "-t",
            str(duration_per_image),

            "-c:v",
            "h264_nvenc",

            "-pix_fmt",
            "yuv420p",

            output_clip
        ]

        subprocess.run(cmd)

        clip_paths.append(output_clip)
    print()

    # ------------------------
    # CONCAT FILE
    # ------------------------

    concat_file = os.path.abspath(
    "temp_clips/concat.txt"
)

    with open(concat_file, "w") as f:

        for clip in clip_paths:

            f.write(
                f"file '{clip}'\n"
            )

    # ------------------------
    # CONCATENATE
    # ------------------------

    print("\nCombining clips...")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-loglevel", "error",

        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,

        "-c:v", "h264_nvenc",

        "-pix_fmt", "yuv420p",

        "temp_clips/video_only.mp4"
    ])

    print("Adding narration audio...")

    subprocess.run([
        "ffmpeg",
        "-y",
        "-loglevel", "error",

        "-i", "temp_clips/video_only.mp4",
        "-i", "audio/narration.mp3",

        "-c:v", "copy",
        "-c:a", "aac",

        "-shortest",

        "output/final_video.mp4"
    ])

    print("DONE!")