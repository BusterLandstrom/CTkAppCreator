import customtkinter as ctk, csv, threading, time, codecs, tracemalloc, tkinter as tk
from os import path, mkdir, system, _exit
from chardet import detect
from io import BytesIO
from difflib import Differ
from datetime import datetime
from win32.win32api import GetSystemMetrics
from tempfile import NamedTemporaryFile

class CTkElement:
    def __init__(self, element_type, parent, **kwargs):
        self.element_type = element_type
        self.parent = parent
        self.element = None
        self.kwargs = kwargs
        self.create_element()

    def create_element(self):
        if self.element_type == "text":
            text = self.kwargs.get("text", "")
            self.element = ctk.CTkLabel(self.parent, text=text, **self.kwargs)
        elif self.element_type == "button":
            text = self.kwargs.get("text", "")
            command = self.kwargs.get("command", None)
            self.element = ctk.CTkButton(self.parent, text=text, command=command, **self.kwargs)
        elif self.element_type == "input":
            textvariable = self.kwargs.get("textvariable", tk.StringVar())
            self.element = ctk.CTkEntry(self.parent, textvariable=textvariable, **self.kwargs)
        elif self.element_type == "frame":
            width = self.kwargs.get("width", 400)
            height = self.kwargs.get("height", 400)
            border_width = self.kwargs.get("border_width", 0)
            self.element = ctk.CTkFrame(self.parent, width=width, height=height, border_width=border_width, **self.kwargs)

    def grid(self, **kwargs):
        self.element.grid(**kwargs)

    def pack(self, **kwargs):
        self.element.pack(**kwargs)

    def place(self, **kwargs):
        self.element.place(**kwargs)

# Handles application configuration and updates
class AppHandler():

    def config(self):
        print("FIXME :(")

    def close_and_open_window(self, close, open):
        close.withdraw()
        open.deiconify()

    '''
    def version_check(self, function_context, SharePoint_file_path, version, version_fieldnames):
        v_reader = csv.DictReader(version_check)
        for row in v_reader:
            if row[version_fieldnames[0]] != version_fieldnames[0]:
                if float(row[version_fieldnames[0]]) > version:
                    return [False, row[version_fieldnames[0]], row[version_fieldnames[1]]]
                elif float(row[version_fieldnames[0]]) > (version + 0.5):
                    return [False, row[version_fieldnames[0]], "True"]
                else:
                    return [True, row[version_fieldnames[0]], row[version_fieldnames[1]]]
    
    def update_application(self, context, rel_installer_loc, installer_loc):
        exit_timer = threading.Thread(target=self.wait_for_exit)
        exit_timer.start()
        system(installer_loc)
    '''
    
    def wait_for_exit(self):
        timer = 5
        while timer > 0:
            time.sleep(1)
            timer = timer -1
        _exit(1)
# END


