import os
import whisper
import subprocess
import pandas as pd

# 📍 Path to the Excel File & Settings
excel_path = "/Users/nurankhalaf/Downloads/TikTok_Data_EndVersion.xlsx"
sheet_name = "tiktok_videos_cleaned"
url_column = "H"  # Spalte mit URLs (Excel-Spalte H)

# 🎙 Whisper-Modell laden
model = whisper.load_model("base")

# 📖 Read Excel file (limit to first 500 rows if necessary)
df = pd.read_excel(excel_path, sheet_name=sheet_name)
urls = df.iloc[:, 7]  # Spalte H (Nullbasiert: A=0, B=1, ..., H=7)

# 🆕 New column for transcripts
df["Transcript"] = ""

for idx, url in enumerate(urls):
    if not isinstance(url, str) or not url.startswith("http"):
        print(f"⏩ Zeile {idx+2} übersprungen – keine gültige URL")
        continue

    print(f"\n🔽 [{idx+1}] Lade Audio von:\n{url}")
    audio_filename = f"audio_{idx+1}.mp3"

    try:
        # Download TikTok audio using yt-dlp
        subprocess.run([
            "yt-dlp",
            "-x", "--audio-format", "mp3",
            "-o", audio_filename,
            url
        ], check=True)

        print("🧠 Transkribiere Audio...")
        result = model.transcribe(audio_filename)
        df.at[idx, "Transcript"] = result["text"]

    except subprocess.CalledProcessError:
        print("⚠️ Fehler beim Download – übersprungen.")
    except Exception as e:
        print(f"⚠️ Fehler bei Transkription: {e}")

    # 🧹 Remove audio file
    if os.path.exists(audio_filename):
        os.remove(audio_filename)

# 💾 Export to a new Excel file
output_path = "/Users/nurankhalaf/Desktop/TikTok_with_Transcripts.xlsx"
df.to_excel(output_path, sheet_name=sheet_name, index=False)
print(f"\n✅ Transkripte gespeichert unter: {output_path}")
