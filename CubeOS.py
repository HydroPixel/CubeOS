# CubeOS Advanced Timer

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import random
import time
import sys
import os

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

window = Tk()
window.iconphoto(
    False,
    PhotoImage(file=resource_path("CubeOS.png"))
)
window.geometry("1000x500")
window.config(bg="#000000", border=10, relief="ridge")
window.title("CubeOS")

# ---------------- VARIABLES ---------------- #

is_fullscreen = False
is_running = False
start_time = 0
final_time = 0

scramble = ""

moves = [
    "R ", "R' ", "R2 ",
    "L ", "L' ", "L2 ",
    "F ", "F' ", "F2 ",
    "B ", "B' ", "B2 ",
    "D ", "D' ", "D2 ",
    "U ", "U' ", "U2 "
]

rgb_colors = [
    "#ff0000",
    "#ff7300",
    "#ffee00",
    "#48ff00",
    "#00ffd5",
    "#002bff",
    "#7a00ff",
    "#ff00c8"
]

rgb_index = 0

times = []

# ---------------- FILES ---------------- #

try:
    with open("times.txt", "r") as file:
        lines = file.readlines()

        for line in lines:

            line = line.strip()

            try:
                times.append(float(line))

            except:
                pass

except:
    open("times.txt", "w").close()

# ---------------- FUNCTIONS ---------------- #

def save_times():

    with open("times.txt", "w") as file:

        for solve in times:
            file.write(f"{solve}\n")

        if len(times) > 0:

            file.write(f"\nBEST:{min(times)}")
            file.write(f"\nWORST:{max(times)}")


def toggle_fullscreen():

    global is_fullscreen

    window.attributes("-fullscreen", not is_fullscreen)

    is_fullscreen = not is_fullscreen


def scrambler():

    global scramble

    scramble = ""

    last_move = ""

    for _ in range(random.randint(12, 15)):

        move = random.choice(moves)

        while move[0] == last_move:
            move = random.choice(moves)

        scramble += move

        last_move = move[0]

    scramble_label.config(text=scramble)


def mean():

    if len(times) == 0:
        return "N/A"

    return round(sum(times) / len(times), 3)


def mo3():

    if len(times) < 3:
        return "N/A"

    last3 = times[-3:]

    return round(sum(last3) / 3, 3)


def ao5():

    if len(times) < 5:
        return "N/A"

    last5 = times[-5:].copy()

    last5.remove(max(last5))
    last5.remove(min(last5))

    return round(sum(last5) / len(last5), 3)


def ao12():

    if len(times) < 12:
        return "N/A"

    last12 = times[-12:].copy()

    last12.remove(max(last12))
    last12.remove(min(last12))

    return round(sum(last12) / len(last12), 3)


def ao50():

    if len(times) < 50:
        return "N/A"

    last50 = times[-50:].copy()

    last50.remove(max(last50))
    last50.remove(min(last50))

    return round(sum(last50) / len(last50), 3)


def ao100():

    if len(times) < 100:
        return "N/A"

    last100 = times[-100:].copy()

    last100.remove(max(last100))
    last100.remove(min(last100))

    return round(sum(last100) / len(last100), 3)


def update_stats():

    mo3_label.config(text=f"Mo3: {mo3()}")
    ao5_label.config(text=f"Ao5: {ao5()}")
    ao12_label.config(text=f"Ao12: {ao12()}")
    ao50_label.config(text=f"Ao50: {ao50()}")
    ao100_label.config(text=f"Ao100: {ao100()}")
    mean_label.config(text=f"Mean: {mean()}")

    if len(times) > 0:

        best_label.config(text=f"Best: {min(times)}")
        worst_label.config(text=f"Worst: {max(times)}")

    else:

        best_label.config(text="Best: N/A")
        worst_label.config(text="Worst: N/A")


def update_timer():

    if is_running:

        current_time = time.time() - start_time

        TimeButton.config(text=f"{current_time:.3f}")

        window.after(10, update_timer)


def toggle_timer():

    global is_running
    global start_time
    global final_time

    if not is_running:

        is_running = True

        start_time = time.time()

        update_timer()

    else:

        is_running = False

        final_time = round(time.time() - start_time, 3)

        times.append(final_time)

        save_times()

        update_stats()

        scrambler()


def delete_last():

    if len(times) > 0:

        times.pop()

        save_times()

        update_stats()


def delete_all():

    answer = messagebox.askyesno(
        "Delete All",
        "Delete all solves?"
    )

    if answer:

        times.clear()

        save_times()

        update_stats()


def export_solves():

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:

        with open(file_path, "w") as file:

            for solve in times:
                file.write(f"{solve}\n")


def rgb_title_animation():

    global rgb_index

    Title_label.config(fg=rgb_colors[rgb_index])

    rgb_index += 1

    if rgb_index >= len(rgb_colors):
        rgb_index = 0

    window.after(120, rgb_title_animation)


def apply_theme(bg, fg, button_bg):

    window.config(bg=bg)

    stats_frame.config(bg=bg)
    center_frame.config(bg=bg)
    top_bar.config(bg=bg)
    scramble_frame.config(bg=bg)

    Title_label.config(bg=bg)

    scramble_label.config(bg=bg, fg=fg)

    labels = [
        mo3_label,
        ao5_label,
        ao12_label,
        ao50_label,
        ao100_label,
        mean_label,
        best_label,
        worst_label
    ]

    for label in labels:
        label.config(bg=bg, fg=fg)

    buttons = [
        toggle_fullscreen_button,
        settings_button,
        scramble_button,
        delete_last_button,
        TimeButton
    ]

    for button in buttons:
        button.config(bg=button_bg, fg=fg)


