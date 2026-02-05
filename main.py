import subprocess
import re
from pathlib import Path

INPUT_FILE = "songs.txt"
OUTPUT_DIR = "downloads"

Path(OUTPUT_DIR).mkdir(exist_ok=True)

def is_valid_song(line):
    line = line.strip()
    return bool(line) and not line.startswith("###")

def clean_song(line):
    return re.sub(r"\(\d{4}\)", "", line).strip()

def download_song(song):
    print(f"Downloading: {song}")

    subprocess.run(
        [
            "yt-dlp",
            f"ytsearch1:{song} official audio",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--embed-thumbnail",
            "--embed-metadata",
            "--cookies", "cookies.txt",
            "-o", f"{OUTPUT_DIR}/{song}.%(ext)s",
            "--no-playlist",
            "--quiet",
            "--no-warnings",
        ],
        check=False,
    )

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    songs = [
        clean_song(line)
        for line in f
        if is_valid_song(line)
    ]

for song in songs:
    download_song(song)

print("All downloads finished.")
