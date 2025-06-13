import cv2
import numpy as np
import pyautogui
import time
from datetime import datetime
import os
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk

class ScreenRecorder:
    def __init__(self, output_dir="recordings"):
        # Create output directory if it doesn't exist
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize screen parameters
        self.screen_size = pyautogui.size()
        self.recording = False
        
        # Define available resolutions
        screen_width = self.screen_size.width
        screen_height = self.screen_size.height
        self.resolutions = {
            "Native": (screen_width, screen_height),
            "1080p": (1920, 1080),
            "720p": (1280, 720),
            "480p": (640, 480)
        }
        
        # Cyberpunk theme colors
        self.bg_dark = "#1a1a1a"  # Dark grey background
        self.bg_darker = "#202020"  # Slightly darker grey
        self.neon_pink = "#ff2e97"  # Neon pink
        self.neon_blue = "#00fff9"  # Neon cyan/blue
        self.neon_purple = "#bf00ff"  # Neon purple
        self.text_color = "#ffffff"  # White text
        
        # Create GUI window with larger size
        self.root = tk.Tk()
        self.root.title("Screen Recorder")
        self.root.geometry("550x850")
        self.root.configure(bg=self.bg_dark)
        
        # Load and set the logo as the window icon
        logo_image = Image.open("logo.png")
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.root.iconphoto(False, logo_photo)
        
        # Create main frame with more padding
        frame = tk.Frame(self.root, bg=self.bg_dark)
        frame.pack(expand=True, fill=tk.BOTH, padx=40, pady=40)
        
        # Title with neon effect
        title_label = tk.Label(
            frame,
            text="SCREEN RECORDER",
            font=("Consolas", 28, "bold"),  # Larger font
            bg=self.bg_dark,
            fg=self.neon_blue,
            pady=10
        )
        title_label.pack(pady=(0, 30))  # More padding below title
        
        # Subtitle
        subtitle_label = tk.Label(
            frame,
            text="< SELECT QUALITY >",
            font=("Consolas", 12),
            bg=self.bg_dark,
            fg=self.neon_pink
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Now create StringVar after root window exists
        self.selected_resolution = tk.StringVar(value="1080p")
        
        # Resolution dropdown styling
        self.resolution_menu = tk.OptionMenu(
            frame, 
            self.selected_resolution, 
            *self.resolutions.keys()
        )
        self.resolution_menu.config(
            width=15,
            font=("Consolas", 12, "bold"),
            bg=self.bg_darker,
            fg=self.neon_blue,
            activebackground=self.neon_purple,
            activeforeground=self.text_color,
            highlightthickness=2,
            highlightbackground=self.neon_blue,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.resolution_menu["menu"].config(
            bg=self.bg_darker,
            fg=self.neon_blue,
            activebackground=self.neon_purple,
            activeforeground=self.text_color,
            font=("Consolas", 10)
        )
        self.resolution_menu.pack(pady=20)
        
        # Create buttons with neon styling
        self.start_button = tk.Button(
            frame, 
            text="⚡ START RECORDING ⚡",
            command=self.start_recording_thread,
            bg=self.bg_darker,
            fg=self.neon_blue,
            height=2,
            width=25,
            font=("Consolas", 12, "bold"),
            relief=tk.FLAT,
            activebackground=self.neon_blue,
            activeforeground=self.bg_dark,
            cursor="hand2",
            highlightthickness=2,
            highlightbackground=self.neon_blue,
        )
        self.start_button.pack(pady=20)
        
        self.stop_button = tk.Button(
            frame,
            text="⚠ STOP RECORDING ⚠",
            command=self.stop_recording,
            bg=self.bg_darker,
            fg=self.neon_pink,
            height=2,
            width=25,
            font=("Consolas", 12, "bold"),
            relief=tk.FLAT,
            activebackground=self.neon_pink,
            activeforeground=self.bg_dark,
            cursor="hand2",
            state=tk.DISABLED,
            highlightthickness=2,
            highlightbackground=self.neon_pink,
        )
        self.stop_button.pack(pady=20)
        
        # Status label with neon effect
        self.status_label = tk.Label(
            frame,
            text="// SYSTEM READY //",
            font=("Consolas", 10),
            bg=self.bg_dark,
            fg=self.neon_purple
        )
        self.status_label.pack(pady=(20, 0))
        
        # Add decorative elements
        decoration_top = tk.Label(
            frame,
            text="<<<<<<<<>>>>>>>>>>",
            font=("Consolas", 14),
            bg=self.bg_dark,
            fg=self.neon_pink
        )
        decoration_top.pack(side=tk.TOP, pady=(0, 20))
        
        decoration_bottom = tk.Label(
            frame,
            text="<<<<<<<<>>>>>>>>>>",
            font=("Consolas", 14),
            bg=self.bg_dark,
            fg=self.neon_pink
        )
        decoration_bottom.pack(side=tk.BOTTOM, pady=(20, 0))
        
        # Timer label with larger font
        self.timer_label = tk.Label(
            frame,
            text="00:00:00",
            font=("Consolas", 32, "bold"),  # Much larger font
            bg=self.bg_dark,
            fg=self.neon_blue
        )
        self.timer_label.pack(pady=25)  # More padding around timer
        
        # Initialize timer variables
        self.start_time = 0
        self.timer_running = False
        
    def generate_filename(self):
        # Generate unique filename based on timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Change extension based on codec
        return os.path.join(self.output_dir, f"recording_{timestamp}.avi")
        
    def start_recording_thread(self):
        # Disable start button and enable stop button
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Start recording in a separate thread
        self.record_thread = Thread(target=self.start_recording)
        self.record_thread.start()
        
    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            hours = elapsed_time // 3600
            minutes = (elapsed_time % 3600) // 60
            seconds = elapsed_time % 60
            time_string = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_string)
            self.root.after(1000, self.update_timer)  # Update every second
        
    def start_recording(self):
        filename = self.generate_filename()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        # Get selected resolution
        resolution = self.resolutions[self.selected_resolution.get()]
        fps = 15.0  # Set both capture and output FPS to 30 for consistency
        
        self.out = cv2.VideoWriter(
            filename,
            fourcc,
            fps,  # Use the same FPS for capture and output
            resolution,
            isColor=True
        )
        
        if not self.out.isOpened():
            print("Error: Could not open video writer")
            return
        
        self.recording = True
        print(f"Recording started at {resolution}. Output file: {filename}")
        
        # Start timer
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()
        
        # Update status label
        self.status_label.config(text="// RECORDING IN PROGRESS //", fg=self.neon_pink)
        
        try:
            frame_time = 1/fps  # Time per frame
            next_frame_time = time.time()
            
            while self.recording:
                current_time = time.time()
                if current_time < next_frame_time:
                    remaining_time = next_frame_time - current_time
                    if remaining_time > 0.001:
                        time.sleep(remaining_time)
                
                # Capture frame
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                if frame.shape[1] != resolution[0] or frame.shape[0] != resolution[1]:
                    frame = cv2.resize(
                        frame, 
                        resolution, 
                        interpolation=cv2.INTER_LINEAR
                    )
                
                # Write every frame to maintain correct duration
                self.out.write(frame)
                
                # Update next frame time
                next_frame_time += frame_time
                    
        except Exception as e:
            print(f"Error during recording: {str(e)}")
            self.stop_recording()
        
    def stop_recording(self):
        self.recording = False
        self.timer_running = False  # Stop timer
        self.timer_label.config(text="00:00:00")  # Reset timer display
        
        if hasattr(self, 'out'):
            self.out.release()
        print("Recording stopped")
        
        # Reset status label
        self.status_label.config(text="// SYSTEM READY //", fg=self.neon_purple)
        
        # Reset buttons
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    recorder = ScreenRecorder()
    recorder.run()