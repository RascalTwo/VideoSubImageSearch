import sys
import cv2
import app

if __name__ == '__main__':
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

    for eta in app.download_video(video_id):
        print "ETA: " + eta + '        \r',
    print ""

    #Process video


    for i, (hms, frame) in enumerate(app.process_video("output/{}.mp4".format(video_id))):
        filename = "output/{}.png".format(i)
        cv2.imwrite(filename, frame)
        cv2.imshow(hms, frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    print "Goodbye!"
