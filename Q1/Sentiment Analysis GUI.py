import tkinter as tk
from tkinter import ttk
from transformers import pipeline
import time


# Decorator for logging actions (How it is linked: Used to log every function call in the application)
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"Action Logged: {func.__name__} was called.")
        return func(*args, **kwargs)

    return wrapper


# Another decorator for timing function execution (How it is linked: Used to measure the time taken for sentiment analysis)
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} executed in {time.time() - start_time:.4f} seconds.")
        return result

    return wrapper


# Encapsulation: GUI class encapsulates the user interface (How it is linked: GUI-specific functionality is encapsulated in this class)
class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sentiment Analysis App with OOP")
        self.geometry("500x350")

        # Input field for user text
        self.label = tk.Label(self, text="Enter text for sentiment analysis:")
        self.label.pack(pady=10)

        self.text_input = tk.Text(self, height=5, width=50)
        self.text_input.pack(pady=10)

        # Analyze button
        self.analyze_button = tk.Button(self, text="Analyze Sentiment", command=self.analyze_sentiment)
        self.analyze_button.pack(pady=10)

        # Label to display the result
        self.result_label = tk.Label(self, text="Sentiment result will appear here", wraplength=400)
        self.result_label.pack(pady=20)

    @log_action  # Decorator logs when the method is called
    def analyze_sentiment(self):
        # This method will be overridden in the MainApp class
        pass

    @log_action  # Decorator logs when the method is called
    def display_result(self, result):
        self.result_label.config(text=f"Sentiment: {result}")


# SentimentAnalysis class for handling the model (How it is linked: Encapsulation of the BERT model and its analysis logic)
class SentimentAnalysis:
    def __init__(self):
        self.model = None  # Placeholder for the BERT model

    @log_action
    @timer  # Decorator to log the time taken to load the model
    def load_model(self):
        # Encapsulation: Loading the BERT model
        self.model = pipeline("sentiment-analysis")
        print("BERT model loaded successfully.")

    @log_action
    @timer  # Decorator to log the time taken for sentiment analysis
    def analyze(self, text):
        # Encapsulation: The model performs sentiment analysis on the text
        result = self.model(text)
        return result[0]['label']


# Polymorphism: MainApp class uses multiple inheritance (How it is linked: Inherits from both GUI and SentimentAnalysis classes)
class MainApp(GUI, SentimentAnalysis):
    def __init__(self):
        # Call constructors from both parent classes
        GUI.__init__(self)
        SentimentAnalysis.__init__(self)

        # Load the sentiment analysis model on initialization
        self.load_model()

    # Method overriding: Overriding the analyze_sentiment method from GUI class (How it is linked: Providing specific functionality in MainApp)
    @log_action  # Logs when the overridden method is called
    def analyze_sentiment(self):
        # Get text from the input field
        user_input = self.text_input.get("1.0", "end-1c").strip()
        if not user_input:
            self.display_result("Please enter some text.")
            return

        # Analyze the sentiment of the text using the BERT model
        result = self.analyze(user_input)

        # Display the result
        self.display_result(result)


# Run the application
if __name__ == "__main__":
    app = MainApp()  # Polymorphism: MainApp inherits behavior from both GUI and SentimentAnalysis
    app.mainloop()
