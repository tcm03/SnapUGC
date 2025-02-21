import argparse
import os
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Integrity check script",
        prog = "integrity_check.py",
    )
    parser.add_argument('--path', type = str, required = True, help = 'Path to video folder')
    parser.add_argument('--output', type = str, required = False, default = None, help = 'Path to output file')
    parser.add_argument('--action', type = str, required = False, default = "log", help = "Either log or rm")
    args = parser.parse_args()
    if args.action == "log":
        if args.output is None:
            assert False, "Output file is required for log action"
        with open(args.output, 'w') as f:
            f.write('')

    for root, dirs, files in os.walk(args.path):
        for file in files:
            file_path = os.path.join(root, file)
            command = [
                'ffmpeg', 
                '-v', 
                'error', 
                '-i', 
                file_path, 
                '-f', 
                'null', 
                '-'
            ]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0 or b"partial" in result.stderr:
                if args.action == "log":
                    with open(args.output, 'a') as f:
                        f.write(file_path + '\n' + result.stderr.decode('utf-8') + '\n')
                elif args.action == "rm":
                    os.remove(file_path)
                else:
                    print("Invalid action")
                    exit(1)
    