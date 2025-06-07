# Gender Prediction Using Voice Detection

A Python application that records a user's voice, extracts audio features, and predicts their gender using a trained machine learning model. The app features a simple Tkinter GUI for easy interaction.

---

## Features

- Records audio from the microphone for a specified duration  
- Reduces background noise from the recording  
- Extracts voice features such as MFCC and pitch  
- Trains a Random Forest classifier on a voice dataset (`voice.csv`)  
- Predicts gender (male/female) from the recorded voice  
- Visualizes the waveform of the cleaned audio in the GUI  
- Runs audio recording and prediction in a background thread to keep the UI responsive  

---

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AnshulPareek/Gender-prediction-using-voice-detection.git
   cd Gender-prediction-using-voice-detection
   ```

2. Install required dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Make sure you have the dataset file voice.csv in the same directory as the script.

## Usage

Run the main Python script:
    ```
    python gender_prediction.py
    ```
- Enter a file name (without extension) to save the audio recording.
- Enter the duration (in seconds) for how long to record your voice.
- Click Record & Predict to start recording and get the gender prediction.
- The waveform of the cleaned audio will be displayed in the GUI.
- The predicted gender will appear in the application window and console.

## How It Works
Load Dataset: Loads the voice.csv dataset, mapping male/female labels to 0/1.
Train Model: Trains a Random Forest classifier on the dataset.
Record Audio: Records audio using your microphone for the specified duration.
Noise Reduction: Applies noise reduction to the recorded audio file.
Feature Extraction: Extracts MFCC and pitch features from the cleaned audio.
Prediction: Uses the trained model to predict gender from extracted features.
Visualization: Displays the waveform of the cleaned audio in the Tkinter GUI.

##  Dependencies

- Python 3.7+
- numpy
- pandas
- scikit-learn
- matplotlib
- librosa
- sounddevice
- soundfile
- noisereduce
- tkinter (usually included with Python)

## License
This project is licensed under the MIT License - see the https://opensource.org/license/MIT file for details.

## Acknowledgements
- Voice dataset sourced from voice.csv
- Noise reduction inspired by the noisereduce library
- Audio processing done with librosa and sounddevice

Feel free to contribute or report issues!
Created with ❤️ by Anshul Pareek.
