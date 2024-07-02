import tkinter as tk
import math

class RadarUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Radar UI")

        # Create menu
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open")
        self.filemenu.add_command(label="Save")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.editmenu.add_command(label="Cut")
        self.editmenu.add_command(label="Copy")
        self.editmenu.add_command(label="Paste")
        self.editmenu.add_command(label="New Object", command=self.new_object)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.optionsmenu = tk.Menu(self.menubar, tearoff=0)
        self.optionsmenu.add_command(label="Settings")
        self.menubar.add_cascade(label="Options", menu=self.optionsmenu)

        self.root.config(menu=self.menubar)

        # Create main screen
        self.main_screen = tk.Canvas(self.root, width=800, height=400, bg="black", highlightthickness=0)
        self.main_screen.pack(side="top", fill="both", expand=True)

        # Create radar screen-like pattern on main screen
        self.center_x = 0
        self.center_y = 0
        self.radius = 0
        self.zoom_level = 1
        self.draw_radar_screen()

        # Create right-hand side bar
        self.right_bar = tk.Frame(self.root, width=200, bg="gray")
        self.right_bar.pack(side="right", fill="y")

        # Create sliders in right-hand side bar
        self.slider1 = tk.Scale(self.right_bar, from_=0, to=100, orient="horizontal")
        self.slider1.pack(fill="x")

        self.slider2 = tk.Scale(self.right_bar, from_=0, to=100, orient="horizontal")
        self.slider2.pack(fill="x")

        # Create bottom bar
        self.bottom_bar = tk.Frame(self.root, height=50, bg="gray")
        self.bottom_bar.pack(side="bottom", fill="x")

        # Create sliders in bottom bar
        self.slider3 = tk.Scale(self.bottom_bar, from_=0, to=100, orient="horizontal")
        self.slider3.pack(side="left")

        self.slider4 = tk.Scale(self.bottom_bar, from_=0, to=100, orient="horizontal")
        self.slider4.pack(side="left")

        # Bind mouse wheel event to zoom
        self.main_screen.bind("<MouseWheel>", self.zoom)

    def draw_radar_screen(self):
        self.main_screen.delete("all")
        self.center_x = self.main_screen.winfo_width() / 2
        self.center_y = self.main_screen.winfo_height() / 2
        self.radius = min(self.center_x, self.center_y) - 20
        for i in range(10):
            radius = i * 40 / self.zoom_level
            self.main_screen.create_oval(self.center_x - radius, self.center_y - radius, self.center_x + radius, self.center_y + radius, outline="green")
            if i > 0:
                distance = i * 40 / self.zoom_level / 1000
                self.main_screen.create_text(self.center_x, self.center_y - radius, text=f"{distance:.1f} km", fill="green")
        for i in range(36):
            angle = i * 10
            x = self.center_x + math.cos(math.radians(angle)) * self.radius / self.zoom_level
            y = self.center_y + math.sin(math.radians(angle)) * self.radius / self.zoom_level
            self.main_screen.create_line(self.center_x, self.center_y, x, y, fill="green")

    def resize(self, event):
        self.draw_radar_screen()

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_level /= 1.1
        else:
            self.zoom_level *= 1.1
        self.draw_radar_screen()

    def new_object(self):
        self.new_object_window = tk.Toplevel(self.root)
        self.new_object_window.title("New Object")

        self.form_label = tk.Label(self.new_object_window, text="Form:")
        self.form_label.pack()

        self.form_var = tk.StringVar()
        self.form_var.set("Circle")
        self.circle_radio = tk.Radiobutton(self.new_object_window, text="Circle",variable=self.form_var, value="Circle")
        self.circle_radio.pack()
        self.square_radio = tk.Radiobutton(self.new_object_window, text="Square", variable=self.form_var, value="Square")
        self.square_radio.pack()
        self.triangle_radio = tk.Radiobutton(self.new_object_window, text="Triangle", variable=self.form_var, value="Triangle")
        self.triangle_radio.pack()

        self.size_label = tk.Label(self.new_object_window, text="Size:")
        self.size_label.pack()
        self.size_entry = tk.Entry(self.new_object_window)
        self.size_entry.pack()

        self.color_label = tk.Label(self.new_object_window, text="Color:")
        self.color_label.pack()
        self.color_button =tk.Button(self.new_object_window, text="Choose Color", command=self.choose_color)
        self.color_button.pack()

        self.create_button = tk.Button(self.new_object_window, text="Create", command=self.create_object)
        self.create_button.pack()

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        self.color_button.config(text=color)

    def create_object(self):
        form = self.form_var.get()
        size = int(self.size_entry.get())
        color = self.color_button.cget("text")
        if form == "Circle":
            self.main_screen.create_oval(self.center_x - size, self.center_y - size, self.center_x + size, self.center_y + size, fill=color)
        elif form == "Square":
            self.main_screen.create_rectangle(self.center_x - size, self.center_y - size, self.center_x + size, self.center_y + size, fill=color)
        elif form == "Triangle":
            x1 = self.center_x - size
            y1 = self.center_y + size
            x2 = self.center_x + size
            y2 = self.center_y + size
            x3 = self.center_x
            y3 = self.center_y - size
            self.main_screen.create_polygon(x1, y1, x2, y2, x3, y3, fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    ui = RadarUI(root)
    root.bind("<Configure>", ui.resize)
    root.mainloop()