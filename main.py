import argparse
import os
import sys
import threading
import time
from pathlib import Path
import torch
import whisper
import yt_dlp

# Global variables for transcription progress
partial_results = []
is_transcribing = False

def download_youtube_audio(youtube_url: str, output_dir: str = "temp") -> str:

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    audio_file = os.path.join(output_dir, "youtube_audio.mp3")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': audio_file[:-4],  
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
        'retries': 3,
        'fragment_retries': 3,
        'nooverwrites': True,
        'continuedl': True,
    }
    
    print(f"Downloading audio from: {youtube_url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        
        # Handle potential filename variations
        possible_path = audio_file[:-4] + '.mp3'
        if os.path.exists(possible_path) and not os.path.exists(audio_file):
            os.rename(possible_path, audio_file)
        
        if not os.path.exists(audio_file):
            raise Exception("Audio file not found after download")
        
        print(f"Audio downloaded successfully to: {audio_file}")
        return audio_file
    except Exception as e:
        raise Exception(f"Failed to download YouTube audio: {e}")

def transcribe_with_progress(model, media_path: str, options: dict) -> dict:
    """Transcribe media with real-time progress updates.

    Args:
        model: Loaded Whisper model instance.
        media_path: Path to the media file.
        options: Transcription options for Whisper.

    Returns:
        Transcription result dictionary.
    """
    global partial_results
    
    def process_segment(segment):
        partial_results.append(segment)
    
    modified_options = options.copy()
    result = model.transcribe(media_path, **modified_options)
    partial_results = result.get("segments", [])
    return result

def display_partial_results():
    """Display transcription progress in real-time."""
    global partial_results, is_transcribing
    
    last_segment_count = 0
    animation = "|/-\\"
    animation_idx = 0
    
    while is_transcribing:
        current_segment_count = len(partial_results)
        if current_segment_count > last_segment_count:
            for i in range(last_segment_count, current_segment_count):
                segment = partial_results[i]
                start_time = format_time(segment["start"])
                end_time = format_time(segment["end"])
                text = segment["text"].strip()
                print(f"\r[{start_time} → {end_time}] {text}")
            last_segment_count = current_segment_count
        
        sys.stdout.write(f"\rProcessing... {animation[animation_idx]} ")
        sys.stdout.flush()
        animation_idx = (animation_idx + 1) % len(animation)
        time.sleep(0.2)
    
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()

def format_time(seconds: float) -> str:
    """Convert seconds to a MM:SS formatted string.

    Args:
        seconds: Time in seconds.

    Returns:
        Formatted time string.
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def main():
    """Main function to handle media transcription."""
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Whisper Audio/Video Transcription Tool")
    parser.add_argument(
        "--model",
        type=str,
        default="small",
        choices=["tiny", "small", "base", "medium", "large"],
        help="Whisper model size to use (tiny, small, base, medium, large)"
    )
    parser.add_argument(
        "--media",
        type=str,
        help="Path to audio/video file or YouTube URL for transcription"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="Language code (default: English)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path for transcription (default: input-based .txt)"
    )
    args = parser.parse_args()

    # Device setup
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Model selection
    model_name = args.model
    if not args.media:
        user_model = input("Enter Whisper model (tiny, small, base, medium, large): ").strip().lower()
        if user_model in ["tiny", "small", "base", "medium", "large"]:
            model_name = user_model
        elif user_model:
            print(f"Invalid model name '{user_model}'! Using '{model_name}' instead.")
    
    print(f"Using model: {model_name}")

    # Load model
    print(f"Loading '{model_name}' model on {device}...")
    try:
        model = whisper.load_model(model_name, device=device)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)

    # Media input
    media_input = args.media
    if not media_input:
        media_input = input("Enter YouTube URL or full path to audio/video file: ").strip()
    
    media_input = media_input.strip('"\'')
    is_youtube = media_input.startswith("http") and ("youtube.com" in media_input or "youtu.be" in media_input)
    
    if is_youtube:
        try:
            media_path = download_youtube_audio(media_input)
        except Exception as e:
            print(f"Failed to process YouTube video: {e}")
            sys.exit(1)
    else:
        media_path = os.path.normpath(media_input)
        if not os.path.isfile(media_path):
            print(f"Error: File not found: {media_path}")
            sys.exit(1)

    # Check media type
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    file_ext = os.path.splitext(media_path)[1].lower()
    if file_ext in video_extensions:
        print("Video file detected. Whisper will extract and transcribe the audio.")

    # Output path setup
    output_path = args.output or Path(media_path).with_suffix('.txt')
    segments_path = Path(output_path).with_name(f"{Path(output_path).stem}_timestamps.txt")

    # Transcription
    print("\nStarting transcription...")
    global is_transcribing
    is_transcribing = True
    
    display_thread = threading.Thread(target=display_partial_results)
    display_thread.daemon = True
    display_thread.start()
    
    start_time = time.time()
    try:
        options = {
            "fp16": device == "cuda",
            "language": args.language,
            "verbose": False
        }
        result = transcribe_with_progress(model, media_path, options)
        is_transcribing = False
        display_thread.join(1)
        
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        print(f"\n\nTranscription completed in {minutes}m {seconds}s!")

        # Save results
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        with open(segments_path, "w", encoding="utf-8") as f:
            f.write("# Transcription with Timestamps\n\n")
            for segment in result.get("segments", []):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                f.write(f"[{format_time(start)} → {format_time(end)}] {text}\n")
        
        print(f"\nTranscription saved to: {output_path}")
        print(f"Timestamps saved to: {segments_path}")

        # Cleanup
        if is_youtube and os.path.exists(media_path):
            os.remove(media_path)
            temp_dir = os.path.dirname(media_path)
            if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                os.rmdir(temp_dir)

    except Exception as e:
        is_transcribing = False
        print(f"\nError during transcription: {e}")
        if "ffmpeg" in str(e).lower() or "av" in str(e).lower():
            print("\nThe error may be related to video processing. Ensure FFmpeg is installed:")
            print("pip install ffmpeg-python")
            print("Install FFmpeg: https://ffmpeg.org/download.html")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)