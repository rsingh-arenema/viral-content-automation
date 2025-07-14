import os

def clean_script(input_path="data/script.txt", output_path="data/voice_script.txt"):
    if not os.path.exists(input_path):
        print(f"[✖] Script not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    spoken_lines = []
    capture = False

    for line in lines:
        line = line.strip()

        if line.lower().startswith("narrator"):
            capture = True
            # Extract line after colon if on same line
            if ":" in line:
                parts = line.split(":", 1)
                if len(parts) > 1 and parts[1].strip():
                    spoken_lines.append(parts[1].strip())
            continue

        # Continue capturing until next empty line or stage direction
        if capture:
            if line == "" or line.startswith("(") or line.startswith("**"):
                capture = False
            else:
                spoken_lines.append(line)

    full_script = " ".join(spoken_lines)
    full_script = full_script.replace("  ", " ").strip()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_script)

    print(f"[✔] Clean voice script saved: {output_path}")
    return output_path

# Test run
if __name__ == "__main__":
    clean_script()
