import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os
import json

LOCATION = "/Users/celes/Library/Containers/com.github.ivoronin.TomatoBar/Data/Library/Caches/TomatoBar.log"
CURRENT_LOCATION = (
    "/Users/celes/Documents/Projects/PythonSmallTool/visualize-pomodoro-menu/"
)
BACKUP_LOCATION = (
    "/Users/celes/Documents/Projects/PythonSmallTool/visualize-pomodoro-menu/backup/"
)
Night_Owl_Calibration = 4  # hours


def load_log_file(filename):
    data = []
    with open(filename, "r") as file:
        formatted_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")
        with open(BACKUP_LOCATION + formatted_datetime + ".log", "w") as wfile:
            wfile.write(file.read())
        file.seek(0)
        for line in file:
            try:
                json_object = json.loads(line)
                if "event" in json_object:
                    data.append(json_object)
            except json.JSONDecodeError:
                print(f"Failed to parse JSON from line: {line.strip()}")

    return data


def create_event_list(filename):
    content = load_log_file(filename)
    Event_List = []
    for obj in content:
        if obj["toState"] == "work":
            start = obj["timestamp"]
        elif (start != -1) and (
            (obj["toState"] == "rest") or (obj["toState"] == "idle")
        ):
            end = obj["timestamp"]
            datetime_start = datetime.fromtimestamp(start)
            datetime_end = datetime.fromtimestamp(end)
            Event_List.append(
                {
                    "date": datetime_start,
                    "focustime": round(
                        (datetime_end - datetime_start).total_seconds() / 60
                    ),
                }
            )
            start = -1
    return Event_List


def create_date_list(Event_List):
    dic = dict()
    for item in Event_List:
        date, focustime = (
            item["date"] - timedelta(hours=Night_Owl_Calibration)
        ).date(), item["focustime"]
        if date in dic:
            dic[date] += round(focustime / 60, 1)
        else:
            dic[date] = round(focustime / 60, 1)
    return dic


def export_date_list():
    return create_date_list(create_event_list(LOCATION))


DATA = export_date_list()
current_datetime = datetime.now()
iso_year, iso_week_number, _ = current_datetime.isocalendar()
# Global variable to store the selected year
selected_year = iso_year
selected_mode = "year"
selected_week = iso_week_number


def update_heatmap():
    # Get the selected mode from the dropdown menu
    selected_mode = mode_var.get()
    selected_year = int(year_var.get())
    selected_week = int(week_var.get())

    if selected_mode == "year":
        update_year_heatmap()
    elif selected_mode == "week":
        update_week_histogram()


def update_week_histogram():
    # Dummy data for the histogram (replace this with your actual data)
    selected_year = int(year_var.get())
    selected_week = int(week_var.get())
    week_data = generate_week_data(selected_year, selected_week)

    # Clear the previous plot using the Figure instance
    fig.clf()

    # Extracting data for the histogram
    dates = [data["date"].strftime("%A") for data in week_data]
    focus_times = [data["focus_time"] for data in week_data]

    # Plotting the histogram
    ax = fig.add_subplot(111)
    ax.bar(dates, focus_times, color="seagreen")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Focus Time (hours)")
    ax.set_title(f"Weekly Focus Time Histogram ({selected_year}, Week {selected_week})")

    # Update the plot in the tkinter window
    canvas.draw()


def generate_week_data(year, week):
    week_start = datetime.fromisocalendar(year, week, 1)
    week_data = []

    for i in range(7):
        current_day = week_start + timedelta(days=i)
        if current_day.date() in DATA:
            focus_time = DATA[current_day.date()]
        else:
            focus_time = 0
        week_data.append({"date": current_day, "focus_time": focus_time})
    return week_data


def next_item():
    selected_mode = mode_var.get()
    selected_year = int(year_var.get())
    selected_week = int(week_var.get())
    if selected_mode == "week":
        num_weeks = int(
            (datetime(selected_year + 1, 1, 1) - datetime(selected_year, 1, 1)).days / 7
        )
        next_week = min(selected_week + 1, num_weeks)
        week_var.set(next_week)
    if selected_mode == "year":
        num_years = datetime.now().year
        next_year = min(selected_year + 1, num_years)
        year_var.set(next_year)
    update_heatmap()


