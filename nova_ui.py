import tkinter as tk
from tkinter import scrolledtext, filedialog
import subprocess
import json
import datetime

MODEL = "deepseek-coder"
LOG_PATH = "../core/memory.jsonl"

def log_interaction(prompt, response):
    with open(LOG_PATH, "a") as log:
        log.write(json.dumps({
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt": prompt,
            "response": response
        }) + "\n")

def query_model(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL],
            input=prompt.encode(),
            capture_output=True,
            timeout=60
        )
        response = result.stdout.decode(errors="ignore")
        log_interaction(prompt, response)
        return response
    except Exception as e:
        return f"[Error] {str(e)}"

def save_output(text):
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f:
        f.write(text)
        f.close()

def run_prompt():
    prompt = prompt_input.get("1.0", tk.END).strip()
    if not prompt:
        return
    response = query_model(prompt)
    response_output.config(state='normal')
    response_output.delete("1.0", tk.END)
    response_output.insert(tk.END, response)
    response_output.config(state='disabled')

# Theme Colors
bg_color = "#1a1a1a"
fg_color = "#ff69b4"  # Hot Pink
entry_bg = "#2b2b2b"
font_main = ("Helvetica", 12)
font_header = ("Helvetica", 18, "bold")

app = tk.Tk()
app.title("NovaCipher: Your LLM Recovery Assistant")
app.geometry("860x620")
app.configure(bg=bg_color)

# Header
header = tk.Label(app, text="NovaCipher LLM UI", font=font_header, fg=fg_color, bg=bg_color)
header.pack(pady=10)

# Prompt Input Frame
prompt_frame = tk.Frame(app, bg=bg_color)
prompt_frame.pack(pady=5)
prompt_label = tk.Label(prompt_frame, text="Your Prompt:", fg=fg_color, bg=bg_color, font=font_main)
prompt_label.pack(anchor='w')
prompt_input = scrolledtext.ScrolledText(prompt_frame, height=6, width=100, bg=entry_bg, fg="white", insertbackground=fg_color)
prompt_input.pack()

# Button Frame
button_frame = tk.Frame(app, bg=bg_color)
button_frame.pack(pady=8)
run_button = tk.Button(button_frame, text="Run Prompt", command=run_prompt, fg=bg_color, bg=fg_color, font=font_main)
run_button.grid(row=0, column=0, padx=10)
save_button = tk.Button(button_frame, text="Save Output", command=lambda: save_output(response_output.get("1.0", tk.END)), fg=bg_color, bg=fg_color, font=font_main)
save_button.grid(row=0, column=1, padx=10)

# Response Output Frame
response_frame = tk.Frame(app, bg=bg_color)
response_frame.pack(pady=5)
response_label = tk.Label(response_frame, text="Model Response:", fg=fg_color, bg=bg_color, font=font_main)
response_label.pack(anchor='w')
response_output = scrolledtext.ScrolledText(response_frame, height=18, width=100, state='disabled', bg=entry_bg, fg="white", insertbackground=fg_color)
response_output.pack()

app.mainloop()

