import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np

class ImageEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Image Enhancer')
        self.root.geometry('800x600')

        # Variabile
        self.cv_img = None
        self.tk_img = None

        # UI
        self.create_widgets()

    def create_widgets(self):
        # Canvas pentru imagine
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='gray')
        self.canvas.pack(pady=10)

        # Butoane
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text='Load Image', command=self.load_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text='Save Image', command=self.save_image).grid(row=0, column=1, padx=5)
        
        # Combo filtre
        self.filter_var = tk.StringVar(value='Original')
        filters = ['Original', 'Grayscale', 'Blur', 'Sharpen', 'Edge Detection', 'Face Detection']
        ttk.Combobox(btn_frame, textvariable=self.filter_var, values=filters, state='readonly').grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text='Apply Filter', command=self.apply_filter).grid(row=0, column=3, padx=5)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[('Image Files', '*.jpg *.png *.jpeg *.bmp')])
        if not path:
            return
        self.cv_img = cv2.imread(path)
        self.display_image(self.cv_img)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((600, 400))
        self.tk_img = ImageTk.PhotoImage(img_pil)
        self.canvas.create_image(300, 200, image=self.tk_img)

    def save_image(self):
        if self.cv_img is None:
            messagebox.showwarning('Warning', 'No image loaded')
            return
        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg')])
        if not path:
            return
        cv2.imwrite(path, self.cv_img)
        messagebox.showinfo('Saved', f'Image saved to {path}')

    def apply_filter(self):
        if self.cv_img is None:
            messagebox.showwarning('Warning', 'No image loaded')
            return
        filter_name = self.filter_var.get()
        img = self.cv_img.copy()

        if filter_name == 'Grayscale':
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        elif filter_name == 'Blur':
            img = cv2.GaussianBlur(img, (7,7), 0)
        elif filter_name == 'Sharpen':
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            img = cv2.filter2D(img, -1, kernel)
        elif filter_name == 'Edge Detection':
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        elif filter_name == 'Face Detection':
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

        self.display_image(img)
        self.cv_img = img  # update imagine curent

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
