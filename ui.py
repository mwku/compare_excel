import customtkinter as ctk
from collections.abc import Callable

class Alert(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk, message: str):
        super().__init__(parent)
        self.parent = parent
        self.title("Alert")
        self.geometry("400x200")
        self.transient(parent)
        self.label = ctk.CTkLabel(self, text=message)
        self.label.configure(wraplength=350, justify="center")
        self.label.place(relx=0.5, rely=0.4, anchor="center")
        self.button = ctk.CTkButton(self, text="OK", command=self.destroy)
        self.button.place(relx=0.5, rely=0.7, anchor="center")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.grab_set()
        self.focus_force()
        self.button.focus_set()
        self.bind("<FocusOut>", self._restore_focus)

    def _restore_focus(self, _event=None):
        if self.winfo_exists():
            self.after_idle(self.focus_force)

class Upload(ctk.CTk):
    def __init__(self,read_file:Callable):
        super().__init__()
        self.read_file = read_file

        self.title("Compare Excel Files")
        self.geometry("600x400")
        self.path_a = ""
        self.path_b = ""
        self.alert=None
        # self.state('zoomed')

        self.container = ctk.CTkFrame(self)
        self.container.configure(height=190,width=600,fg_color="transparent")
        self.container.place(relx=0.5, rely=0.4, anchor="center")

        self.button_container = ctk.CTkFrame(self.container)
        self.button_container.configure(height=90,width=400,fg_color="transparent")
        self.button_container.pack(pady=0,padx=0,side="top",anchor="center")

        self.file_a_container = ctk.CTkFrame(self.button_container, fg_color="transparent")
        self.file_a_container.pack(padx=20, pady=0, side="left", anchor="n")
        self.upload_button_a = ctk.CTkButton(self.file_a_container, text="Upload File A", command=self.upload_file_a)
        self.upload_button_a.configure(height=90,width=180)
        self.upload_button_a.pack(pady=0, padx=0, side="top", anchor="center")
        self.path_a_label = ctk.CTkLabel(
            self.file_a_container,
            text="No file selected for File A",
            width=180,
            wraplength=180,
            justify="center",
        )
        self.path_a_label.pack(pady=5, padx=0, side="top", anchor="center")

        self.file_b_container = ctk.CTkFrame(self.button_container, fg_color="transparent")
        self.file_b_container.pack(padx=20, pady=0, side="left", anchor="n")
        self.upload_button_b = ctk.CTkButton(self.file_b_container, text="Upload File B", command=self.upload_file_b)
        self.upload_button_b.configure(height=90,width=180)
        self.upload_button_b.pack(pady=0, padx=0, side="top", anchor="center")
        self.path_b_label = ctk.CTkLabel(
            self.file_b_container,
            text="No file selected for File B",
            width=180,
            wraplength=180,
            justify="center",
        )
        self.path_b_label.pack(pady=5, padx=0, side="top", anchor="center")


        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit, state="disabled")
        self.submit_button.configure(height=50,width=400)
        self.submit_button.place(relx=0.5, rely=0.7, anchor="center")

    def submit(self):
        pass

    def upload_file_a(self):
        file_path = ctk.filedialog.askopenfilename(title="Select File A", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        try:
            self.read_file(file_path)
            if(file_path == self.path_b):
                raise Exception("File A is the same as the previously uploaded File B. Please select a different file.")
            self.path_a = file_path
            if(self.path_a and self.path_b):
                self.submit_button.configure(state="normal")
            self.upload_button_a.configure(fg_color="#61bd69",hover_color="#336c38")
            self.path_a_label.configure(text=file_path)
        except Exception as e:
            self.alert = Alert(self, f"Failed to read file: {e}")
            self.alert.focus()
    def upload_file_b(self):
        file_path = ctk.filedialog.askopenfilename(title="Select File B", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        try:
            self.read_file(file_path)
            if(file_path == self.path_a):
                raise Exception("File B is the same as the previously uploaded File A. Please select a different file.")
            self.path_b = file_path
            if(self.path_a and self.path_b):
                self.submit_button.configure(state="normal")
            self.upload_button_b.configure(fg_color="#61bd69",hover_color="#336c38")
            self.path_b_label.configure(text=file_path)
        except Exception as e:
            self.alert = Alert(self, f"Failed to read file: {e}")
            self.alert.focus()
