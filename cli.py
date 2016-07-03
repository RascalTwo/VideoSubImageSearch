import sys
import cv2
import app

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python cli.py video_id [options]"
        print ""
        print "Options:"
        print "  -q            -   Don't open any of the frames, only output them"
        print "  -c            -   Ignore cache"
        print "  -sf=#         -   Scan every Nth frame, defaults to 45"
        print "  -fa=y:y2,x:x2 -   Area to search frame for the -fa-nth needle"
        print "                    Where the top left corner is X=0 and Y=0"
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
    search_areas = []
    for arg in sys.argv:
        if arg.startswith("-sf"):
            scanning_frames = int(arg.split('=')[1])
        elif arg.startswith("-fa"):
            fa = []
            for part in arg.split("-fa=")[1].split(","):
                c, c2 = part.split(":")
                c = int(c)
                c2 = int(c2)
                fa.append(c)
                fa.append(c2)
            search_areas.append(fa)

    for eta in app.download_video(video_id, ignore_cache):
        print "ETA: " + eta + "        \r",
    print ""

    #Process video


    for hms, frame in app.process_video("cache/{}.mp4".format(video_id), scanning_frames, search_areas=search_areas):
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
