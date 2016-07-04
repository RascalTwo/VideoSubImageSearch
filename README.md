# Video SubImage Searcher

Search through a YouTube video frames for found subimages.

Shows you the frame themselves, when they occured, and saves them.

> Initally developed to get the entries of a WatchMojo video - scanning the entire video for the number
> graphic that's used whenever the entry title is on screen, but as you can see the program
> can be customized to search for any subimage within any YouTube video.

## Usage

### CLI

`python cli.py http://www.youtube.com/watch?v=BBxLDFIgFCY`

`python cli.py http://youtu.be/BBxLDFIgFCY`

`python cli.py BBxLDFIgFCY`

https://user-images.githubusercontent.com/9403665/131947659-db17ebda-96a4-420e-bb64-4a1e96799b9c.mp4

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

https://user-images.githubusercontent.com/9403665/131947673-89d0a59d-2d5c-4cfb-a440-487d1a518668.mp4


## Dependencies

- Python 2.7+
- youtube-dl
- opencv

## Options

Every image within the `needles` folder is a subimage to search for, so you can add as many as you like.

## Technical

First calls `youtube-dl` to download the provided youtube video.

Then searches every second second of the video for a matching subimage, and saves that image if it's found.

Lastly presents all the images to the end user.
