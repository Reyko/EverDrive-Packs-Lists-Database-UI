from tkinter import *
from utils import *


class Dialog(Toplevel):
    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.scripts_folder = StringVar()
        if self.parent.folder:
            self.scripts_folder.set(get_abs_path(self.parent.folder))
        else:
            self.scripts_folder.set("")

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        textbox_path = Entry(master, width=50,
                             textvariable=self.scripts_folder)
        textbox_path.grid(column=2, row=1, sticky=E)
        ttk.Label(master, text="ROMs folder: "
                  ).grid(column=1, row=1, sticky=W)
        browse_btn = ttk.Button(master, text="Browse", underline=0,
                                command=lambda:
                                select_folder(self.scripts_folder,
                                              "Select Pack Scripts folder"))
        browse_btn.grid(column=3, row=1, sticky=W)

        self.bind("<Alt_L><b>",
                  lambda e: select_folder(self.scripts_folder,
                                          "Select Pack Scripts folder"))
        textbox_path.focus_set()

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, underline=0,
                   command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        x = Button(box, text="Cancel", width=10, underline=0,
                   command=self.cancel)
        x.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Alt_L><o>", self.ok)
        self.bind("<Alt_L><c>", self.cancel)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        if len(self.scripts_folder.get()) > 0:
            # Enable build and parse buttons
            self.parent.toggle_action_buttons(True)
        else:
            # Disable build and parse buttons
            self.parent.toggle_action_buttons(False)

        self.parent.focus_set()
        self.destroy()
        # self.parent.destroy()

    #
    # command hooks

    def validate(self):
        out = False
        if (not self.scripts_folder.get() == ""):
            path = Path(self.scripts_folder.get())
            if path.exists() and path.is_dir():
                out = True
        else:
            # Mark the textbox has an error
            pass

        return out

    def apply(self):
        folder = Path(self.scripts_folder.get())
        build_file, parse_file = get_pack_scripts_paths(folder)
        self.parent.folder = folder
        self.parent.build_file = build_file
        self.parent.parse_file = parse_file

        save_ini_file(get_ini_file(), "UI",
                      {"scripts_folder": get_abs_path(folder)})