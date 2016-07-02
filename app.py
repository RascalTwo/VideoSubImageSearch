import cv2
import sys
import os
import subprocess

def seconds_to_hms(seconds):
    if seconds <= 60:
        return "00:00:{:02d}".format(seconds)
    if seconds <= 3600:
        minutes, seconds = divmod(seconds, 60)
        return "00:{:02d}:{:02d}".format(minutes, seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def download_video(video_id, redownload):
    if redownload and os.path.exists("output/{}.mp4".format(video_id)):
        os.unlink(os.path.exists("output/{}.mp4".format(video_id)))

    if os.path.exists("output/{}.mp4".format(video_id)):
        print "Video already downloaded"
        yield "00:00"
        return

    process = subprocess.Popen("youtube-dl {0} -o output/{0}.mp4 -f 135".format(video_id).split(" "), stdout=subprocess.PIPE, bufsize=1)
    print "Downloading Video..."
    last_line = ""
    while True:
        out = process.stdout.read(1)
        if not out and process.poll() is not None:
            break
        if not out:
            continue
        if out == "\n" or out == "\r":
            if "ETA" in last_line:
                yield last_line.split("ETA ")[1]
            last_line = ""
        else:
            last_line += out
    print "Video Downloaded."

def process_video(filepath, needle_filepath="numbersign.png"):
    video = cv2.VideoCapture(filepath)
    needle = cv2.imread(needle_filepath)
    i = 0
    while True:
        i += 1
        video.grab()
        if i % 45:
            continue
        print "\r" + str(seconds_to_hms(i / 30)),
        sys.stdout.flush()
        frame = video.retrieve()[1]
        if frame is None:
            break
        if cv2.minMaxLoc(cv2.matchTemplate(needle, frame[375:400, 15:35], cv2.cv.CV_TM_SQDIFF_NORMED))[0] > 0.01:
            continue
        yield str(seconds_to_hms(i / 30)), frame
    video.release()