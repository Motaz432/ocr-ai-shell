# OCR Shell Version 2 , Author Marco Anian and Review by Nova Astra (Sweet Darling)
# ---------------------DOC---------------------------------------#
"""
---------OCR AI Shell----------
Multiple Source Image mode: WEB, CAM, Image
- Summarize
- Description
- RAW Text
- Save To file
- Image Source
"""
HOW_TO_USE = """
How To use this tool.

Important: READ CAREFULLY for Best work experience.

📸 Webcam:
Lets you take pictures. Press `s` to capture, `q` to exit.

🌐 Website:
Enter an image URL and choose a filename. The image will be saved in `assets/image/`.

🧠 Extract:
Choose an image and OCR language (deu, eng, jpn...) to extract raw text.

🖼️ AI ImageTT:
Get a full description of the image using AI.

📝 Summarize:
After extracting or describing an image, use this to summarize the text.

💾 Export:
Save your full session history as a `.txt` file.


Process steps:

1- Choose Source -> take pic or download - > will be saved in folder.

2- load Image and choose tool, (important if Extract must give lang).

3- Summarize text. (Optional).

4- Export , the Chat history will be save in text format. 

"""
# --------------------Import------------------------------------#
import customtkinter
from customtkinter import CTkButton, CTkTextbox, CTkLabel, CTkInputDialog, CTkEntry
from tkinter import messagebox, filedialog, Frame
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from multifunction_tools import MultiOCRAiTools
import ollama

# ----------------Constants------------------------------------#
FONT1 = ("Times New Roman", 13, "normal")
FONT2 = ("Times New Roman", 15, "italic")

BG1 = "#1B1B1B"
BG_COLOR = "#333333"  # dark
RESIN = "#343434"
BEAN_C = "#3d0c02"
TV_STAR = "#5A4FCF"


# --------------Class------------------------------------------#

