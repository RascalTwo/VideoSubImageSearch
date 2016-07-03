import sys
import cv2
import app

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python cli.py video_id [options]"
        print ""
        print "Options:"
        print "  -q     -   Don't open any of the frames, only output them"
        print "  -c     -   Ignore cache"
        print "  -sf=#  -   Scan every Nth frame, defaults to 45"
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
    scanning_frames = None
    for arg in sys.argv:
        if arg.startswith("-sf"):
            scanning_frames = int(arg.split('=')[1])

    for eta in app.download_video(video_id, ignore_cache):
        print "ETA: " + eta + "        \r",
    print ""

    #Process video


    for hms, frame in app.process_video("cache/{}.mp4".format(video_id), scanning_frames):
        print "\r" + hms,
        if frame is None:
            continue

        print ""
        filename = "frames/{}.png".format(hms)
        cv2.imwrite(filename, frame)
        if not dont_open:
            cv2.imshow(hms, frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    print "Goodbye!"
