# WatchMojo List Video to List

Goes through a WatchMojo video and extracts the list contents.

Shows you the images of the entries.

# Dependencies

- Python 2.7+
- youtube-dl
- opencv

# Usage

`python app.py http://www.youtube.com/watch?v=BBxLDFIgFCY`

`python app.py http://youtu.be/BBxLDFIgFCY`

`python app.py BBxLDFIgFCY`

# Technical

First calls `youtube-dl` to download the provided youtube video.

Then searches every second second of the video for a list entry, and saved that image if it's found.

Lastly presents all the images to the end user, and deletes the downloaded video file.
