import subprocess
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE = "songs.txt"
OUTPUT_DIR = "downloads"
MAX_WORKERS = 4

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

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(download_song, song) for song in songs]

    for _ in as_completed(futures):
        pass

print("All downloads finished.")
