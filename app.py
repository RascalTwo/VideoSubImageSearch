import cv2
import time
import sys
import os
import youtube_dl
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
    process = subprocess.Popen("youtube-dl {} -o output/temp.mp4 -f 135".format(video_id).split(" "))
    print "Downloading Video..."
    process.communicate()
    print "Video Downloaded."

def process_video():
    global i, list_imgs, video
    numbersign = cv2.imread("numbersign.png")
    while True:
        i += 1
        video.grab()
        if i % 45:
            continue
        print "\r" + str(seconds_to_hms(i / 30)),
        sys.stdout.flush()
        frame = video.retrieve()[1]
        if cv2.minMaxLoc(cv2.matchTemplate(numbersign, frame[375:400, 15:35], cv2.cv.CV_TM_SQDIFF_NORMED))[0] > 0.01:
            continue
        list_imgs.append({"time": str(seconds_to_hms(i / 30)), "image": frame})

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

    download_video(video_id)

    #Process video

    video = cv2.VideoCapture("output/temp.mp4")
    list_imgs = []
    i = -1

    thread = threading.Thread(target=process_video)
    thread.daemon = True
    thread.start()

    last_i = -1
    while True:
        time.sleep(1)
        if i == last_i:
            break
        last_i = i

    print "\nVideo Processed"
    video.release()

    for i in range(len(list_imgs)):
        filename = "output/{}.png".format(len(list_imgs) - i)
        cv2.imwrite(filename, list_imgs[i]["image"])
        cv2.imshow(list_imgs[i]["time"], list_imgs[i]["image"])
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print "Goodbye!"
    os.remove("output/temp.mp4")