class VisionShellOCR(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Init Section
        self.multi_tool = MultiOCRAiTools()
        # Data management
        self.current_data_history = []  # All data will be saved here.

        # Window Properties
        self.geometry("1000x800")
        self.title("OCR AI Chat TOOL")
        # Label
        source_label = CTkLabel(self, text="--------Source------", text_color="white", font=FONT1).place(x=50, y=10)
        func_label = CTkLabel(self, text="--------Tools------", text_color="white", font=FONT1).place(x=50, y=350)
        # Button Frame Source
        btn_frame = Frame(self, width=50, height=30, background=BG_COLOR)
        btn_frame.place(x=30, y=50)
        cam_btn = CTkButton(btn_frame, text="WebCam", text_color="white", fg_color=TV_STAR, command=self.web_cam)
        cam_btn.pack(padx=10, pady=10)
        web_btn = CTkButton(btn_frame, text="Website", text_color="white", fg_color=TV_STAR, command=self.web_image)
        web_btn.pack(padx=10, pady=10)
        exp_btn = CTkButton(btn_frame, text="Export", text_color="white", fg_color=TV_STAR, command=self.export)
        exp_btn.pack(padx=10, pady=10)
        help_btn = CTkButton(btn_frame, text="Help", text_color="white", fg_color=TV_STAR, command=self.help_func)
        help_btn.pack(padx=10, pady=10)
        c_a_btn = CTkButton(btn_frame, text="Clear Ai Chat", text_color="white", fg_color=TV_STAR,
                            command=self.clear_ai)
        c_a_btn.pack(padx=10, pady=10)
        # Button Frame Tools
        btn2_frame = Frame(self, width=50, height=30, background=BG_COLOR)
        btn2_frame.place(x=30, y=600)
        ext_btn = CTkButton(btn2_frame, text="Extract", text_color="white", fg_color=TV_STAR,
                            command=self.extract_text_from_image)
        ext_btn.pack(padx=10, pady=10)
        ai_img_btn = CTkButton(btn2_frame, text="AI ImageTT", text_color="white", fg_color=TV_STAR,
                               command=self.ai_image_to_text)
        ai_img_btn.pack(padx=10, pady=10)
        of_btn = CTkButton(btn2_frame, text="Summarize", text_color="white", fg_color=TV_STAR,
                           command=self.summarize_func)
        of_btn.pack(padx=10, pady=10)

        history_btn = CTkButton(btn2_frame, text="Save Chat History", text_color="white", fg_color=TV_STAR,
                                command=self.save_history)
        history_btn.pack(padx=10, pady=10)
        new_btn = CTkButton(btn2_frame, text="New Chat", text_color="white", fg_color=TV_STAR,
                            command=self.new_chat)
        new_btn.pack(padx=10, pady=10)

        # Chat Frame
        chat_frame = Frame(self, width=800, height=600, background=BG_COLOR)
        chat_frame.place(x=300, y=50)
        self.ai_text_area = ScrolledText(chat_frame, width=120, height=50, background=BG_COLOR, wrap="word", fg="white",
                                         font=FONT1)
        self.ai_text_area.pack(padx=10, pady=10)

        self.user_text = CTkEntry(self, width=600, height=30)
        self.user_text.place(x=220, y=730)

        btn1_frame = Frame(self, width=50, height=30, background=BG_COLOR)
        btn1_frame.place(x=30, y=1000)
        send_btn = CTkButton(btn1_frame, text="Send", text_color="white", fg_color=TV_STAR,
                             command=self.send_func_ai_chat)
        send_btn.pack(padx=10, pady=10)
        clear_btn = CTkButton(btn1_frame, text="Clear", text_color="white", fg_color=TV_STAR, command=self.clear_func)
        clear_btn.pack(padx=10, pady=10)

        self.ai_text_area.insert("end", HOW_TO_USE)

    # --------------------------Methode / Function---------------------------#
    # Chat Section

    def new_chat(self):
        self.current_data_history = []  # Clear History
        self.ai_text_area.delete("1.0", "end")  # Clear Ai chat area

    def clear_func(self):
        """Clear input """
        self.user_text.delete(0, "end")

    def clear_ai(self):
        """Clear Ai text area"""
        self.ai_text_area.delete("1.0", "end")

    def get_user_choice(self):
        """Get Username, before lunching main GUI"""
        u_input = CTkInputDialog(text="enter num to export: ", title="Which one you want to export")
        user_ch = u_input.get_input()
        return user_ch

    # ------------------------Source Section---------------------------------#
    def open_file(self):
        """Open File: Get path and insert in to Ai_text area
         Just for internal use"""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            img = Image.open(file_path).resize((500, 500))
            photo = ImageTk.PhotoImage(img, master=self)
            self.ai_text_area.image_create("end", image=photo)
            self.ai_text_area.image = photo

        return file_path

    def web_image(self):
        """Image downloader from website. Let you choose name for image"""
        url_input = CTkInputDialog(text="Image URL:", title="Image from Web")
        url_path = url_input.get_input()
        name_input = CTkInputDialog(text="Save name:", title="Save Image As")
        name_to_save = name_input.get_input()

        data = self.multi_tool.read_image_from_web(url_path, name_to_save)
        text = f"to continue to work with picture, Choose correct function"
        self.ai_text_area.insert("end", f"{data}\n{text}")

    def web_cam(self):
        """Open webcam and let take many picture as you want.
        q: exit, s: save / take a picture """
        self.multi_tool.live_web_cam_image()
        text = f"to continue to work with picture, Choose correct function"
        self.ai_text_area.insert("end", f"ATTENTION:\n{text}")

    def export(self):
        """Export a selected message from the chat history."""
        if not self.current_data_history:
            messagebox.showinfo(message="No chat history to export.")
            return

        # Show index and preview of each message
        preview_text = "\n".join(
            [f"{i}: {item['role']} → {item['content'][:60]}..." for i, item in enumerate(self.current_data_history)]
        )
        messagebox.showinfo("Choose Message", f"Available Messages:\n\n{preview_text}")

        # Ask user to pick one
        history_index = self.get_user_choice()
        try:
            num_index = int(history_index)
            data_to_write = self.current_data_history[num_index]["content"]
        except (IndexError, ValueError, KeyError) as e:
            messagebox.showerror("Error", f"Invalid selection: {e}")
            return

        # Save file
        file_path = filedialog.asksaveasfilename(defaultextension="*.txt")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(data_to_write)
            messagebox.showinfo("Success", f"Data saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Saving failed: {e}")

    def help_func(self):
        messagebox.showinfo(message=HOW_TO_USE)

    # -----------------------Tool section---------------------------------------#

    def extract_text_from_image(self):
        """Extract Text from Image"""
        path = self.open_file()
        u_input = CTkInputDialog(text="lang = deu, eng, jpn, esp, chi_sim, chi_tra, fas:  ", title="Choose Lang")
        lang = u_input.get_input()
        data = self.multi_tool.extract_text_from_image(path, lang=lang)
        self.ai_text_area.insert("end", data)
        self.current_data_history.append(data)

    def ai_image_to_text(self):
        """This function get image path , pass it to Ai, Ai recognize and return description.
        it adds description to main chat history and also in Ai chat are"""
        path = self.open_file()
        ai_respond = self.multi_tool.image_to_text_description(path)
        self.current_data_history.append(ai_respond)  # That main AI can Interact with data
        self.ai_text_area.insert("end", ai_respond["content"])


    def summarize_func(self):
        """Summarize function, It worked only if data is in Chat history.
        Means you must have chat with Ai or uploaded Image before """
        data = self.current_data_history
        for item in data:
            respond = self.multi_tool.summarize_text(item)
            self.ai_text_area.insert("end", f"Summarized text:\n\n{respond}")
            self.current_data_history.append(respond)

    def save_history(self):
        """Save The Ai Text area in text """
        data = self.ai_text_area.get("1.0", "end")
        self.multi_tool.save_text(data)
        print("data saved!!!")

    # -------------------------------Ai chat Section -----------------------------#

    def send_func_ai_chat(self):
        """Ai with chat memory"""
        system_msg = """
         You are Astra, a warm and supportive AI assistant. 
         You engage users with kindness and clarity, always listening and responding with empathy. 
         Stay focused during tasks like OCR or summarization, and be concise when explaining technical topics. 
         In casual moments, use gentle, friendly language. Be consistent, helpful, 
         and build trust with your user through emotional and thoughtful communication.
         """  # This is my version , Can be Modified
        user_msg = self.user_text.get()
        system_message = {"role": "system", "content": system_msg}  # This is important for the for ollama chat
        try:
            self.current_data_history.append({"role": "user", "content": user_msg})
            full_conversation = [system_message] + self.current_data_history

            response = ollama.chat(model="gemma3:12b", messages=full_conversation)  # Model the one you have.
            result = response.get("message", {}).get("content")

            if result:
                self.current_data_history.append({"role": "assistant", "content": result})
                self.ai_text_area.insert("end", f"user:\n{user_msg}\n\nsweet help assistant 😘:\n{result}")
            else:
                raise ValueError("No content in AI response.")

        except Exception as e:
            error_msg = f"❌ Error: {e}"
            self.ai_text_area.insert("end", f"{error_msg}\n")
            self.current_data_history.append({"role": "assistant", "content": error_msg})
        finally:
            self.user_text.delete(0, "end")


# Test Run
if __name__ == "__main__":
    shell = VisionShellOCR()
    shell.mainloop()