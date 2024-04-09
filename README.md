# Typing Test Application

A simple yet effective typing test application built with Python's Tkinter. It allows users to measure their typing speed in words per minute (WPM) and accuracy percentage. The application provides randomly generated sentences for typing tests and supports translating the text into Spanish for multilingual typing practice.

## Features

- **Typing Speed Measurement**: Calculate your typing speed in WPM and see how fast you can type.
- **Accuracy Calculation**: Measure your typing accuracy to see how precisely you type.
- **Random Text Generation**: Practice typing with new, randomly generated sentences every time.
- **Text Translation**: Switch the typing test text to Spanish for a multilingual typing experience.
- **High Score Tracking**: Keep track of your top typing speeds and accuracies.

## Installation

This application requires Python 3.6+ and the following Python libraries:

- `tkinter` for the GUI.
- `requests` for fetching data from APIs.
- `googletrans==4.0.0-rc1` for translating text.
- `wonderwords` for generating random sentences.

To set up the application, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/BAXTOR95/typing-test.git
   ```

2. Navigate to the cloned repository:

   ```bash
   cd typing-test
   ```

3. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To start the application, run:

```bash
python main.py
```

Follow the on-screen instructions to start the typing test. You can press the "Start" button to begin the test with the displayed text, use the "New Text" button to fetch a new sentence, or use the "Translate" button to translate the text to Spanish.

## Contributing

Contributions are welcome! If you have suggestions for improving the application, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The `googletrans` library for enabling text translation features.
- The `wonderwords` library for generating random sentences for typing tests.
