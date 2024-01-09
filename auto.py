import sys
import time
import logging
import os 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from shutil import move

source_dir = ""
music_dir = ""
videos_dir = ""
pdf_dir = ""
image_dir = ""

image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]

audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


class MoverHandler(FileSystemEventHandler):
    def on_any_event(self,event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name,ext = os.path.splitext(entry.name) 
                dir = os.path.join(source_dir,entry.name) 
                if audio_extensions.count(ext) == 1:
                    dest = os.path.join(music_dir,entry.name)
                elif video_extensions.count(ext) == 1:
                    dest =  os.path.join(videos_dir,entry.name)
                elif document_extensions.count(ext) == 1:
                    dest = os.path.join(pdf_dir,entry.name)
                elif image_extensions.count(ext) == 1:
                    dest = os.path.join(image_dir,entry.name)
                else: 
                    continue

                move(dir,dest)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

