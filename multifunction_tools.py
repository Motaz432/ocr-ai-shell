# Multifunction Tools Version 2, Author: Marco Anian and Review by Nova Astra
#---------------------Doc--------------------------#
"""
📄 MultiOCR AI Tools – Version 2
Author: Marco Anian | Review & AI Support: Nova Astra

This module provides core functionality for image-based OCR, AI-powered image descriptions,
and summarization tools using Tesseract and Ollama-compatible models like Mistral and LLaVA.

Features:
- Webcam capture
- Web image downloader
- Tesseract OCR text extraction
- AI-powered image analysis and summarization
- Plain text export

Use this as a backend utility inside the GUI shell (ocr_shell_gui.py), or as a standalone helper in future projects.

Dependencies:
pip install ollama
pip install opencv-python
pip install pytesseract
"""
#------------------Imports-------------------------#
import ollama
from tkinter import filedialog, messagebox
import requests # for loading Image from web
from PIL import Image, ImageTk
import pytesseract # Need be also installed on windows
import cv2
#----------------Constants-------------------------#
IMAGE_PATH = "assets/image/"


#--------------Class-------------------------------#
class MultiOCRAiTools:
    def __init__(self,master=None):
        # Init Section / if come
        self.master = master
# ---------------Method / Function------------------------#

#---------------------Get Image From multiple Sources-----#
    def read_image_from_web(self, image_link, image_name):
        """Download Image from web and save it in Asset folder """
        url = image_link # Image link will be past in the Gui to here
        image_name_by_user = image_name
        try:
            response = requests.get(url)
            with open(f"{IMAGE_PATH}{image_name_by_user}.jpg", "wb") as file:
                data = file.write(response.content)
                print(f"Data Downloaded to: {IMAGE_PATH}")
                return data
        except Exception as e:
            messagebox.showerror("Download Error", f"{e}\nCheck the image link.")


    def extract_text_from_image(self, file_path,lang):
            """Using Tesseract OCR to extract text from Image
            lang = deu, eng, jpn, esp, chi_sim, chi_tra, fas """
            # Very Important for Tesseract, if not inside, will get Error (DO NOT CHANGE)
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            image = Image.open(file_path) # To open image path
            text = pytesseract.image_to_string(image, lang=lang) # Main Process
            return text

    def live_web_cam_image(self):
        """Using CV2 for live mode, capture Image and save it"""
        cap = cv2.VideoCapture(0) # init / open camera / 0 = main camera
        # Error handling
        if not cap.isOpened():
            print("❌ Cannot open camera.")
            return False  # Indicate failure
        print("🎥 Camera initialized. Press 's' to analyze frame or 'q' to exit.")
        messagebox.showinfo(message="🎥 Camera initialized.\n Press 's' to analyze frame\n or 'q' to exit.")
        n = 0
        ext = "jpg" # image format
        while True:
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Can't receive frame (stream ended?). Exiting...")
                break

                # Display live video feed
            cv2.imshow('Live Feed', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break  # Quit program
            elif key == ord('s'):
                print("\n📸 Capturing and processing image with AI... 🧠💡")
                cv2.imwrite(f"{IMAGE_PATH}image_{n}.{ext}", frame)

                n += 1 # for other image name will be +1
                print("saved!!!")

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Camera closed.")
        return True
#-------------------Ai Section-------------------------------------#
    def image_to_text_description(self,image_path):
        """This is for Scrap class --> Scrape Image func"""
        response = ollama.chat(
            model="llava:13b",
            messages=[
                {
                    "role": "user",
                    "content": "Describe this image in detail and extract any readable data.",
                    "images": [image_path]
                }
            ]
        )
        description = response['message']['content']
        text_format = f"Image analyze: {description}"
        return {"role": "assistant", "content": text_format}  # ✅ return ready-to-use format

    def summarize_text(self, text_description):
        """This is for Scrap class --> Summarize func"""
        system_msg = (
            "You are an AI summarizer. Read the following text carefully and summarize it using the same language as the input. "
            "Do not translate. If the text is in English, the summary must also be in English, If the text is in German, the summary must also be in German. "
            "Focus on key points and important content only. Use bullet points or short paragraphs."
        )

        response = ollama.chat(
            model="mistral:latest",  # or "gemma3:12b" for softer tone
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": text_description}
            ]
        )

        return response["message"]["content"]

    def save_text(self, data):
        """This function is to write AI respond to text"""
        path_file = filedialog.asksaveasfilename(defaultextension="*.txt")
        try:
            with open(path_file,"w", encoding="utf-8") as f:
                f.write(data)
                messagebox.showinfo(message=f"file saved{path_file}")
        except Exception as e:
            messagebox.showinfo(message=f"{e},uppsss!!\nsomething went wrong :/")




# Test Run
if __name__=="__main__":
    tools = MultiOCRAiTools()
    #tools.live_web_cam_image()
    path = filedialog.askopenfilename()
    desc = tools.extract_text_from_image(path, "deu")
    summa_res = tools.summarize_text(desc)
    print(summa_res)




