# Whisper Transcription Tool - AI WorkFlow 1.0

## 📖 Table of Contents

- [Why Should You Use This Tool?](#why-should-you-use-this-tool)
- [Installation Guide](#installation-guide)
- [Getting the Code from GitHub](#getting-the-code-from-github)
- [How It Works](#how-the-tool-works-behind-the-scenes)
- [How to Use](#how-to-use-the-tool)
- [Example Transcription Flows](#example-transcription-flows)
- [Demo Video](#demo-video)
- [Features](#features)
- [Troubleshooting & FAQs](#troubleshooting--faqs)
- [Extra Tips](#extra-tips)
- [Contributing](#contributing)
- [License](#license)

---

## 💡 Why Should You Use This Tool?

Transcription services can be **expensive** and often come with **limitations, subscriptions, or intrusive bots** that join your meetings. Instead of dealing with all that, here’s a **simple and free way** to transcribe your audio or video files!

### 🎤 A Smarter, Cost-Free Alternative

Instead of relying on costly tools, you can use **Windows' built-in recording tools** like Snipping Tool to record your meetings or videos **without any intrusive bots**. Once you have your recording, just **run it through this tool locally**, and it will transcribe everything for you—**for free!**

### 🎯 Choose Your Own Model

You can pick different **Whisper audio transcription models** depending on how accurate you want the transcription to be and how much time you have. **Higher accuracy = longer processing time.** [Check out the Whisperify documentation](https://github.com/openai/whisper) to see the pros and cons of each model.

---

## 🛠️ Installation Guide

### 1️⃣ Install Git

If you don’t have Git installed, follow these steps:
- **Windows**: Download and install [Git for Windows](https://git-scm.com/downloads)
- **Mac**: Install Git via Homebrew:
  ```sh
  brew install git
  ```
- **Linux**: Install Git using your package manager:
  ```sh
  sudo apt install git  # Debian/Ubuntu
  sudo yum install git  # RHEL/CentOS
  ```

To verify Git is installed, run:
```sh
git --version
```

### 2 Install ffmpeg

1. Download **ffmpeg** from [videohelp.com](https://www.videohelp.com/software/ffmpeg)
2. Extract The Downloaded Folder and navigate till bin folder
   ```sh
   example : C:\Users\sande\Downloads\ffmpeg-7.1-full_build\ffmpeg-7.1-full_build\bin
   ```
3. Add the copied path into the environment variable [video guide](https://youtu.be/GYdhqmy_Nt8?si=K6FfdxV5PsrWCKNA)
4. Once installed ,verify the installation by running:
   ```sh
   ffmpeg -version
   ```


### 3 Install Python

1. Download **Python** from [python.org](https://www.python.org/)
2. **Important:** During installation, check the box that says **“Add Python to PATH”**
3. Once installed, verify the installation by running:
   ```sh
   python --version
   ```
   You should see output like `Python 3.x.x`.

### 4 Install an IDE (Optional, Recommended for Beginners)

If you're not familiar with running Python scripts, an **IDE (Integrated Development Environment)** makes things easier:

- **[Visual Studio Code (VS Code)](https://code.visualstudio.com/)** – Recommended!
- **[PyCharm](https://www.jetbrains.com/pycharm/)**

👉 **If using VS Code:** Install the Python extension from the Extensions tab.

### 5 Set Up a Virtual Environment (Recommended)

To keep dependencies isolated and avoid conflicts, **create a virtual environment:**

```sh
python -m venv whisper_env
```

Activate the virtual environment:
- **Windows:** `whisper_env\Scripts\activate`
- **Mac/Linux:** `source whisper_env/bin/activate`

### 6 Install Dependencies

After activating the virtual environment, install the required dependencies:

```sh
pip install -r requirements.txt
```

### 7 Verify the Installation

To confirm everything is installed correctly, run:

```sh
python -c "import whisper; print('Whisper installed successfully!')"
```

If you see the success message, you're all set! 🚀

---

## 📥 Getting the Code from GitHub

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/rulemj7/Workflow-AI.git
```

### 2️⃣ Navigate to the Project Directory

```sh
cd Workflow-AI
```

### 3️⃣ Activate Virtual Environment

```sh
whisper_env\Scripts\activate  # Windows
source whisper_env/bin/activate  # Mac/Linux
```

### 4️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

You're now ready to use the tool! 🚀

---

## 🚀 How the Tool Works (Behind the Scenes)

1. **Detects Hardware** – Uses GPU if available.
2. **Asks You to Pick a Model** – `tiny`, `small`, `base`, `medium`, `large`.
3. **Processes the Media File** – Extracts audio if video is used.
4. **Starts Transcription** – Shows real-time progress.
5. **Saves the Transcription** – Outputs a `.txt` file.

---

## 🎯 How to Use the Tool

```sh
python main.py
```

---

## 📝 Example Transcription Flows

### **1️⃣ Simplified Transcription Flow** (User-Friendly)
1. **Run the Script:**
   ```sh
   python main.py
   ```
2. **Select Whisper Model:** The script will ask for a model (`tiny`, `small`, `base`, `medium`, `large`).
3. **Enter File Path:** Right-click the Video or Audio file in your computer → Click Copy as Path → Paste in the tool → Press Enter.
4. **Real-Time Progress:** The script displays a progress bar while transcribing.
5. **Transcript Saved:**
   - Full transcript: `output.txt`
   - Timestamps & session-wise transcript: `timestamps.txt`

### **2️⃣ Customizable Transcription Flow (Command-Line Arguments)**
This mode gives you more control over settings like model selection and output file location.

```sh
python main.py --model medium --media /path/to/file.mp3 --output /custom/path/output.txt
```
- `--model` → Choose Whisper model (`tiny`, `small`, `base`, `medium`, `large`)
- `--media` → Path to the audio or video file
- `--output` → (Optional) Custom output file location

**Example Console Output:**
```
Using device: CPU
Enter Whisper model (tiny, small, base, medium, large): tiny
Using model: tiny
Loading 'tiny' model on CPU...
Model loaded successfully.
Enter the full path of your audio or video file: "D:\Videos\Recording.mp4"
Video file detected. Whisper will attempt to extract and transcribe the audio.

Starting transcription...
100% [==========]  
Transcription completed in 2m 26s!
Transcription saved to: D:\Videos\Recording_2025-02-18.txt
Timestamps saved to: D:\Videos\Recording_2025-02-18_timestamps.txt
```

Now you can open the generated `.txt` file and use it as needed! 🚀

---

## 🎥 Demo Video

Watch how easy it is to use Whisper Transcription Tool:

[![Watch the Demo](https://img.youtube.com/vi/4IWGEqcjP6w/0.jpg)](https://www.youtube.com/watch?v=4IWGEqcjP6w)

---

## 🤝 Contributing

We welcome contributions! Feel free to submit pull requests or report issues.

---

## 📜 License

This project is **open-source** under the MIT License. Enjoy unlimited transcriptions without annoying paywalls! 🚀
