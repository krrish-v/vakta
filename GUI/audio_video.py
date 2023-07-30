import yt_dlp as youtube_dl
import os
from pytube import Search
import subprocess
from subprocess import Popen, PIPE
from platform import system

class Open_file:
    OSNAME = system().lower()

    def get_open_command(self, filepath):
        """
        Get the console command to open the file
        """

        if 'windows' in self.OSNAME: opener = 'start'
        elif 'osx' in self.OSNAME or 'darwin' in self.OSNAME: opener = 'open'
        else: opener = 'xdg-open'
        return '{opener} "{filepath}"'.format(opener=opener, filepath=filepath)


    def opener(self, filepath):
        """
        Method to open the file with the default program in a subprocess.
        As being called in a subprocess, it will not block the current one.
        This method runs the command on a subprocess using the default system shell.
        """
        command = self.get_open_command(filepath)

        subproc = Popen(
            command,
            stdout=PIPE, stderr=PIPE, shell=True
        )
        subproc.wait()
        return subproc


def download_ytvid_as_mp3(video_url):

    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
    filename = f"songs/{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

        return filename


def search_and_get_audio(query):
    search_query = f"{query} official video"  # Append "official video" to improve search results
    results = Search(search_query).results

    try:
        if results:
            video = results[0]
            video_url = video.watch_url

            filename = download_ytvid_as_mp3(video_url)

            Open_file().opener(filename)

        else: return False
    except: return False

#search_and_get_audio('Bad lier')
