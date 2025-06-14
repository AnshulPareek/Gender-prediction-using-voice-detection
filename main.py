import tkinter as tk
import threading
import sounddevice as sd
import librosa
import soundfile as sf
import numpy as np
import noisereduce as nr
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# === Reads the voice dataset csv file ===
def load_dataset():
    df = pd.read_csv("voice.csv")
    df["label"] = df["label"].map({"male": 0, "female": 1})
    X = df.drop(columns=["label"]) #stores all columns except label in x variable
    Y = df["label"] #stores label column in y variable
    return X, Y

# === Trains the model based on voice data ===
def train_model(X, Y):
    print("✅ Starting training...")
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("✅ Training complete!")
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"✅ Model Accuracy: {accuracy * 100:.2f}%\n")
    return model

# === Records the audio of the user & saves it to a file
def record_audio(file_path, duration, sample_rate=44100):
    print("🎙️ Recording... Speak now!")
    time.sleep(1)  
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    sf.write(file_path, audio_data, sample_rate)
    print(f"🎵 Recording saved at\n{file_path}")
    return file_path

# === reduces the noise from saved .wav file
def reduce_noise(file_path):
    time.sleep(1)
    print("\n🔊 Reducing background noise...")
    y, sr = sf.read(file_path)
    y_denoised = nr.reduce_noise(y=y, sr=sr, stationary=True)
    sf.write(file_path, y_denoised, sr)
    time.sleep(1)
    print(f"✅ Noise reduction complete.")
    return file_path, y_denoised, sr

# === extract features like mfcc and pitch from the denoised audio ===
def extract_features(y, sr):
    print("\n🗣️ Extracting Voice features...")
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=19)
    avg_mfcc = np.mean(mfcc, axis=1)
    
    pitch = librosa.yin(y=y, fmax=600, fmin=50, sr=sr)
    avg_pitch = np.median(pitch)
    
    features = np.append(avg_mfcc, avg_pitch)
    return features.reshape(1, -1)

# === plot the waveform of the recorded noise ===
def plot_waveform(y, sr, container):
    for widget in container.winfo_children():
        widget.destroy()
    
    fig = Figure(figsize=(6, 2.5), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(np.linspace(0, len(y)/sr, len(y)), y, color='blue')
    plot.set_title("Waveform")
    plot.set_xlabel("Time (s)")
    plot.set_ylabel("Amplitude")

    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Loads Voice dataset and trains AI model
X, Y = load_dataset()
model = train_model(X, Y)
feature_names = X.columns

def main():
    print("Hey there! I'm going to help you record\nyour voice and predict the gender. Ready?")
    def run_prediction():
        predict_button.config(state=tk.DISABLED) #To prevent user from giving multiple input at same time

        file_name = str(file_name_entry.get().strip())
        duration = int(duration_entry.get().strip())
        file_path = f"C:\\{file_name}.wav"

        # Check if the duration is positive
        if duration <= 0:
            tk.messagebox.showerror("Input Error", "Duration should be a positive number.")
            return

        # Record Audio
        bottom = tk.Label(root, text="🎙️Recording... Speak now!", font=("Arial", 16), fg="blue")
        bottom.pack()
        record_audio(file_path, duration)

        # Reduces Noise
        bottom.config(text="🔊 Reducing background noise...")
        file_path, cleaned_audio, sr = reduce_noise(file_path)

        # Waveform Plotting
        plot_waveform(cleaned_audio, sr, waveform_frame)

        # Extracts Voice Features
        bottom.config(text="🧠 Extracting voice features...")
        features = extract_features(cleaned_audio, sr)
        bottom.config(text="📚 Loading dataset and training model...")

        # Make Prediction using Model
        features_df = pd.DataFrame(features, columns=feature_names)
        prediction = model.predict(features_df)[0]
        gender = "Female" if prediction == 1 else "Male"

        # Print the result
        bottom.config(text="✅ Gender prediction complete!",font=("Helvetica",20))
        prediction_label = tk.Label(root, text=f"🎤 Predicted Gender: {gender}", font=("Georgia", 30, "bold"), fg="green")
        prediction_label.pack()
        print(f"🎤 Predicted Gender: {gender}")
        
        predict_button.config(state=tk.NORMAL) #Enables the option

    def start_thread():
        threading.Thread(target=run_prediction, daemon=True).start()

    # --- GUI Setup ---
    root = tk.Tk()
    root.title("Gender Prediction using Voice detection")
    root.geometry("800x720")
    root.resizable(False,False)
    tk.Label(root,text="👨Gender Predictor👩",font=("Georgia",48,"bold"),fg='black').pack(pady=25)

    tk.Label(root, text="File Name:").pack()
    file_name_entry = tk.Entry(root, width=30)
    file_name_entry.pack()

    tk.Label(root, text="Duration (seconds):").pack()
    duration_entry = tk.Entry(root, width=10)
    duration_entry.pack()

    predict_button = tk.Button(root, text="🎤 Record & Predict", command=start_thread)
    predict_button.pack(pady=15)

    global waveform_frame
    waveform_frame = tk.Frame(root)
    waveform_frame.pack(pady=20)
    root.mainloop()
main()
