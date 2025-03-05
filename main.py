import whisper
import torch
import os
import time
import argparse
from pathlib import Path
import threading
import sys

# Global variable to store partial results
partial_results = []
is_transcribing = False

def main():
    # Step 1: Set up argument parser for command line options
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
        help="Path to audio or video file for transcription"
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
        help="Output file path for transcription (default: same as input with .txt extension)"
    )
    args = parser.parse_args()

    # Step 2: Check GPU availability and set device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Step 3: Handle model selection (from args or interactively)
    model_name = args.model
    if not args.media:
        # If running interactively without command line args
        user_model = input("Enter Whisper model (tiny, small, base, medium, large): ").strip().lower()
        if user_model in ["tiny", "small", "base", "medium", "large"]:
            model_name = user_model
        elif user_model:
            print(f"Invalid model name '{user_model}'! Using '{model_name}' instead.")
    
    print(f"Using model: {model_name}")
    
    # Step 4: Load model with error handling
    print(f"Loading '{model_name}' model on {device}...")
    try:
        model = whisper.load_model(model_name, device=device)
        print(f"Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Step 5: Get media file path (from args or interactively)
    media_path = args.media
    if not media_path:
        media_path = input("Enter the full path of your audio or video file: ").strip()
    
    # Clean up the path - handle pasted paths with quotes and normalize slashes
    media_path = media_path.strip('"\'')  # Remove any surrounding quotes
    media_path = os.path.normpath(media_path)  # Normalize path separators for the current OS
    
    # Validate media file exists
    if not os.path.isfile(media_path):
        print(f"Error: File not found: {media_path}")
        return
    
    # Check if it's a video file and inform the user
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
    file_ext = os.path.splitext(media_path)[1].lower()
    if file_ext in video_extensions:
        print(f"Video file detected. Whisper will attempt to extract and transcribe the audio.")
    
    # Step 6: Determine output file path
    output_path = args.output
    if not output_path:
        media_file = Path(media_path)
        output_path = media_file.with_suffix('.txt')
    
    segments_path = Path(output_path).with_name(f"{Path(output_path).stem}_timestamps.txt")
    
    # Step 7: Start transcription with real-time updates
    print("\nStarting transcription...")
    global is_transcribing
    is_transcribing = True
    
    # Start the display thread to show real-time updates
    display_thread = threading.Thread(target=display_partial_results)
    display_thread.daemon = True
    display_thread.start()
    
    start_time = time.time()
    
    try:
        # Perform the transcription with real-time feedback
        options = {
            "fp16": device == "cuda",
            "language": args.language,
            "verbose": False  # We'll handle our own display
        }
        
        # Call the transcribe method - Whisper can handle many audio and video formats directly
        result = transcribe_with_progress(model, media_path, options)
        
        # Transcription finished
        is_transcribing = False
        
        # Wait for display thread to catch up
        display_thread.join(1)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"\n\nTranscription completed in {minutes}m {seconds}s!")
        
        # Step 8: Save results to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        # Save segments with timestamps
        with open(segments_path, "w", encoding="utf-8") as f:
            f.write("# Transcription with Timestamps\n\n")
            for segment in result.get("segments", []):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                f.write(f"[{format_time(start)} → {format_time(end)}] {text}\n")
        
        # Display summary
        print(f"\nTranscription saved to: {output_path}")
        print(f"Timestamps saved to: {segments_path}")
        
    except Exception as e:
        is_transcribing = False
        print(f"\nError during transcription: {e}")
        
        # Provide helpful error message for common video-related errors
        if "ffmpeg" in str(e).lower() or "av" in str(e).lower():
            print("\nThe error may be related to video processing. Whisper uses PyAV or FFmpeg internally.")
            print("You may need to install additional dependencies:")
            print("pip install av ffmpeg-python")
            print("\nAlternatively, you can pre-convert your video to audio using:")
            print("- VLC Media Player")
            print("- Online converters")
            print("- FFmpeg command: ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav")


def transcribe_with_progress(model, media_path, options):
    """Transcribe media with progress updates"""
    global partial_results
    
    # Create a wrapper around Whisper's segment callback
    def process_segment(segment):
        # Add the segment to our partial results
        partial_results.append(segment)
    
    # Create modified options to include our callback
    modified_options = options.copy()
    
    # Use the Whisper model's transcribe method
    result = model.transcribe(media_path, **modified_options)
    
    # Store all segments
    partial_results = result.get("segments", [])
    
    return result


def display_partial_results():
    """Display partial results as they become available"""
    global partial_results, is_transcribing
    
    last_segment_count = 0
    animation = "|/-\\"
    animation_idx = 0
    
    # Continue until transcription is complete
    while is_transcribing:
        # Check if we have new segments
        current_segment_count = len(partial_results)
        
        if current_segment_count > last_segment_count:
            # Display new segments
            for i in range(last_segment_count, current_segment_count):
                segment = partial_results[i]
                start_time = format_time(segment["start"])
                end_time = format_time(segment["end"])
                text = segment["text"].strip()
                
                # Print the segment with timestamps
                print(f"\r[{start_time} → {end_time}] {text}")
            
            # Update last seen count
            last_segment_count = current_segment_count
        
        # Show a spinner to indicate we're still working
        sys.stdout.write(f"\rProcessing... {animation[animation_idx]} ")
        sys.stdout.flush()
        animation_idx = (animation_idx + 1) % len(animation)
        
        # Short sleep to prevent CPU hogging
        time.sleep(0.2)
    
    # Clear the animation line when done
    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()


def format_time(seconds):
    """Convert seconds to a formatted time string (MM:SS)"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    main()