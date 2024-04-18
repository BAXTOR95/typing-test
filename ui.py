import tkinter as tk
import threading


class TypingTestUI(tk.Frame):
    """
    A user interface for a typing test application. It handles the layout and
    interaction of UI elements like text display, input field, and buttons.

    Attributes:
        master (tk.Tk): The root window.
        text_manager (object): An instance of TextManager for text generation and translation.
    """

    def __init__(self, master=None):
        """
        Initializes the TypingTestUI frame.

        Args:
            master (tk.Tk): The root window.
        """
        super().__init__(master)
        self.master = master
        self.text_manager = None  # This will be set from outside
        self.pack()
        self.create_widgets()
        self.fetch_new_text_thread()

    def create_widgets(self):
        """
        Creates and arranges the widgets within the frame.
        """
        self.master.title('Typing Speed Test')

        # Create the grid layout for the widgets
        # Set equal weight for the columns that will contain buttons and labels
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)

        # Set equal weight for the row that will expand to fill space
        self.grid_rowconfigure(1, weight=1)

        # Creating UI elements
        self.setup_labels()
        self.setup_text_display()
        self.setup_input_field()
        self.setup_buttons()

    def setup_labels(self):
        """Sets up the labels for status, speed, accuracy, and timer at the top row."""
        self.speed_label = tk.Label(self, text='Speed: - WPM')
        self.accuracy_label = tk.Label(self, text='Accuracy: - %')
        self.timer_label = tk.Label(self, text="Time: 60")
        self.status_label = tk.Label(self, text="")

        self.speed_label.grid(row=0, column=0, sticky='ew', padx=5)
        self.accuracy_label.grid(row=0, column=1, sticky='ew', padx=5)
        self.timer_label.grid(row=0, column=2, sticky='ew', padx=5)
        self.status_label.grid(row=2, column=0, columnspan=3, sticky='ew', padx=5)

    def setup_text_display(self):
        """Configures the text display area."""
        self.text_display = tk.Text(
            self, height=10, width=50, wrap=tk.WORD, state=tk.DISABLED
        )
        self.text_display.grid(
            row=1, column=0, columnspan=3, padx=10, pady=5, sticky='ew'
        )

    def setup_input_field(self):
        """Sets up the typing input field."""
        self.input_field = tk.Entry(self, state=tk.DISABLED)
        self.input_field.grid(
            row=3, column=0, columnspan=3, padx=10, pady=5, sticky='ew'
        )

    def setup_buttons(self):
        """Creates the Start, New Text, and Translate buttons."""
        self.start_button = tk.Button(self, text='Start', command=self.set_start_test_callback)
        self.new_text_button = tk.Button(
            self, text="New Text", command=self.fetch_new_text_thread
        )
        self.translate_button = tk.Button(
            self, text="Translate", command=self.translate_text_thread
        )

        self.start_button.grid(row=4, column=0, pady=5, sticky='ew', padx=5)
        self.new_text_button.grid(row=4, column=1, pady=5, sticky='ew', padx=5)
        self.translate_button.grid(row=4, column=2, pady=5, sticky='ew', padx=5)

    def set_start_test_callback(self, start_test_callback):
        """
        Set the callback function for the start test functionality.

        Parameters:
        - start_test_callback: The callback function to be set.

        Returns:
        None
        """
        self.start_test_callback = start_test_callback
        # Update the start button command to use the new callback
        self.start_button.config(command=self.trigger_start_test)

    def trigger_start_test(self):
        """
        This method gets called when the start button is pressed.
        It triggers the start_test_callback with the current text as an argument.
        """
        if self.start_test_callback:
            self.start_test_callback(
                self.text_display.get('1.0', 'end-1c')
            )  # Pass the current text as an argument

    def fetch_new_text(self):
        """
        Fetches new text from the text manager and updates the text display.

        If the text manager is available, it creates a new paragraph of text and updates the text display with the new text.
        If successful, the text display is enabled, cleared, and populated with the new text.
        If unsuccessful, an error message is shown.

        Args:
            None

        Returns:
            None
        """
        if self.text_manager:
            self.status_label.config(text="Loading text...")
            new_text = self.text_manager.create_paragraph()
            if new_text:
                self.text_display.config(state=tk.NORMAL)
                self.text_display.delete('1.0', tk.END)
                self.text_display.insert(tk.END, new_text)
                self.text_display.config(state=tk.DISABLED)
            else:
                self.show_error("Failed to fetch new text.")
        self.status_label.config(text="")

    def translate_text(self):
        """
        Translates the current text displayed in the text display widget.

        If a text manager is available, it retrieves the current text from the text display widget,
        strips any leading or trailing whitespace, and passes it to the text manager's `translate_paragraph` method.
        The translated text is then displayed in the text display widget.

        If the translation is successful, the text display widget is enabled, cleared, and updated with the translated text.
        If the translation fails, an error message is shown.

        Note: This method assumes the existence of a `text_manager` attribute and a `status_label` attribute.

        Returns:
            None
        """
        if self.text_manager:
            self.status_label.config(text="Translating new text...")
            current_text = self.text_display.get('1.0', tk.END).strip()
            translated_text = self.text_manager.translate_paragraph(current_text)
            if translated_text:
                self.text_display.config(state=tk.NORMAL)
                self.text_display.delete('1.0', tk.END)
                self.text_display.insert(tk.END, translated_text)
                self.text_display.config(state=tk.DISABLED)
            else:
                self.show_error("Failed to translate text.")
        self.status_label.config(text="")

    def fetch_new_text_thread(self):
        """
        Starts a new thread to fetch new text.
        """
        threading.Thread(target=self.fetch_new_text).start()

    def translate_text_thread(self):
        """
        Starts a new thread to execute the translate_text method.
        """
        threading.Thread(target=self.translate_text).start()

    def show_error(self, message):
        """
        Display a pop-up window to show an error message.

        Parameters:
        - message (str): The error message to be displayed.

        Returns:
        - None
        """
        error_window = tk.Toplevel(self)
        error_window.title("Error")
        error_label = tk.Label(error_window, text=message)
        error_label.pack(padx=10, pady=10)
        ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
        ok_button.pack(pady=10)

    def initialize_typing_test(self):
        """
        Initializes the typing test by fetching new text from the text manager.
        This method will be called after the text_manager is set.
        """
        self.fetch_new_text_thread()
        
