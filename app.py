import cv2
import time
import sys
import os
import subprocess
import threading

def seconds_to_hms(seconds):
    if seconds <= 60:
        return "00:00:{:02d}".format(seconds)
    if seconds <= 3600:
        minutes, seconds = divmod(seconds, 60)
        return "00:{:02d}:{:02d}".format(minutes, seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def download_video(video_id):
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

def process_video(video):
    numbersign = cv2.imread("numbersign.png")
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
            return
        if cv2.minMaxLoc(cv2.matchTemplate(numbersign, frame[375:400, 15:35], cv2.cv.CV_TM_SQDIFF_NORMED))[0] > 0.01:
            continue
        yield str(seconds_to_hms(i / 30)), frame

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Need a video URL"
        sys.exit()

    #Download video

    if "v=" in sys.argv[1]:
        video_id = sys.argv[1].split("v=")[1]
    elif "youtu.be" in sys.argv[1]:
        video_id = sys.argv[1].split(".be/")[1]
    else:
        video_id = sys.argv[1]

    for eta in download_video(video_id):
        print "ETA: " + eta + '        \r',
    print ""

    #Process video

    video = cv2.VideoCapture("output/{}.mp4".format(video_id))

    for i, (hms, frame) in enumerate(process_video(video)):
        filename = "output/{}.png".format(i)
        cv2.imwrite(filename, frame)
        cv2.imshow(hms, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    video.release()
    print "Goodbye!"