def prev_item():
    selected_mode = mode_var.get()
    selected_year = int(year_var.get())
    selected_week = int(week_var.get())
    if selected_mode == "week":
        prev_week = max(selected_week - 1, 1)
        week_var.set(prev_week)
    elif selected_mode == "year":
        prev_year = max(selected_year - 1, 2020)
        year_var.set(prev_year)
    update_heatmap()


# Function to update the heatmap based on selected year
def update_year_heatmap():
    # Get the selected year from the dropdown menu
    selected_year = int(year_var.get())
    # Create a numpy array to store the heatmap data
    heatmap = np.zeros((12, 31)) - 1

    # Iterate over each day of the selected year
    start_date = datetime(selected_year, 1, 1)
    for i in range(365):
        date = start_date + timedelta(days=i)
        month = date.month - 1
        day = date.day - 1
        if date.date() in DATA:
            focus_time = DATA[date.date()]
        else:
            focus_time = -1
        heatmap[month, day] = focus_time

    # Clear the previous plot using the Figure instance
    fig.clf()

    # Plot the heatmap using matshow
    ax = fig.add_subplot(111)
    cax = ax.matshow(heatmap, cmap="Greens")

    # Set the X and Y axis labels
    ax.set_xlabel("Day of Month")
    ax.set_ylabel("Month")

    # Set custom X and Y tick labels with increased font size
    ax.set_xticks(np.arange(0, 31))
    ax.set_xticklabels([str(i) for i in range(1, 32)], fontsize=8)
    ax.set_yticks(np.arange(0, 12))
    ax.set_yticklabels([month for month in np.arange(1, 13)], fontsize=8)

    # Add a colorbar legend
    fig.colorbar(cax)

    # Update the plot in the tkinter window
    canvas.draw()


# Create the tkinter window
window = tk.Tk()
window.title("Heatmap")


# Create a dropdown menu to select the modes
mode_var = tk.StringVar(window)
mode_choices = ["week", "month", "year"]
mode_var.set("week")
mode_dropdown = tk.OptionMenu(window, mode_var, *mode_choices)
mode_dropdown.grid(row=0, column=1, padx=5, sticky="W")

# Create a dropdown menu to select the year
year_var = tk.StringVar(window)
year = datetime.now().year
year_choices = [str(year) for year in range(year - 3, year + 1)]
year_var.set(iso_year)
year_dropdown = tk.OptionMenu(window, year_var, *year_choices)
year_dropdown.grid(row=0, column=2, padx=5, sticky="W")

# Create a dropdown menu to select the month
month_var = tk.StringVar(window)
month_choices = [str(year) for year in range(1, 13)]
month_dropdown = tk.OptionMenu(window, month_var, *month_choices)
month_dropdown.grid(row=0, column=3, padx=5, sticky="W")

# Create a dropdown menu to select the week
week_var = tk.StringVar(window)
# Calculate the number of weeks in the selected year
num_weeks = int(
    (datetime(selected_year + 1, 1, 1) - datetime(selected_year, 1, 1)).days / 7
)
week_choices = [str(week) for week in range(1, num_weeks + 1)]
week_var.set(iso_week_number)
week_dropdown = tk.OptionMenu(window, week_var, *week_choices)
week_dropdown.grid(row=0, column=4, padx=5, sticky="W")


# Create navigation buttons
prev_button = tk.Button(window, text="←", command=prev_item)
prev_button.grid(row=0, column=5, padx=(0, 5), sticky="E")

next_button = tk.Button(window, text="→", command=next_item)
next_button.grid(row=0, column=6, padx=(0, 5), sticky="W")

# Create labels for the dropdown menus
mode_label = tk.Label(window, text="Mode:")
mode_label.grid(row=0, column=0, padx=5, sticky="E")

year_label = tk.Label(window, text="Year:")
year_label.grid(row=0, column=1, padx=5, sticky="E")

month_label = tk.Label(window, text="Month:")
month_label.grid(row=0, column=2, padx=5, sticky="E")

week_label = tk.Label(window, text="Week:")
week_label.grid(row=0, column=3, padx=5, sticky="E")

# Create a larger matplotlib figure and canvas to display the heatmap
fig = plt.Figure(figsize=(10, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=7)

# Create a button to update the heatmap
update_button = tk.Button(window, text="Update Heatmap", command=update_heatmap)
update_button.grid(row=2, column=0, columnspan=7, pady=5)

# Update the heatmap for the initial year
update_heatmap()

# Start the tkinter event loop
window.mainloop()
