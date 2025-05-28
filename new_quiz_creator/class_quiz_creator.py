
class QuizCreatorApp:
    def __init__(self, root_window):
        self.root_window = root_window
        self.root_window.title("Quiz Creator")
        self.root_window.config(bg="#f0f4f8")
        self.option_entries = {}
        self.option_image_paths = {}
        self.option_image_labels = {}
        self.correct_answer_variable = tk.StringVar(value="a")
        self.option_keys = ["a", "b", "c", "d"]
        self.questions_list = []
        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(
            self.root_window,
            padx=10,
            pady=10,
            bg="#f0f4f8")
        main_frame.grid(row=0, column=0)

        question_label = tk.Label(
            main_frame,
            text="Enter your question:",
            font=("Helvetica", 12, "bold"),
            bg="#f0f4f8"
        )
        question_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.question_entry = tk.Entry(main_frame, width=60)
        self.question_entry.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=5)

        options_frame = tk.LabelFrame(
            main_frame,
            text="Options",
            padx=10,
            pady=10,
            borderwidth=2,
            relief="groove",
            font=("Helvetica", 11, "bold"),
            bg="#f0f4f8"
        )
        options_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=15)
        options_frame.configure(bg="#f0f4f8")

        for index, option_key in enumerate(self.option_keys):
            option_label = tk.Label(
                options_frame,
                text=f"Option {option_key.upper()} Text:",
                font=("Helvetica", 10),
                bg="#f0f4f8"
            )
            option_label.grid(row=index, column=0, sticky="w", padx=5, pady=5)

            option_entry = tk.Entry(options_frame, width=40, font=("Helvetica", 10))
            option_entry.grid(row=index, column=1, padx=5, pady=5)
            self.option_entries[option_key] = option_entry

            image_path = tk.StringVar()
            self.option_image_paths[option_key] = image_path

            image_label = tk.Label(
                options_frame,
                textvariable=image_path,
                fg="grey",
                wraplength=150,
                bg="#f0f4f8"
            )
            image_label.grid(row=index, column=2, sticky="w", padx=5, pady=5)
            self.option_image_labels[option_key] = image_label

            upload_button = tk.Button(
                options_frame,
                text="Upload Image",
                command=lambda key=option_key: self.upload_image(key),
                font=("Helvetica", 10)
            )
            upload_button.grid(row=index, column=3, padx=5, pady=5)

            clear_button = tk.Button(
                options_frame,
                text="Clear",
                command=lambda key=option_key: self.clear_image(key),
                font=("Helvetica", 10)
            )
            clear_button.grid(row=index, column=4, padx=5, pady=5)

        correct_label = tk.Label(
            main_frame,
            text="Correct Answer:",
            font=("Helvetica", 12),
            bg="#f0f4f8"
        )
        correct_label.grid(row=2, column=0, sticky="w", padx=5, pady=10)

        correct_dropdown = tk.OptionMenu(
            main_frame,
            self.correct_answer_variable,
            *self.option_keys
        )
        correct_dropdown.config(font=("Helvetica", 10))
        correct_dropdown.grid(row=2, column=1, sticky="w", padx=5, pady=10)

        button_frame = tk.Frame(main_frame, bg="#f0f4f8")
        button_frame.grid(row=3, column=0, columnspan=4, pady=15)

        add_question_button = tk.Button(
            button_frame,
            text="Save Question",
            command=self.save_question,
            font=("Helvetica", 10)
        )
        add_question_button.pack(side="left", padx=10)

        export_button = tk.Button(
            button_frame,
            text="Export Quiz",
            command=self.save_all_questions,
            font=("Helvetica", 10)
        )
        export_button.pack(side="left", padx=10)

        clear_form_button = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            font=("Helvetica", 10)
        )
        clear_form_button.pack(side="left", padx=10)

        exit_button = tk.Button(
            button_frame,
            text="Exit",
            command=self.root_window.quit,
            font=("Helvetica", 10)
        )
        exit_button.pack(side="left", padx=10)

        self.questions_count_label = tk.Label(
            main_frame,
            text=f"Questions in current quiz: {len(self.questions_list)}",
            font=("Helvetica", 10),
            bg="#f0f4f8"
        )
        self.questions_count_label.grid(row=4, column=0, columnspan=4, pady=5)

    def save_question(self):

        question_text = self.question_entry.get().strip()
        if not question_text:
            messagebox.showerror("Error", "Question cannot be empty!")
            return

        options_dict = {}
        for key in self.option_keys:
            option_text = self.option_entries[key].get().strip()
            if not option_text:
                messagebox.showerror("Error", f"Option {key.upper()} text cannot be empty!")
                return

            image_path = self.option_image_paths[key].get()
            if image_path == "":
                image_path = None

            options_dict[key] = {
                "text": option_text,
                "image": image_path
            }

        single_question_data = {
            "question": question_text,
            "options": options_dict,
            "answer": self.correct_answer_variable.get()
        }

        self.questions_list.append(single_question_data)
        self.update_questions_count()
        messagebox.showinfo("Sucesss", "Question added to quiz!")
        self.clear_form()

    def save_all_questions(self):
        if not self.questions_list:
            messagebox.showinfo("Info", "No questions to save!")

        file_path = filedialog.asksaveasfilename(
            title="Save Quiz File",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            initialfile="quiz_data.json"
        )

        if not file_path:
            return

        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        existing_question = json.load(file)
                        if not isinstance(existing_question, list):
                            raise ValueError("Existing file does not contain a list")
                        combined_questions = existing_questions + self.questions_list
                    except json.JSONDecodeError:
                        combined_questions = []
            else:
                combined_questions = []

            combined_questions = self.questions_list

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(combined_questions, file, indent=4)

            messagebox.showinfo("Success", f"Question saved successfully to\n{file_path}")
            self.questions_list = []
            self.update_questions_count()

        except Exception as error:
            messagebox.showerror("Save Error", f"An error occured while saving: \n{error}")

    def clear_form(self):
        self.question_entry.delete(0, tk.END)
        for key in self.option_keys:
            self.option_entries[key].delete(0, tk.END)
            self.clear_image(key)
        self.correct_answer_variable.set(self.option_keys[0])
        self.question_entry.focus_set()

    def upload_image(self, option_key):
        file_path = filedialog.askopenfilename(
            title=f"Select Image for Option {option_key.upper()}",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif"), ("All Files", "*.*")]
        )

        if file_path:
            file_name = os.path.basename(file_path)
            self.option_image_paths[option_key].set(file_path)
            self.option_image_labels[option_key].config(text=file_name)
            messagebox.showinfo("Image Selected", f"Image '{file_name}' selected for Option {option_key.upper()}.")
        else:
            self.option_image_paths[option_key].set("")
            self.option_image_labels[option_key].config(text="")

    def clear_image(self, option_key):
        self.option_image_paths[option_key].set("")
        self.option_image_labels[option_key].config(text="")

    def update_questions_count(self):
        if hasattr(self, 'questions_count_label'):
            try:
                question_count = len(self.questions_list)
                self.questions_count_label.config(text=f"Questions in current quiz: {len(self.questions_list)}")
            except Exception as e:
                print(f"Error in update_questions_count: {e}")
