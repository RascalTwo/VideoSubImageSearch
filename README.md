# Video SubImage Searcher

Search through a YouTube video frames for found subimages.

https://user-images.githubusercontent.com/9403665/131947673-89d0a59d-2d5c-4cfb-a440-487d1a518668.mp4

https://user-images.githubusercontent.com/9403665/131947659-db17ebda-96a4-420e-bb64-4a1e96799b9c.mp4

Shows you the frame themselves, when they occurred, and saves them.

> Initially developed to get the entries of a WatchMojo video - scanning the entire video for the number
> graphic that's used whenever the entry title is on screen, but as you can see the program
> can be customized to search for any subimage within any YouTube video.

## How It's Made

**Tech Used:** Python, OpenCV, YouTube API, tkinter

With a provided search image, the program will search through the frames of a YouTube video for the image. It will then show you the frames themselves, when they occurred, and saves them.

Additionally the search frame rate and area can be customized, and an easily be used on any raw video files.

## Optimizations

While many optimizations were already made, from not searching every single frame, to allowing searching only a subarea of the video, there may exist better template matching algorithms that could be used aside from the default `TM_SQDIFF_NORMED` used in OpenCV.

## Lessons Learned

Much was learned about using OpenCV template matching, efficiently using the YouTube API, and writing reusable code for both a GUI and CLI interface.

## Usage

### CLI

`python cli.py http://www.youtube.com/watch?v=BBxLDFIgFCY`

`python cli.py http://youtu.be/BBxLDFIgFCY`

`python cli.py BBxLDFIgFCY`

#### Options

- `q`
  - Don't open any of the frames, only output them
- `-c`
  - Ignore cache
- `-sf=#`
  - Scan every Nth frame, defaults to 45
- `-fa=y:y2,x:x2`
  - Area to search frame for the -fa-nth needle
  - Where the top left corner is X=0 and Y=0

### GUI

`python gui.py`

## Dependencies

- Python 2.7+
- youtube-dl
- opencv

## Options

Every image within the `needles` folder is a subimage to search for, so you can add as many as you like.
