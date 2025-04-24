
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse

# Theme
bg_color = "#1a1a1a"
fg_color = "#ff69b4"
entry_bg = "#2b2b2b"
font_main = ("Helvetica", 12)
font_header = ("Helvetica", 18, "bold")

scraped_data = []

# Scraper logic
def scrape_and_store():
    urls = url_input.get("1.0", tk.END).strip().splitlines()
    tag_text = tags_entry.get().strip()
    tags = [tag.strip() for tag in tag_text.split(",") if tag.strip()]

    for url in urls:
        try:
            res = requests.get(url, timeout=15)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)

            domain = urlparse(url).netloc.replace(".", "_")
            scraped_data.append({
                "source": url,
                "domain": domain,
                "content": text,
                "tags": tags
            })
        except Exception as e:
            messagebox.showerror("Scrape Error", f"Failed to scrape {url}\n{e}")

    update_preview()

def update_preview():
    preview_box.config(state='normal')
    preview_box.delete("1.0", tk.END)
    for item in scraped_data:
        preview_box.insert(tk.END, f"{item['source']}\nTags: {', '.join(item['tags'])}\nPreview: {item['content'][:300]}...\n\n")
    preview_box.config(state='disabled')

def save_as_json():
    if not scraped_data:
        messagebox.showwarning("No Data", "Scrape some URLs first!")
        return
    file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(scraped_data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Saved", f"Training JSON saved to:\n{file}")

# UI
app = tk.Tk()
app.title("NovaScrape – LLM Training Harvester")
app.geometry("900x620")
app.configure(bg=bg_color)

# Header
header = tk.Label(app, text="NovaScrape", font=font_header, fg=fg_color, bg=bg_color)
header.pack(pady=10)

# URL Input
url_label = tk.Label(app, text="Enter URLs (one per line):", fg=fg_color, bg=bg_color, font=font_main)
url_label.pack(anchor='w', padx=10)
url_input = scrolledtext.ScrolledText(app, height=6, width=100, bg=entry_bg, fg="white", insertbackground=fg_color)
url_input.pack(padx=10)

# Tags Input
tag_frame = tk.Frame(app, bg=bg_color)
tag_frame.pack(pady=10)
tags_label = tk.Label(tag_frame, text="Tags (comma-separated):", fg=fg_color, bg=bg_color, font=font_main)
tags_label.pack(side='left')
tags_entry = tk.Entry(tag_frame, width=50, bg=entry_bg, fg="white", insertbackground=fg_color)
tags_entry.pack(side='left', padx=10)

# Buttons
btn_frame = tk.Frame(app, bg=bg_color)
btn_frame.pack(pady=10)
run_btn = tk.Button(btn_frame, text="Scrape URLs", command=scrape_and_store, bg=fg_color, fg=bg_color, font=font_main)
run_btn.grid(row=0, column=0, padx=10)
save_btn = tk.Button(btn_frame, text="Save as JSON", command=save_as_json, bg=fg_color, fg=bg_color, font=font_main)
save_btn.grid(row=0, column=1, padx=10)

# Preview Box
preview_label = tk.Label(app, text="Preview (first 300 chars):", fg=fg_color, bg=bg_color, font=font_main)
preview_label.pack(anchor='w', padx=10)
preview_box = scrolledtext.ScrolledText(app, height=15, width=100, state='disabled', bg=entry_bg, fg="white")
preview_box.pack(padx=10, pady=(0, 10))

app.mainloop()
