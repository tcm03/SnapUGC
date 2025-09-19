import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend before importing pyplot
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

INPUT_PATH = "/media02/nthuy/SnapUGC/train_out_sanitized.txt"
OUTPUT_IMG = "/media02/nthuy/SnapUGC/images/video_duration_histogram.png"

def load_durations(path):
    durations = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for row in reader:
            try:
                durations.append(int(float(row[1])))
            except (IndexError, ValueError):
                continue
    return durations

def plot_histogram(durations, out_img):
    max_fixed = 60
    bin_edges = list(np.arange(0, max_fixed + 5, 5))
    bin_edges.append(max(durations) + 1)

    plt.figure(figsize=(8, 5))
    plt.hist(durations, bins=bin_edges, edgecolor="black", color="skyblue")

    xticks = bin_edges[:-1]
    xtick_labels = [f"{int(b)}–{int(b+5)}" for b in xticks[:-1]] + [f"{xticks[-1]}+"]
    plt.xticks(xticks, xtick_labels, rotation=45)

    plt.xlabel("Video Duration (in 5-second intervals)")
    plt.ylabel("Number of Videos")
    plt.title("Distribution of Video Durations of the SnapUGC Dataset")
    plt.grid(axis="y", alpha=0.75)
    plt.tight_layout()

    plt.savefig(out_img, dpi=150, bbox_inches='tight')
    # plt.show()  # omit this on headless servers

if __name__ == "__main__":
    durations = load_durations(INPUT_PATH)
    print(f"Loaded {len(durations)} durations → min={min(durations)}, max={max(durations)}")
    plot_histogram(durations, OUTPUT_IMG)
    print(f"Histogram saved to: {OUTPUT_IMG}")