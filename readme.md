# Whisper Transcription Tool

## 📖 Table of Contents

- [Why Should You Use This Tool?](#why-should-you-use-this-tool)
- [Installation Guide](#installation-guide)
- [Getting the Code from GitHub](#getting-the-code-from-github)
- [How It Works](#how-the-tool-works-behind-the-scenes)
- [How to Use](#how-to-use-the-tool)
- [Features](#features)
- [Troubleshooting & FAQs](#troubleshooting--faqs)
- [Extra Tips](#extra-tips)
- [Contributing](#contributing)
- [License](#license)

---

## 💡 Why Should You Use This Tool?

Transcription services can be **expensive** and often come with **limitations, subscriptions, or intrusive bots** that join your meetings. Instead of dealing with all that, here’s a **simple and free way** to transcribe your audio or video files!

### 🎤 A Smarter, Cost-Free Alternative

Instead of relying on costly tools, you can use **Windows' built-in recording tools** (like the **Snipping Tool or Xbox Game Bar**) to record your meetings or videos **without any intrusive bots**. Once you have your recording, just **run it through this tool**, and it will transcribe everything for you—**for free!**

### 🎯 Choose Your Own Model

You can pick different **Whisper audio transcription models** depending on how accurate you want the transcription to be and how much time you have. **Higher accuracy = longer processing time.** [Check out the Whisperify documentation](#) to see the pros and cons of each model.

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

### 2️⃣ Install Python

1. Download **Python** from [python.org](https://www.python.org/)
2. **Important:** During installation, check the box that says **“Add Python to PATH”**
3. Once installed, verify the installation by running:
   ```sh
   python --version
   ```
   You should see output like `Python 3.x.x`.

### 3️⃣ Install an IDE (Optional, Recommended for Beginners)

If you're not familiar with running Python scripts, an **IDE (Integrated Development Environment)** makes things easier:

- **[Visual Studio Code (VS Code)](https://code.visualstudio.com/)** – Recommended!
- **[PyCharm](https://www.jetbrains.com/pycharm/)**

👉 **If using VS Code:** Install the Python extension from the Extensions tab.

### 4️⃣ Set Up a Virtual Environment (Recommended)

To keep dependencies isolated and avoid conflicts, **create a virtual environment:**

```sh
python -m venv whisper_env
```

Activate the virtual environment:
- **Windows:** `whisper_env\Scripts\activate`
- **Mac/Linux:** `source whisper_env/bin/activate`

### 5️⃣ Install Dependencies

After activating the virtual environment, install the required dependencies:

```sh
pip install -r requirements.txt
```

### 6️⃣ Verify the Installation

To confirm everything is installed correctly, run:

```sh
python -c "import whisper; print('Whisper installed successfully!')"
```

If you see the success message, you're all set! 🚀

---

## 📥 Getting the Code from GitHub

### 1️⃣ Clone the Repository

```sh
git clone <your-repository-url>
```

### 2️⃣ Navigate to the Project Directory

```sh
cd <your-repository-name>
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
python script.py --media /path/to/file.mp3
```

👉 **Choose a Model:**
```sh
python script.py --model medium --media /path/to/file.mp3
```

👉 **Specify Output File:**
```sh
python script.py --media /path/to/file.mp3 --output my_transcription.txt
```

---

## 🔥 Features

✅ **Works for audio & video**✅ **Uses CPU & GPU (GPU is faster!)**✅ **Saves transcripts with timestamps**✅ **Provides real-time updates**✅ **No subscriptions or hidden costs!**

---

## ❓ Troubleshooting & FAQs

### ❌ Problem: File Not Found

**Solution:** Ensure you provide the correct path.

### ❌ Problem: Missing Dependencies

**Solution:** Install FFmpeg:

```sh
pip install av ffmpeg-python
```

### ❌ Problem: Transcription is Slow

**Solution:**

- Use a **GPU** if available.
- Try a **smaller model** like `tiny` or `small`.

---

## 🤝 Contributing

We welcome contributions! Feel free to submit pull requests or report issues.

---

## 📜 License

This project is **open-source** under the MIT License. Enjoy unlimited transcriptions without annoying paywalls! 🚀
