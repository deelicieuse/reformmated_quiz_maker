import tkinter as tk
from tkinter import filedialog, messagebox
import json
import random

class QuizPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Player")
        self.build_ui()
        self.questions= []
        self.score = 0
        self.lives = 3
        self.asked_indices = set()
        self.window_bg = "#ffe0f0"
        self.text_fg = "#8c176a"
        self.button_bg = "#ffb3e6"
        self.apply_theme()

    def apply_theme(self):
        self.root.config(bg=self.window_bg)
        for widget in self.root. winfo_children():
            self._recolor(widget)

    def _recolor(self, widget):
        widget.config(bg=self.window_bg)
        if isinstance(widget, (tk.Label, tk.Button)):
            widget.config(fg=self.text_fg)
        if isinstance(widget, tk.Button):
            widget.config(
                activebackground=self.text_fg,
                activeforeground=self.window_bg
            )
        if hasattr(widget, "winfo_children"):
            for child in widget.winfo_children():
                self._recolor(child)

    def build_ui(self):

        self.intro_frame = tk.Frame(self.root)
        tk.Label(
            self.intro_frame,
            text="ARE YOU READY TO PLAY?",
            font=("Courier", 28, "bold")
        ).pack(pady=20)
        tk.Button(
            self.intro_frame,
            text="LET'S START",
            font=("Courier", 14),
            command=lambda: self.switch_frame(self.file_selection_frame)
        ).pack()
        self.intro_frame.pack(fill="both", expand=True)

        self.file_selection_frame = tk.Frame(self.root)
        tk.Label(
            self.file_selection_frame,
            text="Select JSON Quiz File",
            font=("Courier", 14)
        ).pack(pady=10)
        tk.Button(
            self.file_selection_frame,
            text="Browse...",
            font=("Courier", 12),
            command=self.choose_file
        ).pack()

        self.quiz_frame = tk.Frame(self.root, padx=20, pady=20)
        self.questions_label = tk.Label(
            self.quiz_frame,
            wraplength=500,
            font=("Courier", 12)
        )

        self.lives_label = tk.Label(self.quiz_frame, font=("Courier", 12))
        self.lives_label.pack(pady=0)

        self.header_label = tk.Label(self.quiz_frame, font=("Courier", 12))
        self.header_label.pack(pady=5)

        self.questions_label.pack(pady=10)
        self.answer_buttons = {}
        for key in "abcd":
            button = tk.Button(
            self.quiz_frame,
            width=40,
            font=("Courier", 12),
            command=lambda o=key: self._answer(o)
            )
            button.pack(pady=3)
            self.answer_buttons[key] = button

    def switch_frame(self, frame):
        for child in self.root.winfo_children():
            child.pack_forget()
        frame.pack(fill="both", expand=True)
        self.apply_theme()

    def choose_file(self):
        fp = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All", "*.*")])
        print("Selected file:", fp)
        with open(fp, 'r') as f:
            self.questions = json.load(f)
        print("Loaded queations:", self.questions)
        self.switch_frame(self.quiz_frame)
        self.show_next_question()

    def update_header(self):
        self.lives_label.config(text="♥ " * self.lives)
        self.header_label.config(text=f" Score: {self.score}/{len(self.questions)}")

    def show_next_question(self):
        if len(self.asked_indices) >= len(self.questions) or self.lives <= 0:
            self.finish_quiz()
            return
        while True:
            idx = random.randrange(len(self.questions))
            if idx not in self.asked_indices:
                break
        self.current_index = idx
        self.current_question = self.questions[idx]
        self.questions_label.config(text=self.current_question["question"])
        for key, button in self.answer_buttons.items():
            button.config(text=f"{key.upper()}: {self.current_question['options'][key]['text']}")

        self.update_header()


    def _answer(self, selected_option):
        if selected_option == self.current_question["answer"]:
            messagebox.showinfo("✓", "Correct!")
        else:
            messagebox.showerror("X", "Wrong answer! Try again!")
        if selected_option == self.current_question["answer"]:
            self.score += 1
            self.asked_indices.add(self.current_index)
        else:
            self.lives -= 1

        self.update_header()
        self.show_next_question()


    def finish_quiz(self):
        message = f"Score: {self.score}/{len(self.questions)}"
        if self.lives <= 0:
            message = f"Game Over!\nAnswer was: {self.current_question['answer'].upper()}\n" + message
        again = messagebox.askyesno("Done", message + "\nPlay again? (You can select a different JSON Quiz)")
        if again:
            self.score = 0
            self. lives = 3
            self.asked_indices.clear()
            self.switch_frame(self.file_selection_frame)
        else:
            self.root.quit()

    def run(self):
        self.root.mainloop()