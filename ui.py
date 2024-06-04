
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time
import customtkinter as ctk
from utils.detect import get_label,load_model
# Set themes
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LoginApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Notification")
        self.window.geometry("300x200")  # Set the size of the window
        
        self.inf = ctk.CTkLabel(self.window, text="TRACKING BEHAVIOR")
        self.inf.pack()

        
        self.login_button = ctk.CTkButton(self.window, text="Start", command=self.start)
        self.login_button.pack()
        
    def start(self):
        self.window.destroy()
        CameraApp().show()
        
    def show(self):
        self.window.mainloop()
        
class CameraApp:
    def __init__(self, video_source=0):
        self.window = ctk.CTk()
        self.window.title("Streaming")
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        self.config()
        self.frame = None
        self.anchor = None
        self.history = []
        self.canvas = ctk.CTkCanvas(self.window, width=self.width, height= self.height)
        self.canvas.pack()

        self.fps_label = ctk.CTkLabel(self.window, text="FPS: ")
        self.fps_label.pack()
        self.get_anchor()
        self.frame_count = 0
        self.start_time = time.time()
        self.FM, self.session = load_model()
        
    def show(self):
        self.update()
        self.window.mainloop()
    def get_anchor(self):
        ret, self.anchor = self.vid.read()
    def get_size_source(self):
        ret, self.frame = self.vid.read()
        if ret:
            return self.frame.shape
        
    def config(self):
        self.number_of_frame_predict = 10  
        self.height, self.width,_ = self.get_size_source()
        self.height+=10
        self.width+=10
        self.thread_warning = 3        
        self.requests_after = 10
        self.strict = 0.6
                
    def destroy(self):
        self.vid.release()  # Release the video capture object
        self.window.destroy()
        
    def update(self):
        ret, self.frame = self.vid.read()
        if ret:
            idx = int(get_label(self.FM, self.session,self.anchor,self.frame)) # it will return 0 or 1
            self.frame_count+=1
            if idx == 0:
                self.canvas.configure(borderwidth=1, relief="solid", background="red")
            else:
                self.canvas.configure(borderwidth=1, relief="solid", background="green")
                
            # frame = cv2.resize(self.frame,(self.width,self.height))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(10, 10, image=self.photo, anchor=ctk.NW)
            
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 1: 
                fps = self.frame_count / elapsed_time
                self.fps_label.configure(text="FPS: {:.2f}".format(fps))
                self.frame_count = 0
                self.start_time = time.time()
        self.window.after(10, self.update)
        
LoginApp().show()