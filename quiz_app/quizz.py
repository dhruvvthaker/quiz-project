import tkinter as tk
from tkinter import messagebox

class QuizUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Multiple Choice Quiz")
        self.master.geometry("750x500")
        self.master.resizable(False, False)

        # Quiz state
        self.current_q = 0
        self.questions = self.placeholder_data()
        self.total_qs = len(self.questions)
        self.user_answers = [None] * self.total_qs
        self.correct_answers = [
            "C. Paris", "B. Mars", "C. William Shakespeare", "D. Pacific", "C. Carbon Dioxide",
            "C. 7", "C. 2", "B. Au", "B. China", "D. Tennis", "C. Leonardo da Vinci", "C. Kidney",
            "C. Mandarin", "B. Piano", "B. Diamond"
        ]

        # Theme
        self.theme = "light"
        self.themes = {
            "light": {
                "bg": "#f7f9fc", "fg": "#222831", "option_fg": "#393e46",
                "button_bg": "#4CAF50", "button_fg": "white", "danger_bg": "#f44336",
                "progress_fg": "#555"
            },
            "dark": {
                "bg": "#2c2c2c", "fg": "#f2f2f2", "option_fg": "#e0e0e0",
                "button_bg": "#00adb5", "button_fg": "white", "danger_bg": "#c62828",
                "progress_fg": "#cccccc"
            }
        }

        # UI Elements
        self.progress_label = tk.Label(master, font=("Helvetica", 12, "italic"))
        self.progress_label.pack(pady=(10, 0))

        self.question_label = tk.Label(master, font=("Helvetica", 16, "bold"),
                                       wraplength=600, justify="center")
        self.question_label.pack(pady=20)

        self.selected_option = tk.StringVar()
        self.options = []
        for _ in range(4):
            rb = tk.Radiobutton(master, variable=self.selected_option, font=("Helvetica", 14),
                                anchor="w", justify="left")
            rb.pack(fill="x", padx=100, pady=2)
            self.options.append(rb)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=30)

        self.prev_button = tk.Button(self.button_frame, text="Previous", font=("Helvetica", 12,"bold"),
                                     width=10, command=self.prev_question)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.next_button = tk.Button(self.button_frame, text="Next", font=("Helvetica", 12, "bold"),
                                     width=10, command=self.next_question)
        self.next_button.grid(row=0, column=1, padx=5)

        self.quit_button = tk.Button(self.button_frame, text="Quit", font=("Helvetica", 12, "bold"),
                                     width=10, command=self.master.quit)
        self.quit_button.grid(row=0, column=2, padx=5)

        self.theme_button = tk.Button(master, text="Toggle Theme", font=("Helvetica", 10, "bold"),
                                      command=self.toggle_theme)
        self.theme_button.pack(pady=5)

        self.apply_theme()
        self.load_question()

    def placeholder_data(self):
        return [
            {"question": "What is the capital of France?",
             "choices": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"]},
            {"question": "Which planet is known as the Red Planet?",
             "choices": ["A. Earth", "B. Mars", "C. Jupiter", "D. Saturn"]},
            {"question": "Who wrote 'Romeo and Juliet'?",
             "choices": ["A. Charles Dickens", "B. Mark Twain", "C. William Shakespeare", "D. Jane Austen"]},
            {"question": "What is the largest ocean on Earth?",
             "choices": ["A. Atlantic", "B. Indian", "C. Arctic", "D. Pacific"]},
            {"question": "Which gas do plants use for photosynthesis?",
             "choices": ["A. Oxygen", "B. Nitrogen", "C. Carbon Dioxide", "D. Hydrogen"]},
            {"question": "How many continents are there?",
             "choices": ["A. 5", "B. 6", "C. 7", "D. 8"]},
            {"question": "Which is the smallest prime number?",
             "choices": ["A. 0", "B. 1", "C. 2", "D. 3"]},
            {"question": "What is the chemical symbol for gold?",
             "choices": ["A. Gd", "B. Au", "C. Ag", "D. Go"]},
            {"question": "Which country is famous for the Great Wall?",
             "choices": ["A. Japan", "B. China", "C. India", "D. Korea"]},
            {"question": "In which sport is the term 'love' used?",
             "choices": ["A. Cricket", "B. Badminton", "C. Football", "D. Tennis"]},
            {"question": "Who painted the Mona Lisa?",
             "choices": ["A. Vincent Van Gogh", "B. Pablo Picasso", "C. Leonardo da Vinci", "D. Michelangelo"]},
            {"question": "Which organ purifies blood in the human body?",
             "choices": ["A. Heart", "B. Liver", "C. Kidney", "D. Lungs"]},
            {"question": "Which language has the most native speakers worldwide?",
             "choices": ["A. English", "B. Hindi", "C. Mandarin", "D. Spanish"]},
            {"question": "Which instrument has black and white keys?",
             "choices": ["A. Guitar", "B. Piano", "C. Violin", "D. Flute"]},
            {"question": "Which is the hardest natural substance on Earth?",
             "choices": ["A. Iron", "B. Diamond", "C. Platinum", "D. Gold"]}
        ]

    def apply_theme(self):
        t = self.themes[self.theme]
        self.master.configure(bg=t["bg"])
        self.progress_label.config(bg=t["bg"], fg=t["progress_fg"])
        self.question_label.config(bg=t["bg"], fg=t["fg"])
        self.button_frame.config(bg=t["bg"])
        self.theme_button.config(bg=t["button_bg"], fg=t["button_fg"])
        self.next_button.config(bg=t["button_bg"], fg=t["button_fg"])
        self.prev_button.config(bg=t["button_bg"], fg=t["button_fg"])
        self.quit_button.config(bg=t["danger_bg"], fg="white")

        for rb in self.options:
            rb.config(bg=t["bg"], fg=t["option_fg"], selectcolor=t["bg"], activebackground=t["bg"])

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()

    def load_question(self):
        q = self.questions[self.current_q]
        self.progress_label.config(text=f"Question {self.current_q + 1} of {self.total_qs}")
        self.question_label.config(text=q["question"])
        self.selected_option.set(self.user_answers[self.current_q])

        for i in range(4):
            self.options[i].config(text=q["choices"][i], value=q["choices"][i])

        self.prev_button.config(state=tk.NORMAL if self.current_q > 0 else tk.DISABLED)

    def save_answer(self):
        self.user_answers[self.current_q] = self.selected_option.get()

    def next_question(self):
        if not self.selected_option.get():
            messagebox.showwarning("Warning", "Please select an option before proceeding.")
            return

        self.save_answer()
        if self.current_q < self.total_qs - 1:
            self.current_q += 1
            self.load_question()
        else:
            self.show_result()

    def prev_question(self):
        self.save_answer()
        if self.current_q > 0:
            self.current_q -= 1
            self.load_question()

    def show_result(self):
        correct = 0
        self.clear_screen()

        # Title
        title = tk.Label(self.master, text="Quiz Completed", font=("Helvetica", 20, "bold"),
                         bg=self.themes[self.theme]["bg"], fg=self.themes[self.theme]["fg"])
        title.pack(pady=10)

        # Canvas + Scrollbar
        canvas = tk.Canvas(self.master, bg=self.themes[self.theme]["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.themes[self.theme]["bg"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        for i in range(self.total_qs):
            q = self.questions[i]
            user_ans = self.user_answers[i]
            correct_ans = self.correct_answers[i]
            is_correct = user_ans == correct_ans

            if is_correct:
                correct += 1

            result_text = (
                f"{i + 1}. {q['question']}\n"
                f"Your answer: {user_ans or 'No answer'}\n"
                f"Correct answer: {correct_ans} {'✅' if is_correct else '❌'}\n"
            )

            label = tk.Label(
                scroll_frame,
                text=result_text,
                font=("Helvetica", 12),
                justify="left",
                anchor="w",
                wraplength=700,
                bg=self.themes[self.theme]["bg"],
                fg="#008000" if is_correct else "#b00020"
            )
            label.pack(anchor="w", pady=5)

        score_msg = f"\nYou scored {correct} out of {self.total_qs}!"
        score_label = tk.Label(self.master, text=score_msg, font=("Helvetica", 16, "bold"),
                               bg=self.themes[self.theme]["bg"], fg=self.themes[self.theme]["fg"])
        score_label.pack(pady=10)

        exit_btn = tk.Button(self.master, text="Exit", command=self.master.quit,
                             font=("Helvetica", 12), bg="#c62828", fg="white")
        exit_btn.pack(pady=20)

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizUI(root)
    root.mainloop()
