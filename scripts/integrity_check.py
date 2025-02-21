import argparse
import os
import subprocess
import concurrent.futures

def process_file(file_path, action, output):
    command = [
        'ffmpeg',
        '-v', 'error',
        '-i', file_path,
        '-f', 'null',
        '-'
    ]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0 or "partial" in result.stderr:
            print(f"{file_path}: not okay")
            if action == "log" and output:
                with open(output, 'a') as f:
                    f.write(f"{file_path}\n{result.stderr}\n")
            elif action == "rm":
                os.remove(file_path)
        else:
            print(f"{file_path}: okay")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Integrity check script",
        prog="integrity_check.py",
    )
    parser.add_argument('--path', type=str, required=True, help='Path to video folder')
    parser.add_argument('--output', type=str, required=False, default=None, help='Path to output file')
    parser.add_argument('--action', type=str, required=False, default="log", choices=["log", "rm"], help="Action to perform on corrupted files: 'log' or 'rm'")
    args = parser.parse_args()

    if args.action == "log" and args.output is None:
        parser.error("Output file is required for log action")
    
    if args.output:
        # Clear the output file at the start
        with open(args.output, 'w') as f:
            f.write('')

    # Collect all .mp4 video files
    video_files = []
    for root, _, files in os.walk(args.path):
        for file in files:
            if file.lower().endswith('.mp4'):
                file_path = os.path.join(root, file)
                video_files.append(file_path)

    # Process files concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_file, file_path, args.action, args.output): file_path for file_path in video_files}
        for future in concurrent.futures.as_completed(futures):
            file_path = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    main()
