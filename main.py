import subprocess
import yt_dlp
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from itertools import cycle
from pydub import AudioSegment
import time
import os
from rich.align import Align
from halo import Halo
import random
import requests
import lyricsgenius

LASTFM_API_KEY = '14d1ed452c6143e3607da84c56c02f2b'
GENIUS_API_KEY = 'E9GElTHKRnIpdUBxqQ4kFK1bGImIMXBhe_5shlecQphT-yQpMZvaZCXWlDYcuUyK'

console = Console()

colors = cycle(["red", "green", "yellow", "blue", "magenta", "cyan"])
colors2 = cycle(["yellow", "red", "blue", "blue", "green", "cyan"])

def download_song(song_name):
    URLS = [f"ytsearch:{song_name}"]
    ydl_opts = {
        "quiet": True,
        "format": "bestaudio[ext=mp3]/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        spinner = Halo(text=f"Downloading {song_name}", spinner="runner")
        spinner.start()
        ydl.download(URLS)
        os.system("cls")
        spinner.succeed("Song downloaded successfully!")
        console.input("[bold yellow]Press Enter to continue[/bold yellow]")

def get_random_color():
    return random.choice(["blue", "green", "yellow", "red", "cyan", "magenta", "white"])

def list_downloaded_songs():
    console = Console()
    console.print("\nDownloaded Songs:", style="bold underline")

    files = os.listdir("downloads")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Number", style="dim")
    table.add_column("Song", style="dim")

    os.system("curl -sL https://s13.gifyu.com/images/SCRDW.gif -o gif.gif")
    os.system("kitty +kitten icat --align center gif.gif")

    for i, file in enumerate(files, start=1):
        random_color = random.choice(["blue", "green", "yellow", "red", "cyan", "magenta"])
        table.add_row(
            str(i),
            file[:-4],  # Show the file name without the .mp3 extension
            style=f"bold {random_color}"
        )

    console.print(table)

    return files

def play_song(song_index, files):
    try:
        song_index = int(song_index)
        if 1 <= song_index <= len(files):
            mp3_file = os.path.join("downloads", files[song_index - 1])
            song_name = files[song_index - 1][:-4]

            audio = AudioSegment.from_mp3(mp3_file)
            song_length = len(audio) / 1000
            os.system("cls")

            os.system("curl -sL https://s13.gifyu.com/images/SCRDW.gif -o gif.gif")
            os.system("kitty +kitten icat --align center gif.gif")

            playing_text = Text("Playing...", style=f"bold {get_random_color()}")
            song_name_text = Text(f"\n{song_name}", style=f"bold {get_random_color()}")
            duration_text = Text(f"\nDuration: {int(song_length//60):02d}:{int(song_length%60):02d}", style=f"bold {get_random_color()}")

            panel_content = playing_text + song_name_text + duration_text
            console.print(Panel(Align(panel_content, align="center"), box=box.ROUNDED, style=f"bold {get_random_color()}"))

            rich_colors = ["bold red", "bold green", "bold yellow", "bold blue", "bold magenta", "bold cyan"]

            audio.export("temp.wav", format="wav")
            subprocess.Popen(["start", "temp.wav"], shell=True)
            start_time = time.time()

            while time.time() - start_time < song_length:
                remaining_time = max(0, song_length - (time.time() - start_time))
                remaining_minutes, remaining_seconds = divmod(remaining_time, 60)

                remaining_minutes = int(remaining_minutes)
                formatted_seconds = str(int(remaining_seconds)).zfill(2)

                random_color = random.choice(rich_colors)

                console.print(f"Remaining time (Press q for exit): {remaining_minutes:02d}:{formatted_seconds}", style=random_color, end="\r")
                
                time.sleep(1)
                

            console.print("\nPlayback completed.")

    except ValueError:
        console.print("Invalid input. Please enter a valid number.", style="bold red")
        return

def styled_input(prompt, style):
    console.print(Panel.fit(Text(prompt, style=style), box=box.ROUNDED, style=f"bold {next(colors)}"))
    return console.input("📻 [magenta]Or type the text [bold yellow]menu[/bold yellow] to go back ➜  [/magenta]")

def get_popular_songs():
    try:
        response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={LASTFM_API_KEY}&format=json")
        response.raise_for_status()
        data = response.json()
        if "tracks" in data and "track" in data["tracks"]:
            popular_songs = [track["name"] for track in data["tracks"]["track"]]
            return popular_songs
        else:
            return []
    except Exception as e:
        console.print(f"Error during the request to Last.fm: {e}", style="bold red")
        return []

def get_lyrics(song_name):
    try:
        genius = lyricsgenius.Genius(GENIUS_API_KEY)
        song = genius.search_song(song_name)
        if song:
            return song.lyrics
        else:
            return "Lyrics not found for this song."
    except Exception as e:
        console.print(f"Error fetching lyrics from Genius: {e}", style="bold red")
        return "Error fetching lyrics."

def show_lyrics():
    os.system("cls")
    song_name = styled_input("Enter the name of the song to get lyrics:",  style=f'bold {next(colors)}')
    if song_name.lower() == "menu":
        return
    lyrics = get_lyrics(song_name)

    console.print(Panel.fit(
        Text("\nLyrics:", style="bold underline") +
        Text("\n" + lyrics, style="bold red"),
        box=box.ROUNDED, style="bold yellow",title="🔠 Lyrics"
    ))

def show_popular_songs(popular_songs):
    console = Console()

    if not popular_songs:
        console.print("Unable to fetch popular songs.", style="bold red")
        return

    console.print("\nPopular Songs:", style="bold underline")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Number", style="dim")
    table.add_column("Song", style="dim")

    for i, song in enumerate(popular_songs, start=1):
        random_color = random.choice(["blue", "green", "yellow", "red", "cyan", "magenta"])
        table.add_row(
            str(i),
            song,
            style=f"bold {random_color}"
        )

    console.print(Panel(table, box=box.ROUNDED, style="bold"))
    console.input("[bold yellow]Press Enter to continue[/bold yellow]")

def main():
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    while True:
        os.system("cls")

        os.system("curl -sL https://s13.gifyu.com/images/SCRDZ.gif -o gif.gif")
        os.system("kitty +kitten icat --align center gif.gif")

        console.print(Panel.fit(Text("🎤 Menu", justify="center"), box=box.ROUNDED, style=f"bold {get_random_color()}"))
        console.print("1. Download song", style="green")
        console.print("2. Listen to song", style="yellow")
        console.print("3. Search for popular songs", style="cyan")
        console.print("4. Get lyrics of a song", style="magenta")
        console.print("5. Exit", style="red")

        choice = console.input("Enter the number corresponding to the desired action (or type 'menu' to return to the main menu): ")

        if choice.lower() == "menu":
            continue

        if choice == "1":
            os.system("cls")

            os.system("curl -sL https://s13.gifyu.com/images/SCRor.gif -o gif.gif")
            os.system("kitty +kitten icat --align center gif.gif")

            song_name = styled_input("🎼 Enter the name of the song to download",  style=f'bold {next(colors)}')

            if song_name.lower() == "menu":
                continue
            os.system("cls")
            os.system("curl -sL https://s13.gifyu.com/images/SCROt.gif -o gif.gif")
            os.system("kitty +kitten icat --align center gif.gif")
            download_song(song_name)

        elif choice == "2":
            os.system("cls")
            files = list_downloaded_songs()
            if files:
                song_index = console.input("Enter the number of the song to listen to (or type 'menu' to return to the main menu): ")
                if song_index.lower() == "menu":
                    continue
                play_song(song_index, files)

            else:
                console.print("No songs downloaded.", style="bold red")
        elif choice == "3":
            os.system("cls")
            popular_songs = get_popular_songs()
            show_popular_songs(popular_songs)

        elif choice == "4":
            show_lyrics()

        elif choice == "5":
            console.print("Exiting the program.", style="bold red")
            break

        else:
            console.print("Invalid choice. Please try again.", style="bold red")

if __name__ == "__main__":
    main()
