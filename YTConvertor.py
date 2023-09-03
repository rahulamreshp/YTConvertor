import os
import certifi
import ssl
from pytube import YouTube
import moviepy.editor as mp
import psutil

ssl._create_default_https_context = ssl._create_unverified_context
YouTube.DEFAULT_RETRIES = 5
YouTube.DEFAULT_CA_CERTS_PATH = certifi.where()


def download_and_convert(url, conversion_option):
    try:
        yt = YouTube(url)
        video_title = yt.title

        if conversion_option == "mp4":
            resolution = input("Enter the desired resolution (360p, 480p, 720p, 1080p): ")
            while resolution not in ["360p", "480p", "720p", "1080p"]:
                print("Invalid resolution. Please enter a valid resolution.")
                resolution = input("Enter the desired resolution (360p, 480p, 720p, 1080p): ")
            video_stream = yt.streams.filter(file_extension="mp4", res=resolution).first()
            mp4_file = f"{video_title}.mp4"
            video_stream.download(filename=video_title)
            os.rename(video_title, mp4_file)
            close_ffmpeg_processes()
            print(f"Download completed: {mp4_file}")

        elif conversion_option == "mp3":
            bitrate = input("Enter the desired bitrate (128, 256, 512): ")
            while bitrate not in ["128", "256", "512"]:
                print("Invalid bitrate. Please enter a valid bitrate.")
                bitrate = input("Enter the desired bitrate (128, 256, 512): ")
            video_stream = yt.streams.filter(file_extension="mp4", res="360p").first()
            mp4_file = f"{video_title}"
            video_stream.download(filename=video_title)
            mp4_audio_clip = mp.VideoFileClip(mp4_file)
            mp3_file = f"{video_title}.mp3"
            mp4_audio_clip.audio.write_audiofile(mp3_file, codec='mp3', bitrate=f"{bitrate}k")
            close_ffmpeg_processes()
            os.remove(mp4_file)
            print(f"Conversion to MP3 completed: {mp3_file}")

        elif conversion_option == "wav":
            video_stream = yt.streams.filter(file_extension="mp4", res="360p").first()
            mp4_file = f"{video_title}"
            video_stream.download(filename=video_title)
            wav_file = f"{video_title}.wav"
            mp4_audio_clip = mp.VideoFileClip(mp4_file)
            mp4_audio_clip.audio.write_audiofile(wav_file, codec='pcm_s16le', fps=44100)
            close_ffmpeg_processes()
            os.remove(mp4_file)
            print(f"Conversion to WAV completed: {wav_file}")

        else:
            print("Invalid conversion option")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def close_ffmpeg_processes():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if "ffmpeg" in process.info['name']:
                os.kill(process.info['pid'], psutil.signal.SIGTERM)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


if __name__ == "__main__":
    while True:
        youtube_url = input("Enter the YouTube URL (Type 'exit' to quit): ")
        if youtube_url.lower() == 'exit':
            break
        conversion_option = input("Enter the desired conversion option (mp4, mp3, wav): ")
        while conversion_option not in ["mp4", "mp3", "wav"]:
            print("Invalid conversion option. Please enter a valid option.")
            conversion_option = input("Enter the desired conversion option (mp4, mp3, wav): ")
        download_and_convert(youtube_url, conversion_option)
