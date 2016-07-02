import sys
import cv2
import app

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python cli.py video_id [options]"
        print ""
        print "Options:"
        print "  -q   -   Don't open any of the images, only output the files"
        print "  -c   -   Ignore cache"
        sys.exit()

    #Download video

    if "v=" in sys.argv[1]:
        video_id = sys.argv[1].split("v=")[1]
    elif "youtu.be" in sys.argv[1]:
        video_id = sys.argv[1].split(".be/")[1]
    else:
        video_id = sys.argv[1]

    dont_open = "-q" in sys.argv
    ignore_cache = "-c" in sys.argv


    for eta in app.download_video(video_id, ignore_cache):
        print "ETA: " + eta + "        \r",
    print ""

    #Process video


    for hms, frame in app.process_video("output/{}.mp4".format(video_id)):
        print ""
        filename = "output/{}.png".format(hms)
        cv2.imwrite(filename, frame)
        if not dont_open:
            cv2.imshow(hms, frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    print "Goodbye!"
