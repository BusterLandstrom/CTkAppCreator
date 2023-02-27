import customtkinter as ctk, csv, threading, time, codecs, tracemalloc, tkinter as tk
from os import path, mkdir, system, _exit
from chardet import detect
from tkinter import ttk
from webbrowser import open_new_tab
from io import BytesIO
from difflib import Differ
from datetime import datetime
from win32.win32api import GetSystemMetrics
from tempfile import NamedTemporaryFile


class CurrentProj:
    def __init__(self):
        self._proj_path = None

    @property
    def proj_path(self):
        return self._proj_path

    @proj_path.setter
    def proj_path(self, new_value):
        self._proj_path = new_value

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

    def convert_to_frame(self, filename):
        with open(filename, 'r') as f:
            code = f.read()

        # Replace "ctk.CTk()" with "ctk.CTkFrame()"
        code = code.replace("ctk.CTk()", "ctk.CTkFrame()")

        # Create a temporary root window to execute the code
        temp_root = ctk.CTk()
        temp_root.eval(code)

        # Get the frame from the temporary root window
        frame = temp_root.winfo_children()[0]

        # Destroy the temporary root window
        temp_root.destroy()

        return frame
    
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

        create = kwargs.get("create", "none")
        start = kwargs.get("start", "notfirst")

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
        self.info_label = ctk.CTkLabel(self.dashboard, text="Version: 0.1 | Created by: Buster Landstrom (alias)", font=ctk.CTkFont(size=20, weight="bold"))
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

        if create == "none":
            self.select_frame_by_name("dashboard")
        elif create == "new":
            self.select_frame_by_name("nproj")
        elif create == "load":
            self.select_frame_by_name("lproj")

        if start == "first":
            self.acs.protocol("WM_DELETE_WINDOW", self.quit_app)
        elif start == "notfirst":
            self.acs.protocol("WM_DELETE_WINDOW", self.acs.destroy)

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
            f.write(f"class {proj_cname}(ctk.CTk):\n    def __init__(self, *args, **kwargs):\n        ctk.CTk.__init__(self, *args, **kwargs)\n        self.geometry('600x600')\n\n\n        self.protocol('WM_DELETE_WINDOW', self.quit_app)\n\n    def quit_app(self):\n        _exit(1)")
        CurrentProj._proj_path = file_path
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

        # Create a top menu
        top_menu = tk.Menu(self)
        file_menu = tk.Menu(top_menu, tearoff=0)
        file_menu.add_command(label="New Project", command=self.new_proj)
        file_menu.add_command(label="Load Project", command=self.load_proj)
        top_menu.add_cascade(label="File", menu=file_menu)
        edit_menu = tk.Menu(top_menu, tearoff=0)
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        top_menu.add_cascade(label="Edit", menu=edit_menu)
        settings_menu = tk.Menu(top_menu, tearoff=0)
        settings_menu.add_command(label="Preferences", command=self.settings)
        top_menu.add_cascade(label="Settings", menu=settings_menu)
        help_menu = tk.Menu(top_menu, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.documentation)
        help_menu.add_command(label="About", command=self.about)
        top_menu.add_cascade(label="Help", menu=help_menu)
        self.config(menu=top_menu)

        # Attributes. e.g. set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="AppCreator",
                                                            compound="left", font=ctk.CTkFont(size=60, weight="bold"))
        self.navigation_frame_label.grid(row=1, column=0, padx=50, pady=(40,40))

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="🏠 Home",
                                                   fg_color="transparent",
                                                   command=self.visual_event, font=ctk.CTkFont(size=25, weight="bold"))
        self.home_button.grid(row=2, column=0, sticky="ew")

        self.loan_frame_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="⏳ Loan",
                                                   fg_color="transparent",
                                                   command=self.code_event, font=ctk.CTkFont(size=25, weight="bold"))
        self.loan_frame_button.grid(row=3, column=0, sticky="ew")
        

        self.visual_frame = ctk.CTkFrame(self, corner_radius=0)

        self.visual_window = ctk.CTkFrame(self.visual_frame, corner_radius=0)
        self.visual_window.pack()

        self.code_frame = ctk.CTkFrame(self, corner_radius=0)

        #self.visual_frame = ctk.CTkFrame(self, corner_radius=0)

        def wait_proj():
            if CurrentProj._proj_path != None:
                self.visual_window.pack_forget()
                self.visual_window = AppHandler().convert_to_frame(CurrentProj.proj_path)
                self.visual_window.pack()
            else:
                self.after(100, wait_proj)
        
        wait_proj()
        self.open_toplevel(AppCreatorStart(start="first"))
        self.visual_event
    
    # Opens a TopLevel window
    def open_toplevel(self, function):
        self.withdraw()
        tl = function
    # END

    # Define the functions for the menu options here
    def new_proj(self):
        AppCreatorStart(create="new")
    
    def load_proj(self):
        AppCreatorStart(create="load")
    
    def cut(self):
        print("Cut")
    
    def copy(self):
        print("Copy")
    
    def paste(self):
        print("Paste")
    
    def settings(self):
        #Settings()
        print("Settings")
    
    def documentation(self):
        open_new_tab("https://github.com/BusterLandstrom/CTkAppCreator")
    
    def about(self):
        print("Bbout")

    def select_frame_by_name(self, name):
        if name == "visual":
            self.visual_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.visual_frame.grid_forget()
        if name == "code":
            self.code_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.code_frame.grid_forget()

    def visual_event(self):
        self.select_frame_by_name("visual")
    
    def code_event(self):
        self.select_frame_by_name("code")

    # Event trigger to change scaling of UI elements
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
    # END



# Main loop (Application loop)
if __name__ == "__main__":

    CurrentProj = CurrentProj()

    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    # Main window
    root=AppCreator()
    root.title("AppCreator")
    root.mainloop()
# END
