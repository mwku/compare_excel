import customtkinter as ctk
import tkinter as tk
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

class App(ctk.CTk):
    def __init__(self,read_file:Callable,compare_same:Callable,to_excel:Callable):
        super().__init__()
        self.read_file = read_file
        self.compare_same = compare_same
        self.to_excel = to_excel
        # self.set_default_color_theme("dark-blue")

        self.title("Compare Excel Files")
        self.geometry("600x400")
        self.path_a = ""
        self.path_b = ""
        self.alert=None
        self.resizable(False, False)
        # self.minsize(480, 320)
        # self.state('zoomed')
        self.init_ui()

    def _clear_page(self):
        for name in (
            "container",
            "submit_button",
            "function_choice_container",
            "compare_same_button",
            "compare_different_button",
            "back_button",
            "save_button",
            "back_to_function_button",
            "is_restart_button",
        ):
            widget = getattr(self, name, None)
            if widget is not None:
                try:
                    widget.destroy()
                except tk.TclError:
                    pass
                setattr(self, name, None)

    def init_ui(self):
        self._clear_page()
        self.container = ctk.CTkFrame(self)
        self.container.configure(height=190,width=600,fg_color="transparent")
        self.container.place(relx=0.5, rely=0.4, anchor="center")

        self.button_container = ctk.CTkFrame(self.container)
        self.button_container.configure(height=90,width=400,fg_color="transparent")
        self.button_container.pack(pady=0,padx=0,side="top",anchor="center")

        self.file_a_container = ctk.CTkFrame(self.button_container, fg_color="transparent")
        self.file_a_container.pack(padx=20, pady=0, side="left", anchor="n")
        self.upload_button_a = ctk.CTkButton(self.file_a_container, text="上傳檔案A\n(使用配對編號時『沒有編號』的檔案)", command=self.upload_file_a)
        self.upload_button_a.configure(height=90,width=180)
        if self.path_a:
            self.upload_button_a.configure(fg_color="#61bd69",hover_color="#336c38")
        self.upload_button_a.pack(pady=0, padx=0, side="top", anchor="center")
        self.path_a_label = ctk.CTkLabel(
            self.file_a_container,
            text=self.path_a if self.path_a else "No file selected for File A",
            width=180,
            wraplength=180,
            justify="center",
        )
        self.path_a_label.pack(pady=5, padx=0, side="top", anchor="center")

        self.file_b_container = ctk.CTkFrame(self.button_container, fg_color="transparent")
        self.file_b_container.pack(padx=20, pady=0, side="left", anchor="n")
        self.upload_button_b = ctk.CTkButton(self.file_b_container, text="上傳檔案B\n(使用配對編號時『有編號』的檔案)", command=self.upload_file_b)
        self.upload_button_b.configure(height=90,width=180)
        if self.path_b:
            self.upload_button_b.configure(fg_color="#61bd69",hover_color="#336c38")
        self.upload_button_b.pack(pady=0, padx=0, side="top", anchor="center")
        self.path_b_label = ctk.CTkLabel(
            self.file_b_container,
            text=self.path_b if self.path_b else "No file selected for File B",
            width=180,
            wraplength=180,
            justify="center",
        )
        self.path_b_label.pack(pady=5, padx=0, side="top", anchor="center")

        self.submit_button = ctk.CTkButton(self, text="下一步", command=self.submit, state="disabled")
        if self.path_a and self.path_b:
            self.submit_button.configure(state="normal")
        self.submit_button.configure(height=50,width=400)
        self.submit_button.place(relx=0.5, rely=0.75, anchor="center")

    def submit(self):
        self._clear_page()

        self.function_choice_container = ctk.CTkFrame(self)
        self.function_choice_container.configure(width=600,height=90,fg_color="transparent")
        self.function_choice_container.place(relx=0.5, rely=0.4, anchor="center")

        self.compare_same_button = ctk.CTkButton(self.function_choice_container, text="配對零件編號", command=self.compare_same_,fg_color="#61bd69",hover_color="#336c38")
        self.compare_same_button.configure(height=90,width=180)
        self.compare_same_button.pack(pady=0, padx=25, side="left", anchor="center")

        self.compare_different_button = ctk.CTkButton(self.function_choice_container, text="配對差異", command=self.compare_different)
        self.compare_different_button.configure(height=90,width=180)
        self.compare_different_button.pack(pady=0, padx=25, side="left", anchor="center")

        self.back_button = ctk.CTkButton(self, text="上一頁", command=self.back)
        self.back_button.configure(height=50,width=180)
        self.back_button.place(relx=0.5, rely=0.75, anchor="center")

    def back(self):
        self.init_ui()

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

    def compare_same_(self):
        try:
            self.result=self.compare_same(self.read_file(self.path_a), self.read_file(self.path_b))
            
            self.function_choice_container.destroy()
            self.back_button.destroy()

            self.save_button = ctk.CTkButton(self, text="儲存為Excel", command=self.save_excel,fg_color="#61bd69",hover_color="#336c38")
            self.save_button.configure(height=50,width=400)
            self.save_button.place(relx=0.5, rely=0.3, anchor="center")

            self.back_to_function_button = ctk.CTkButton(self, text="上一頁", command=self.submit)
            self.back_to_function_button.configure(height=50,width=400)
            self.back_to_function_button.place(relx=0.5, rely=0.6, anchor="center")

            self.update()

            # self.save_excel()
        except Exception as e:
            self.alert = Alert(self, f"Failed to compare files: {e}")
            self.alert.focus()
            # print(f"Failed to compare files: {e}")

    def compare_different(self):
        pass

    def restart(self):
        try:
            self.is_restart_button.destroy()
        except Exception as e:
            pass
        try:
            self.save_button.destroy()
        except Exception as e:
            pass
        try:
            self.back_to_function_button.destroy()
        except Exception as e:
            pass

        self.path_a = ""
        self.path_b = ""
        self.init_ui()
        return

    def save_excel(self):
        try:
            self.save_button.configure(state="disabled")
            self.back_to_function_button.configure(state="disabled")
            # self.back_to_function_button.place(relx=0.5, rely=0.75, anchor="center")
            path = ctk.filedialog.asksaveasfilename(
                defaultextension=".xlsx", 
                filetypes=[("Excel files", "*.xlsx"), 
                        ("All files", "*.*")],
                title="Save Compare Result",
                initialdir="/".join(self.path_b.split("/")[0:-1]),
                initialfile="result.xlsx")
            if not path:
                self.save_button.configure(state="normal")
                self.back_to_function_button.configure(state="normal")
                return
            self.to_excel(self.result,path)
            self.save_button.configure(state="normal")
            self.back_to_function_button.configure(state="normal")
            self.is_restart_button = ctk.CTkButton(self, text="重新開始", command=self.restart,fg_color="#bd6161",hover_color="#6c3333")
            self.is_restart_button.configure(height=50,width=400)
            self.is_restart_button.place(relx=0.5, rely=0.8, anchor="center")
            return 
        except Exception as e:
            self.alert = Alert(self, f"Failed to save file: {e}")
            self.alert.focus()
