import threading
import time
from Tkinter import *
import cv2
import app


class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.thread = None
        self.sample_sizes = [4, 4]
        self.thumbnails = []
        self.raw_frames = [None for _ in range(25)]
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.output_frame = Frame(self)
        self.message = Label(self.output_frame, text="Sup")
        self.message.grid(row=0, column=0)

        self.timestamps = Listbox(self.output_frame, selectmode="multiple")
        self.timestamps.grid(row=1, column=0, sticky="NS")
        self.timestamps.bind("<<ListboxSelect>>", self.on_listbox_select)

        self.image_grid = Frame(self.output_frame)

        i = 0
        for x in xrange(5):
            for y in xrange(5):
                button = Button(self.image_grid, state=DISABLED, command = lambda i=i: self.on_image_click(i))
                
                button.bind("<Enter>", self.on_image_hover)
                button.grid(row=x, column=y)

                self.thumbnails.append(button)

                i += 1
        self.image_grid.grid(row=1, column=1)

        self.output_frame.pack()

        self.label = Label(self)
        self.label["text"] = "Enter Video Here"
        self.label.pack()
        self.input = Entry(self)
        self.input.pack()

        self.start = Button(self)
        self.start["text"] = "Start"
        self.start["command"] = self.start_process
        self.start.pack()

    def on_image_click(self, i):
        button = self.thumbnails[i]
        cv2.imshow(button.timestamp, self.raw_frames[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def on_listbox_select(self, event):
        indexes = event.widget.curselection()
        for i in range(25):
            if i in indexes:
                self.thumbnails[i].configure(highlightbackground="red")
            else:
                self.thumbnails[i].configure(highlightbackground="white")

    def on_image_hover(self, event):
        if not hasattr(event.widget, "timestamp"):
            return
        index = None
        for i in xrange(25):
            self.thumbnails[i].configure(highlightbackground="white")
            if self.thumbnails[i] == event.widget:
                index = i
        event.widget.configure(highlightbackground="red")
        if index is not None:
            self.timestamps.selection_clear(0, END)
            self.timestamps.selection_set(index)

    def start_process(self):
        self.start["text"] = "Stop"
        self.start["command"] = self.stop_process
        self.thread = threading.Thread(target=self.process)
        self.thread.daemon = True
        self.thread.start()

    def stop_process(self):
        self.thread = None
        self.start["text"] = "Start"
        self.start["command"] = self.start_process

    def process(self):
        input = self.input.get()
        if "v=" in input:
            video_id = input.split("v=")[1]
        elif "youtu.be" in input:
            video_id = input.split(".be/")[1]
        else:
            video_id = input

    
        self.message["text"] = "Video ID: {}".format(video_id)
        time.sleep(2)

        for eta in app.download_video(video_id, False):
            if not self.thread:
                return
            self.message["text"] = "ETA: " + eta

        #Process video
        self.message["text"] = "Video Downloaded"

        i = 0
        for hms, frame in app.process_video("cache/{}.mp4".format(video_id), None):
            if not self.thread:
                return

            self.message["text"] = hms
            if frame is None:
                continue

            filename = "frames/{}.png".format(hms)
            cv2.imwrite(filename, frame)
            self.raw_frames[i] = frame

            image = PhotoImage(file=filename).subsample(*self.sample_sizes)
            self.thumbnails[i].configure(image=image, state=NORMAL)
            self.thumbnails[i].image = image
            self.thumbnails[i].timestamp = hms

            for o in xrange(i):
                self.thumbnails[o].configure(highlightbackground="white")
            self.thumbnails[i].configure(highlightbackground="red")

            self.timestamps.insert(END, hms)
            self.timestamps.selection_clear(0, END)
            self.timestamps.selection_set(i)

            i += 1

        self.message["text"] = "{} frames found".format(i + 1)
        self.thread = None
        self.start["text"] = "Start"
        self.start["command"] = self.start_process


if __name__ == '__main__':
    root = Tk()
    gui = GUI(master=root)
    gui.mainloop()
