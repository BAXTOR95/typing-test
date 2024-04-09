import tkinter as tk
from ui import TypingTestUI
from typing_test import TypingTest
from text_manager import TextManager
from score_manager import ScoreManager


def main():
    root = tk.Tk()
    app = TypingTestUI(master=root)
    text_manager = TextManager()
    score_manager = ScoreManager()

    # Pass the text and score manager to the app
    app.text_manager = text_manager
    app.score_manager = score_manager

    # Now that text_manager is set, initialize the typing test
    app.initialize_typing_test()

    # Create a typing test object
    typing_test = TypingTest(
        app.text_display,
        app.input_field,
        app.speed_label,
        app.accuracy_label,
        app.timer_label,
        score_manager,
    )

    app.set_start_test_callback(typing_test.start_test)

    app.mainloop()


if __name__ == "__main__":
    main()