def settings_screen():

    settings = Toplevel(window)

    settings.geometry("400x500")

    settings.config(bg="#111111")

    settings.title("CubeOS Settings")

    Label(
        settings,
        text="Themes",
        font=("Michroma", 18),
        bg="#111111",
        fg="white"
    ).pack(pady=10)

    Button(
        settings,
        text="OLED",
        command=lambda: apply_theme("black", "white", "#474747")
    ).pack(pady=5)

    Button(
        settings,
        text="Matrix",
        command=lambda: apply_theme("black", "lime", "#003300")
    ).pack(pady=5)

    Button(
        settings,
        text="Ice",
        command=lambda: apply_theme("#001122", "cyan", "#003344")
    ).pack(pady=5)

    Button(
        settings,
        text="Inferno",
        command=lambda: apply_theme("#220000", "orange", "#661100")
    ).pack(pady=5)

    Button(
        settings,
        text="Export Solves",
        command=export_solves
    ).pack(pady=20)

    Button(
        settings,
        text="Delete All Solves",
        command=delete_all,
        bg="#440000",
        fg="white"
    ).pack(pady=10)

# ---------------- TOP BAR ---------------- #

top_bar = Frame(window, bg="black")

top_bar.pack(fill="x")

# ---------------- FULLSCREEN BUTTON ---------------- #

toggle_fullscreen_button = Button(
    top_bar,
    text="Toggle Fullscreen",
    font=("Michroma", 10),
    bg="#474747",
    fg="white",
    activebackground="white",
    activeforeground="#474747",
    border=5,
    relief="ridge",
    command=toggle_fullscreen
)


toggle_fullscreen_button.pack(
    side="left",
    padx=5,
    pady=5
)

# ---------------- SETTINGS BUTTON ---------------- #

settings_button = Button(
    top_bar,
    text="Settings",
    font=("Michroma", 10),
    bg="#474747",
    fg="white",
    border=5,
    relief="ridge",
    command=settings_screen
)

settings_button.pack(
    side="right",
    padx=5,
    pady=5
)

# ---------------- MAIN AREA ---------------- #

main_frame = Frame(window, bg="black")

main_frame.pack(expand=True, fill="both")

# ---------------- STATS ---------------- #

stats_frame = Frame(main_frame, bg="black")

stats_frame.pack(side="left", fill="y", padx=20)

mo3_label = Label(stats_frame, text="Mo3: N/A", font=("Michroma", 10), bg="black", fg="white")
mo3_label.pack(anchor="w", pady=5)

ao5_label = Label(stats_frame, text="Ao5: N/A", font=("Michroma", 10), bg="black", fg="white")
ao5_label.pack(anchor="w", pady=5)

ao12_label = Label(stats_frame, text="Ao12: N/A", font=("Michroma", 10), bg="black", fg="white")
ao12_label.pack(anchor="w", pady=5)

ao50_label = Label(stats_frame, text="Ao50: N/A", font=("Michroma", 10), bg="black", fg="white")
ao50_label.pack(anchor="w", pady=5)

ao100_label = Label(stats_frame, text="Ao100: N/A", font=("Michroma", 10), bg="black", fg="white")
ao100_label.pack(anchor="w", pady=5)

mean_label = Label(stats_frame, text="Mean: N/A", font=("Michroma", 10), bg="black", fg="white")
mean_label.pack(anchor="w", pady=5)

best_label = Label(stats_frame, text="Best: N/A", font=("Michroma", 10), bg="black", fg="white")
best_label.pack(anchor="w", pady=5)

worst_label = Label(stats_frame, text="Worst: N/A", font=("Michroma", 10), bg="black", fg="white")
worst_label.pack(anchor="w", pady=5)

# ---------------- CENTER ---------------- #

center_frame = Frame(main_frame, bg="black")

center_frame.pack(side="left", expand=True, fill="both")

# ---------------- TITLE ---------------- #

Title_label = Label(
    center_frame,
    text="CubeOS",
    font=("Michroma", 35),
    bg="#000000",
    fg="#ffffff"
)

Title_label.pack(pady=10)

# ---------------- SCRAMBLE ---------------- #

scramble_frame = Frame(center_frame, bg="black")

scramble_frame.pack(pady=10)

scramble_label = Label(
    scramble_frame,
    text="",
    font=("Iceberg", 20),
    bg="#000000",
    fg="#ffffff"
)

scramble_label.pack(side="left", pady=5)

scramble_button = Button(
    scramble_frame,
    text="Scramble ⟳",
    font=("Michroma", 10),
    bg="#474747",
    fg="white",
    border=5,
    relief="ridge",
    command=scrambler
)

scramble_button.pack(side="left", padx=10)

# ---------------- DELETE LAST ---------------- #

delete_last_button = Button(
    scramble_frame,
    text="Delete Last",
    font=("Michroma", 10),
    bg="#550000",
    fg="white",
    border=5,
    relief="ridge",
    command=delete_last
)


delete_last_button.pack(side="left", padx=10)

# ---------------- TIMER ---------------- #

TimeButton = Button(
    center_frame,
    text="0.000",
    font=("Michroma", 40),
    bg="#474747",
    fg="white",
    activebackground="white",
    activeforeground="#474747",
    border=5,
    relief="ridge",
    command=toggle_timer
)

TimeButton.pack(
    pady=20,
    padx=20,
    expand=True,
    fill="both"
)

# ---------------- START ---------------- #

scrambler()
update_stats()
rgb_title_animation()

window.mainloop()