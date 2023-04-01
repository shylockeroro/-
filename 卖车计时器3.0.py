import tkinter as tk
from tkinter import messagebox
import time

timestamps = []

def load_timestamps():
    try:
        with open("timestamps.txt", "r") as f:
            for line in f:
                timestamp = line.strip()
                timestamps.append(timestamp)
                add_marker(timestamp)
    except FileNotFoundError:
        pass

def add_timestamp():
    current_time = time.time()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
    timestamps.append(formatted_time)
    add_marker(formatted_time)
    while len(timestamps) > 8:
        timestamps.pop(0)
        canvas.delete("all")
        canvas.create_line(50, 50, 50, 350)
        for t in timestamps:
            add_marker(t)
    save_timestamps()
    check_timestamps()

def check_timestamps():
    two_hours_ago = time.time() - 2*60*60
    thirty_hours_ago = time.time() - 30*60*60
    two_hour_count = 0
    thirty_hour_count = 0
    for timestamp in timestamps:
        timestamp_time = time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
        if timestamp_time > two_hours_ago:
            two_hour_count += 1
        if timestamp_time > thirty_hours_ago:
            thirty_hour_count += 1
    if two_hour_count >= 2 or thirty_hour_count >= 7:
        messagebox.showwarning("警告", "即将超出卖车限制!")

def save_timestamps():
    with open("timestamps.txt", "w") as f:
        for timestamp in timestamps:
            f.write(timestamp + "\n")

def clear_timestamps():
    global timestamps
    timestamps = []
    canvas.delete("all")
    canvas.create_line(50, 50, 50, 350)
    save_timestamps()

def add_marker(timestamp):
    timestamp_time = time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
    first_timestamp_time = time.mktime(time.strptime(timestamps[0], "%Y-%m-%d %H:%M:%S"))
    y = 50 + (timestamp_time - first_timestamp_time) / (30*60*60) * 300
    if y > 350:
        timestamps.pop(0)
        canvas.delete("all")
        canvas.create_line(50, 50, 50, 350)
        for t in timestamps:
            add_marker(t)
    else:
        canvas.create_line(45, y, 55, y)
        text_y = y + 10
        overlapping = True
        while overlapping:
            overlapping = False
            for text_id in canvas.find_withtag("timestamp_text"):
                coords = canvas.coords(text_id)
                if abs(coords[1] - text_y) < 20:
                    text_y += 20
                    overlapping = True
                    break
        canvas.create_text(115, text_y, text=timestamp, tags="timestamp_text")

root = tk.Tk()
root.title("卖车计时器")
add_button = tk.Button(root, text="添加卖车记录", command=add_timestamp)
add_button.pack()
clear_button = tk.Button(root, text="清除记录", command=clear_timestamps)
clear_button.pack()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()
canvas.create_line(50, 50, 50, 350)
load_timestamps()
root.mainloop()