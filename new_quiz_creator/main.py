import tkinter as tk
from class_quiz_creator import QuizCreatorApp

if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.config(padx=15, pady=15)
    quiz_app = QuizCreatorApp(main_window)
    main_window.mainloop()