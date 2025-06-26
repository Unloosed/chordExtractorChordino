import os
import csv
from chord_extractor.extractors import Chordino
from collections import Counter

print("🎵 Chord Detection Script")

# === User Inputs ===
input_file = input("Enter full path to the .wav file: ").strip('"')

if not os.path.exists(input_file):
    print(f"❌ File not found: {input_file}")
    exit()

default_txt = "detected_chords.txt"
output_file_txt = input(f"Enter name for output text file (default: {default_txt}): ").strip()
if not output_file_txt:
    output_file_txt = default_txt

skip_no_chords_input = input("Skip 'N' (no chord) entries? (y/n) [default: y]: ").strip().lower()
remove_no_chord = skip_no_chords_input != 'n'

# === Output Paths ===
output_dir = os.path.dirname(input_file)
base_filename = os.path.splitext(os.path.basename(input_file))[0]
output_csv = os.path.join(output_dir, base_filename + "_chords.csv")
output_txt = os.path.join(output_dir, output_file_txt)

try:
    print("\n🔍 Extracting chords, please wait...")
    chordino = Chordino()
    chords = chordino.extract(input_file)

    processed_chords = []
    for entry in chords:
        time = entry.timestamp
        chord = entry.chord
        if remove_no_chord and chord == "N":
            continue
        processed_chords.append((time, chord))

    print(f"✅ {len(processed_chords)} chord entries found.\n")

    # === Write TXT file ===
    with open(output_txt, "w") as f_txt:
        f_txt.write("Time (s)\tChord\n")
        f_txt.write("=" * 20 + "\n")
        for time, chord in processed_chords:
            try:
                time = float(time)  # Ensure time is a float
                line = f"{time:.2f}\t{chord}"
                f_txt.write(line + "\n")
            except Exception as e:
                print(f"⚠️ Skipping invalid entry: {(time, chord)} — {e}")

    print(f"📄 Text output saved to: {output_txt}")

    # === Write CSV file ===
    with open(output_csv, "w", newline='') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(["Time (s)", "Chord"])
        for time, chord in processed_chords:
            try:
                time = float(time)
                writer.writerow([f"{time:.2f}", chord])
            except Exception as e:
                print(f"⚠️ Skipping invalid entry: {(time, chord)} — {e}")

    print(f"📊 CSV output saved to: {output_csv}")

    # === Print summary ===
    chord_counts = Counter(chord for _, chord in processed_chords)

    print("\n🎼 Chord Summary:")
    for chord, count in chord_counts.most_common():
        print(f"{chord}: {count} times")

except Exception as e:
    print(f"❌ Error: {e}")