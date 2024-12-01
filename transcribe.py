import os
import subprocess
import sys
import whisper

def extract_audio(input_file, output_audio):
    """Extract the audio from the input video file."""
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vn",  # No video
        "-ac", "1",  # Convert to mono
        "-ar", "16000",  # Resample to 16 kHz
        "-y",  # Overwrite without asking
        output_audio
    ]
    subprocess.run(command, check=True)

def transcribe_audio(audio_file, model_name="base"):
    """Transcribe audio to SRT using Whisper."""
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_file)
    return result.get("segments", [])

def save_srt(segments, output_file):
    """Save the transcription segments to an SRT file."""
    with open(output_file, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(segments, start=1):
            start_time = format_time(segment["start"])
            end_time = format_time(segment["end"])
            text = segment["text"]
            srt_file.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

def format_time(seconds):
    """Format time in seconds to SRT time format."""
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <video_file>")
        sys.exit(1)

    input_video = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    temp_audio = f"/app/{base_name}.wav"
#    output_srt = f"/app/{base_name}.srt"
    basedir = os.path.dirname(input_video)
    output_srt = f"{basedir}/{base_name}.srt"

    try:
        extract_audio(input_video, temp_audio)
        segments = transcribe_audio(temp_audio)
        save_srt(segments, output_srt)
        print(f"Subtitle file generated: {output_srt}")
    finally:
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
