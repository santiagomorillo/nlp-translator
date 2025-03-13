# Flask Translation App

This project is a Flask application that provides a translation service from English to French using a pre-trained model. The application serves a simple web interface where users can input English text and receive the French translation.

## Project Structure

```
flask-translation-app
├── app.py               # Main application file containing the Flask app and translation logic
├── Dockerfile           # Dockerfile to containerize the application
├── requirements.txt     # Python dependencies required for the application
└── README.md            # Documentation for the project
```

## Requirements

Before running the application, ensure you have Docker installed on your machine.

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd flask-translation-app
   ```

2. Build the Docker image:

   ```
   docker build -t flask-translation-app .
   ```

## Running the Application

To run the application, use the following command:

```
docker run -p 80:80 flask-translation-app
```

You can then access the application by navigating to `http://localhost:80` in your web browser.

## Usage

1. Enter the English text you want to translate in the provided text area.
2. Click the "Obtener Traducción" button to receive the French translation.