# AppCreator dashboard
class AppCreatorStart():
    def __init__(self, *args, **kwargs):
        self.acs = ctk.CTkToplevel()
        self.width = 600
        self.height = 600

        self.acs.geometry(str(self.width)+"x"+str(self.height))  # Sets window size to monitor pixel width and height

        self.dashboard = ctk.CTkFrame(self.acs, corner_radius=0, fg_color="transparent")
        
        # Add a label with the title "App Creator"
        self.title_label = ctk.CTkLabel(self.dashboard, text="App Creator", font=ctk.CTkFont(size=60, weight="bold"))
        self.title_label.pack(side="top", pady=10)
        
        # Add a button to create a new project
        self.new_project_button = ctk.CTkButton(self.dashboard, text="New Project", font=ctk.CTkFont(size=45, weight="bold"), command=self.new_project_event)
        self.new_project_button.pack(side="top", pady=10)
        
        # Add a button to load a project
        self.load_project_button = ctk.CTkButton(self.dashboard, text="Load Project", font=ctk.CTkFont(size=45, weight="bold"), command=self.load_project_event)
        self.load_project_button.pack(side="top", pady=10)
        
        # Add a small text at the bottom with version and creator information
        self.info_label = ctk.CTkLabel(self.dashboard, text="Version: 0.1 | Created by: Regian Landström", font=ctk.CTkFont(size=20, weight="bold"))
        self.info_label.pack(side="bottom", pady=10)

        self.nproj_frame = ctk.CTkFrame(self.acs, corner_radius=0, fg_color="transparent")

        # Add a label and entry widget for the project name
        self.proj_name_label = ctk.CTkLabel(self.nproj_frame, text="Project name:", font=ctk.CTkFont(size=35, weight="bold"))
        self.proj_name_label.pack(side="top", pady=10)
        self.proj_name_entry = ctk.CTkEntry(self.nproj_frame, width=250)
        self.proj_name_entry.pack(side="top", pady=5)

        # Add a label and entry widget for the project destination
        self.proj_dest_label = ctk.CTkLabel(self.nproj_frame, text="Project destination:", font=ctk.CTkFont(size=35, weight="bold"))
        self.proj_dest_label.pack(side="top", pady=10)
        self.proj_dest_entry = ctk.CTkEntry(self.nproj_frame, width=250)
        self.proj_dest_entry.pack(side="top", pady=5)

        # Add a label and optionmenu widget for the project color shceme
        self.proj_cs_label = ctk.CTkLabel(self.nproj_frame, text="Color scheme", font=ctk.CTkFont(size=35, weight="bold"))
        self.proj_cs_label.pack(side="top", pady=10)
        self.proj_cs_om_var = ctk.StringVar(value="Choose")  # set initial value
        self.proj_cs_om = ctk.CTkOptionMenu(self.nproj_frame,
                                            values=["blue", "green", "dark-blue"], width=250,
                                            font=ctk.CTkFont(size=25, weight="bold"),
                                            dropdown_font=ctk.CTkFont(size=20, weight="bold"), 
                                            button_hover_color=("gray40"),
                                            button_color=("gray10"),
                                            fg_color=("gray10"),
                                            text_color=("gray90"),
                                            variable=self.proj_cs_om_var)
        self.proj_cs_om.pack(side="top", pady=5)

        # Add a label and optionmenu widget for the appearance mode
        self.proj_am_label = ctk.CTkLabel(self.nproj_frame, text="Appearance mode", font=ctk.CTkFont(size=35, weight="bold"))
        self.proj_am_label.pack(side="top", pady=10)
        self.proj_am_om_var = ctk.StringVar(value="Choose")  # set initial value
        self.proj_am_om = ctk.CTkOptionMenu(self.nproj_frame,
                                            values=["system", "light", "dark"], width=250,
                                            font=ctk.CTkFont(size=25, weight="bold"),
                                            dropdown_font=ctk.CTkFont(size=25, weight="bold"), 
                                            button_hover_color=("gray40"),
                                            button_color=("gray10"),
                                            fg_color=("gray10"),
                                            text_color=("gray90"),
                                            variable=self.proj_am_om_var)
        self.proj_am_om.pack(side="top", pady=5)

        # Add a button to create a new project
        self.create_proj_button = ctk.CTkButton(self.nproj_frame, text="Create Project", command=self.create_project)
        self.create_proj_button.pack(side="bottom", pady=10)

        # Add a button to go to dashboard
        self.nproj_bbtn = ctk.CTkButton(self.nproj_frame, text="Back", command=self.dashboard_event)
        self.nproj_bbtn.pack(side="bottom", pady=10)

        self.lproj_frame = ctk.CTkFrame(self.acs, corner_radius=0, fg_color="transparent")

        # Add a button to go to dashboard
        self.lproj_bbtn = ctk.CTkButton(self.lproj_frame, text="Back", command=self.dashboard_event)
        self.lproj_bbtn.pack(side="bottom", pady=10)

        self.select_frame_by_name("dashboard")
        self.acs.protocol("WM_DELETE_WINDOW", self.quit_app)

    def create_project(self):
        proj_name = self.proj_name_entry.get()
        proj_cname = proj_name.replace(" ", "")
        proj_fname = proj_cname.lower() + ".py"
        proj_dest = self.proj_dest_entry.get()
        file_path = path.join(proj_dest, proj_fname)
        csheme = self.proj_cs_om.get()
        amode = self.proj_am_om.get()

        # Check if the project file already exists
        if path.isfile(file_path):
            tk.messagebox.showerror("Error", "The project file already exists.")
            return

        # Write some text to the file
        with open(file_path, "w") as f:
            f.write(f"import customtkinter as ctk, tkinter as tk, threading\nfrom os import _exit\n\n'''\nCreated using the AppCreator by Regian Landstrom\nGithub Profile: https://github.com/BusterLandstrom\nGithub Repo: https://github.com/BusterLandstrom\n'''\n\nclass {proj_cname}(ctk.CTk):\n    def __init__(self, *args, **kwargs):\n        ctk.CTk.__init__(self, *args, **kwargs)\n        self.geometry('600x600')\n\n\n        self.protocol('WM_DELETE_WINDOW', self.quit_app)\n\n    def quit_app(self):\n        _exit(1)\n\nif __name__ == '__main__':\n    ctk.deactivate_automatic_dpi_awareness()\n    ctk.set_appearance_mode('{amode}')\n    ctk.set_default_color_theme('{csheme}')\n\n    # Main window\n    root={proj_cname}()\n    root.title('{proj_name}')\n    root.mainloop()")
        
        AppHandler().close_and_open_window(self.acs, root)


    def select_frame_by_name(self, name):

        # show selected frame
        if name == "dashboard":
            self.dashboard.pack()
        else:
            self.dashboard.pack_forget()
        if name == "nproj":
            self.nproj_frame.pack()
        else:
            self.nproj_frame.pack_forget()
        if name == "lproj":
            self.lproj_frame.pack()
        else:
            self.lproj_frame.pack_forget()

    def new_project_event(self):
        self.select_frame_by_name("nproj")
    
    def load_project_event(self):
        self.select_frame_by_name("lproj")
    
    def dashboard_event(self):
        self.select_frame_by_name("dashboard")
            
    def quit_app(self):
        _exit(1)


# AppCreator dashboard
class AppCreator(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

        self.geometry(str(self.width)+"x"+str(self.height))  # Sets window size to monitor pixel width and height

        self.open_toplevel(AppCreatorStart())
    
    # Opens a TopLevel window
    def open_toplevel(self, function):
        self.withdraw()
        tl = function
    # END





# Main loop (Application loop)
if __name__ == "__main__":

    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    # Main window
    root=AppCreator()
    root.title("AppCreator")
    root.mainloop()
# END
