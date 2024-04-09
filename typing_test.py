import time
import tkinter as tk
from tkinter import simpledialog


class TypingTest:
    """A class to manage the typing test logic, including timing, user interaction,
    and score management.

    Attributes:
        display_text_widget (tk.Text): The widget where the text to be typed is displayed.
        input_field_widget (tk.Entry): The widget where the user types the text.
        speed_label_widget (tk.Label): The label displaying the typing speed.
        accuracy_label_widget (tk.Label): The label displaying the typing accuracy.
        timer_label_widget (tk.Label): The label displaying the remaining time.
        score_manager (ScoreManager): An instance of ScoreManager to manage high scores.
        start_time (float): The epoch timestamp of when the test starts.
        end_time (float): The epoch timestamp of when the test ends.
        timer_update_id (str): The identifier for the scheduled timer update call.
        test_ended (bool): A flag indicating whether the test has ended.
        remaining_time (int): The remaining time for the typing test in seconds.
    """

    def __init__(
        self,
        display_text_widget,
        input_field_widget,
        speed_label_widget,
        accuracy_label_widget,
        timer_label_widget,
        score_manager,
    ):
        """Initializes the TypingTest with the necessary UI widgets and score manager."""
        self.display_text_widget = display_text_widget
        self.input_field_widget = input_field_widget
        self.speed_label_widget = speed_label_widget
        self.accuracy_label_widget = accuracy_label_widget
        self.timer_label_widget = timer_label_widget
        self.score_manager = score_manager
        self.start_time = None
        self.end_time = None
        self.timer_update_id = None
        self.test_ended = False
        self.remaining_time = 60  # Starting time for the timer

    def update_timer(self):
        """Update the timer label and check if the time is up."""
        if self.remaining_time <= 0:
            self.timer_label_widget.config(text="Time's up!")
            self.end_test_programmatically()
        else:
            self.timer_label_widget.config(text=f"Time: {self.remaining_time}")
            self.remaining_time -= 1
            # Schedule the next update. Keep a reference to the after call
            self.timer_update_id = self.display_text_widget.after(
                1000, self.update_timer
            )

    def start_test(self, text):
        """Start the typing test with the given text."""
        text = self.display_text_widget.get('1.0', tk.END).strip()
        if not text:
            print("No text loaded for the test.")
            return  # Exit the method to avoid starting the test without text.

        self.test_ended = False  # Reset the flag for a new test
        self.display_text_widget.config(state=tk.NORMAL)
        self.display_text_widget.delete('1.0', tk.END)
        self.display_text_widget.insert(tk.END, text)
        self.display_text_widget.config(state=tk.DISABLED)
        self.input_field_widget.delete(0, tk.END)
        self.input_field_widget.config(state=tk.NORMAL)
        self.input_field_widget.focus_set()  # Focus on the input field
        self.input_field_widget.bind('<Return>', self.end_test)
        self.start_time = time.time()
        # Schedule the test to end after 60 seconds (60000 milliseconds)
        self.display_text_widget.after(60000, self.end_test_programmatically)

        self.remaining_time = 60  # Reset the timer each time a test starts
        self.update_timer()  # Start the timer

    def end(self):
        """End the typing test and calculate the speed and accuracy."""
        if self.test_ended:  # Check if the test has already ended
            return  # Exit the method to avoid ending the test again

        self.test_ended = True  # Set the flag to indicate the test has ended

        self.end_time = time.time()
        typed_text = self.input_field_widget.get()
        original_text = self.display_text_widget.get('1.0', tk.END).strip()

        calculated_speed = self.calculate_speed(typed_text, original_text)
        calculated_accuracy = self.calculate_accuracy(typed_text, original_text)

        name = None
        while not name:
            name = simpledialog.askstring("Name", "Enter your name:")
            if name is None:  # User cancelled the prompt
                return

        self.score_manager.add_score(name, calculated_speed, calculated_accuracy)

        # Clear the input field
        self.input_field_widget.delete(0, tk.END)

        self.input_field_widget.config(state=tk.DISABLED)

        # Resetting the timer for the next test
        self.remaining_time = 60
        self.timer_label_widget.config(text="Time: 60")  # Visually reset timer
        # Stop the after loop
        self.display_text_widget.after_cancel(self.timer_update_id)

        # Show the high scores after the test ends
        self.show_high_scores()

    def end_test(self, event):
        """End the test when the user presses Enter."""
        self.end()

    def end_test_programmatically(self):
        """End the test programmatically after the time limit is reached."""
        self.end()

    def calculate_speed(self, typed_text):
        """
        Calculates the typing speed in words per minute (WPM).

        Args:
            typed_text (str): The text typed by the user.

        Returns:
            float: The typing speed in WPM.
        """
        elapsed_time = max(
            self.end_time - self.start_time, 1
        )  # Ensure at least 1 second to avoid division by zero
        elapsed_minutes = elapsed_time / 60.0
        word_count = len(typed_text.split())
        wpm = word_count / elapsed_minutes
        self.speed_label_widget.config(text=f'Speed: {wpm:.2f} WPM')
        return wpm

    def calculate_accuracy(self, typed_text, original_text):
        """
        Calculates the accuracy of the typed text compared to the original text.

        Args:
            typed_text (str): The text that was typed by the user.
            original_text (str): The original text to compare against.

        Returns:
            float: The accuracy of the typed text as a percentage.
        """
        # Ensure there is text to compare against
        if not original_text:
            return 0  # No original text to compare to, so accuracy is 0%

        # Calculate matches, accounting for the possibility of extra characters in typed_text
        matches = sum(
            typed_char == original_char
            for typed_char, original_char in zip(typed_text, original_text)
        )
        accuracy = matches / len(original_text) * 100
        self.accuracy_label_widget.config(text=f'Accuracy: {accuracy:.2f} %')
        return accuracy

    def show_high_scores(self):
        """Displays a pop-up window with the high scores formatted as a table."""
        top_scores = self.score_manager.get_top_scores()

        # Create a Toplevel window to display the scores
        scores_window = tk.Toplevel(self.display_text_widget)
        scores_window.title("High Scores")

        # Create header labels for the table
        headers = ['Name', 'Score (WPM)', 'Accuracy (%)', 'Date']
        for column, header in enumerate(headers):
            header_label = tk.Label(
                scores_window, text=header, font=('Helvetica', 10, 'bold')
            )
            header_label.grid(row=0, column=column, padx=10, pady=5, sticky='ew')

        # Create a grid of labels to show each score
        for row, score in enumerate(top_scores, start=1):
            score_labels = [
                tk.Label(scores_window, text=score['name']),
                tk.Label(scores_window, text=f"{score['score']}"),
                tk.Label(scores_window, text=f"{score['accuracy']}%"),
                tk.Label(scores_window, text=score['date']),
            ]
            for column, score_label in enumerate(score_labels):
                score_label.grid(row=row, column=column, padx=10, pady=5, sticky='ew')

        # Create a 'Close' button at the bottom
        ok_button = tk.Button(scores_window, text="OK", command=scores_window.destroy)
        ok_button.grid(row=row + 1, column=0, columnspan=len(headers), pady=10)
