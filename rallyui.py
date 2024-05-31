import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import rallydb as rb

# changelog
# create very important panic function

# TODO
# arrange stuff
# move description to info box
# daily/weekly counter
# add function to get filepath or custom filename
# maybe button to select file/filepath
# button to write stages to file?

# ideas
# make some buttons on top for more info, maybe for file loading
# make rallyui standalone?
# if searching for stage, activate the right country

# bugs
# on macOS arrow keys dont work + plus weird layout


def panic():
    rb.eprint("ERROR: oh my god, run RUN!!!")
    rb.sys.exit()

class App:
    # every line in file
    stages_from_file: list[rb.Stage] = []
    # every selected object left side
    selected_objects: list[rb.Stage] = []
    # same but the objects
    selected_options_list: list[str] = []
    # results list, left side, the objects
    results_vector: list[rb.Stage] = []

    all_locations: list[str] = list(rb.Stage.location_stage_names.keys())
    all_groups: list[str] = list(rb.Stage.car_names.keys())
    all_stages = list(rb.Stage.location_stage_names.values())
    stages_list = []
    for stages in all_stages:
        for stage in stages:
            stages_list.append(stage)
    # tthis is the only way surely...
    user_input_stage = ""

    def __init__(self, root):
        self.root = root
        self.root.title("RallyUI")
        #root.geometry("800x600")
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Help", command=self.show_help)
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="Options", menu=self.file_menu)

        self.root.config(menu=self.menu_bar)

        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()
        #self.results_label = tk.Label(self.root, text="Results").grid(row=0, column=0)
        self.results_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=60, height=15,font=("courier", 12))
        self.results_listbox.bind('<FocusIn>', self.on_focus_in)
        self.results_listbox.bind('<FocusOut>', self.on_focus_out)
        self.results_listbox.grid(row=0, column=0, padx=10, pady=5)
        self.results_button = tk.Button(self.root, text='add>>', command=self.add_stage)
        self.results_button.grid(row=1, column=1)
        # right side
        #self.selected_label = tk.Label(self.root, text="Selected Stages").grid(row=0, column=3)
        self.selected_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=60, height=15, font=("courier", 12))
        self.selected_listbox.bind('<FocusIn>', self.on_focus_in)
        self.selected_listbox.bind('<FocusOut>', self.on_focus_out)
        self.selected_listbox.grid(row=0, column=3, padx=10, pady=5)
        self.selected_button = tk.Button(self.root, text='<<remove', command=self.remove_stage)
        self.selected_button.grid(row=2, column=1)

        #self.results_label = tk.Label(self.root, text="total time").grid(row=3, column=2)
        self.selected_stages_time = tk.Label(self.root, text="total stages time", font=("courier", 12))
        self.selected_stages_time.grid(row=1, column=3)
        self.selected_label = tk.Label(self.root, text="sum of best", font=("courier", 12)).grid(row=2, column=3)

        self.total_time_label = tk.Label(self.root, text="total time", font=("courier", 12))
        self.total_time_label.grid(row=1, column=0)

        self.clear_button = tk.Button(self.root, text="Clear all", command=self.clear_selections)
        self.clear_button.grid(row=4, column=1)

        self.clear_user_input = tk.Button(self.root, text="reset search", command=self.clear_input)
        self.clear_user_input.grid(row=9, column=1)

        self.text = tk.Label(self.root, text="use arrow keys or hjkl\nto add or remove stages").grid(row=5, column=1)

        self.check_vars = {}
        self.labels: list[str] = App.all_locations

        self.label_entry = tk.Label(self.root, text="search for stagename:").grid(row=7, column=1)
        self.entry = tk.Entry(root)
        self.entry.grid(row=8, column=1)
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry.bind('<FocusOut>', self.on_entry_focus_out)


        root.bind('<Up>', self.navigate)
        root.bind('<Down>', self.navigate)
        root.bind('<Right>', self.add_stage)
        root.bind('<Left>', self.remove_stage)
        root.bind('h', self.remove_stage)
        root.bind('l', self.add_stage)
        root.bind('j', self.navigate)
        root.bind('k', self.navigate)
        self.results_listbox.select_set(0)
        self.results_listbox.activate(0)

        for i, label in enumerate(self.labels):
            i += 4
            var = tk.BooleanVar()
            self.check_vars[label] = var
            checkbutton = tk.Checkbutton(root, text=label, variable=var, command=lambda var=var, label=label: self.toggle_action(var, label))
            checkbutton.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        self.check_vars = {}
        self.labels: list[str] = App.all_groups
        for i, label in enumerate(self.labels):
            i += 4
            var = tk.BooleanVar()
            self.check_vars[label] = var
            checkbutton = tk.Checkbutton(root, text=label, variable=var, command=lambda var=var, label=label: self.toggle_action(var, label))
            checkbutton.grid(row=i, column=0, padx=110, pady=5, sticky="w")

        self.check_vars = {}
        self.labels: list[str] = ["dry", "wet"]
        for i, label in enumerate(self.labels):
             i += 4
             var = tk.BooleanVar()
             self.check_vars[label] = var
             checkbutton = tk.Checkbutton(root, text=label, variable=var, command=lambda var=var, label=label: self.toggle_action(var, label))
             checkbutton.grid(row=i, column=0, padx=210, pady=5, sticky="w")

        self.check_vars = {}
        self.labels: list[str] = ["forward", "reverse"]
        for i, label in enumerate(self.labels):
             i += 4
             var = tk.BooleanVar()
             self.check_vars[label] = var
             checkbutton = tk.Checkbutton(root, text=label, variable=var, command=lambda var=var, label=label: self.toggle_action(var, label))
             checkbutton.grid(row=i, column=0, padx=310, pady=5, sticky="w")

        self.update_all_stages()

    def on_focus_in(self, event):
            self.bind_navigation_keys()
    def on_focus_out(self, event):
            self.unbind_navigation_keys()
    def on_entry_focus_in(self, event):
            self.unbind_navigation_keys()
    def on_entry_focus_out(self, event):
            self.bind_navigation_keys()

    def bind_navigation_keys(self):
        self.root.bind('<Up>', self.navigate)
        self.root.bind('<Down>', self.navigate)
        self.root.bind('h', self.navigate)
        self.root.bind('j', self.navigate)
        self.root.bind('k', self.navigate)
        self.root.bind('l', self.navigate)
        self.root.bind('<Right>', self.add_stage)  # Bind the Right arrow key to add_stage
        self.root.bind('<Left>', self.remove_stage)  # Bind the Right arrow key to add_stage

    def unbind_navigation_keys(self):
        self.root.unbind('<Up>')
        self.root.unbind('<Down>')
        self.root.unbind('h')
        self.root.unbind('j')
        self.root.unbind('k')
        self.root.unbind('l')
        self.root.unbind('<Right>')
        self.root.unbind('<Left>')

    def navigate(self, event):
        focused_widget = self.root.focus_get()
        if isinstance(focused_widget, tk.Listbox):
            if event.keysym in ['Up', 'k']:
                self.move_up(focused_widget)
            elif event.keysym in ['Down', 'j']:
                self.move_down(focused_widget)
            elif event.keysym in ['l']:
                self.add_stage()
            elif event.keysym in ['h']:
                self.remove_stage()

    def move_up(self, listbox):
        current_selection = listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
            if current_index > 0:
                listbox.select_clear(current_index)
                listbox.select_set(current_index - 1)
                listbox.activate(current_index - 1)
                listbox.see(current_index - 1)

    def move_down(self, listbox):
        current_selection = listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
            if current_index < listbox.size() - 1:
                listbox.select_clear(current_index)
                listbox.select_set(current_index + 1)
                listbox.activate(current_index + 1)
                listbox.see(current_index + 1)
    def show_help(self):
        messagebox.showinfo("Help", "Add search options with the boxes,\nadd stages to the right window with arrow keyes or with the move>> button\nThe search function only works if the corresponding country is selected.")


    def read_file(self):
        with open("Leaderboards.txt", 'r') as file:
            lines = file.readlines()
        for line in lines:
            if "daily" in line or "weekly" in line:
               continue
            try:
                App.stages_from_file.append(rb.Stage(line))
            except TypeError:
                continue

    def update_all_stages(self):
        # left side
        self.results_listbox.delete(0, tk.END)
        self.results_vector.clear()
        for object in App.stages_from_file:
            if (object.location in App.selected_options_list and
                object.group in App.selected_options_list and
                object.weather in App.selected_options_list and
                object.direction in App.selected_options_list and
                (not App.user_input_stage or App.user_input_stage in object.stage)
            ):

                time = object.time.get_time()
                string: str = f"{object.location:<10} {object.stage:<17} {object.group:<7}{object.direction:<3} {object.weather:<3} {time}"
                self.results_listbox.insert(tk.END, string)
                self.results_vector.append(object)
                #print(f"{object.time.get_time()} {object.stage}")
            else:
                continue
        self.update_total_time()
        self.update_stage_time()
        self.results_listbox.select_set(0)
        self.results_listbox.activate(0)

    def add_stage(self, event=None):
        focused_widget = self.root.focus_get()
        if focused_widget == self.results_listbox:
            selected_idx = self.results_listbox.get(tk.ACTIVE)
            index = self.results_listbox.curselection()[0]
            if selected_idx:
                self.selected_listbox.insert(tk.END, selected_idx)
                App.selected_objects.append(App.results_vector[index])
            self.update_stage_time()

    # delete this..
    def add_stage_test(self):
        # todo check both list,
        focused_widget = self.root.focus_get()
        selected_idx = self.results_listbox.get(tk.ACTIVE)
        try:
            index = self.results_listbox.curselection()[0]
            if selected_idx:
                self.selected_listbox.insert(tk.END, selected_idx)
                App.selected_objects.append(App.results_vector[index])
            self.update_stage_time()
        except IndexError:
            rb.eprint("debug: nothing to add")

    def remove_stage(self, event=None):
        selected_idx = self.selected_listbox.curselection()
        try:
            index = self.selected_listbox.curselection()[0]
            if selected_idx:
                self.selected_listbox.delete(selected_idx)
                App.selected_objects.pop(index)
            self.update_stage_time()
            if index <= 0:
                self.selected_listbox.select_set(0)
            else:
                self.selected_listbox.select_set(index-1)
                self.selected_listbox.activate(0)
        except IndexError:
            rb.eprint("debug: nothing to remove")

    def clear_selections(self):
        self.selected_listbox.delete(0, tk.END)
        App.selected_objects.clear()
        self.update_stage_time()

    def update_stage_time(self):
        total_time = 0
        hours, minutes, seconds, ms = 0,0,0,0
        for stage in App.selected_objects:
            if stage.time_ms >= 356400000:
                continue
            total_time += stage.time_ms
        try:
            hours, minutes, seconds, ms = rb.Time.convert_race_time(total_time)
        except TypeError:
            print("error converting number in Leaderboards file to time")
        total_time_str = f"{hours}:{minutes:02d}:{seconds:02d}.{ms:03d}"
        #print(f"{hours}:{minutes}:{seconds}.{ms}")
        self.selected_stages_time.config(text=total_time_str)

    def update_total_time(self):
        total_time = 0
        hours, minutes, seconds, ms = 0,0,0,0
        for stage in self.results_vector:
            total_time += stage.time_ms
            try:
                hours, minutes, seconds, ms = rb.Time.convert_race_time(total_time)
            except TypeError:
                continue
        total_time_str = f"{hours}:{minutes:02d}:{seconds:02d}.{ms:03d}"
        self.total_time_label.config(text=total_time_str)

    def toggle_action(self, var, label):
        if var.get():
            App.selected_options_list.append(label)
            #print(f"{label} enabled")
        else:
            #print(f"{label} disabled")
            App.selected_options_list.remove(label)
        self.update_all_stages()
        self.results_listbox.select_set(0)
        self.results_listbox.activate(0)

    def on_enter(self, event):
        user_input: str = self.entry.get()
        user_list: list[str] = []
        user_list.append(user_input)
        print(f"user: {user_input}")
        #self.entry.delete(0, tk.END)
        try:
            #App.stages_list.clear()
            search_results: list[str] = rb.find_stage(user_list)
            #App.stages_list.append(search_results[0])
            App.user_input_stage = search_results[0]
            print(f"search: {search_results}")
            self.update_all_stages()
            # add a clear button
        except SystemError:
            pass
            #rb.eprint("ERROR: stage not found?")

    def clear_input(self):
        self.entry.delete(0, tk.END)
        App.user_input_stage = ""
        self.update_all_stages()
    # find stage
    # rb.all_stages
    # rb.find_stage()


def main():
    root = tk.Tk()
    app = App(root)
    app.read_file()
    root.mainloop()

if __name__ == "__main__":
    main()
