import csv
import pandas as pd
import matplotlib.pyplot as plt

TRAIN_FILE_PATH = "train_out_sanitized.txt"
TEST_FILE_PATH = "test_out_sanitized.txt"

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":

    metrics = []
    with open(TRAIN_FILE_PATH, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)  # Skip header row
        for row in reader:
            if row[1] == '' or row[2] == '' or row[3] == '':
                print(f"Empty row found: {row[0]}")
                continue
            if not is_float(row[1]) or not row[2].isdigit() or not row[3].isdigit():
                print(f"Non-numeric row found: {row[0]}")
                continue
            metrics.append({
                "duration": float(row[1]),
                "ecr": int(row[2]),
                "nawp": int(row[3])
            })

    with open(TEST_FILE_PATH, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter="\t")
        next(reader)
        for row in reader:
            if row[1] == '' or row[2] == '' or row[3] == '':
                print(f"Empty row found: {row[0]}")
                continue
            if not is_float(row[1]) or not row[2].isdigit() or not row[3].isdigit():
                print(f"Non-numeric row found: {row[0]}")
                continue
            metrics.append({
                "duration": float(row[1]),
                "ecr": int(row[2]),
                "nawp": int(row[3])
            })
    print("Number of videos read:", len(metrics))
    ecrs = pd.Series([m["ecr"] for m in metrics])
    ecrs.plot.hist(bins=100, edgecolor="black")
    plt.xlabel('Order of ECR')
    plt.ylabel('Frequency')
    plt.title('Histogram of orders of ECR')

    # Display the plot
    plt.show()
    ecrs_freq = {}
    for ecr in ecrs:
        if ecr not in ecrs_freq:
            ecrs_freq[ecr] = 0
        ecrs_freq[ecr] += 1
    sorted_ecrs = sorted(ecrs_freq.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 ECRs:")
    for ecr, freq in sorted_ecrs[:10]:
        print(f"ECR {ecr}: {freq} videos")
    nawps = pd.Series([m["nawp"] for m in metrics])
    nawps_freq = {}
    for nawp in nawps:
        if nawp not in nawps_freq:
            nawps_freq[nawp] = 0
        nawps_freq[nawp] += 1
    sorted_nawps = sorted(nawps_freq.items(), key=lambda x: x[1], reverse=True)
    print("Top 10 NAWPs:")
    for nawp, freq in sorted_nawps[:10]:
        print(f"NAWP {nawp}: {freq} videos")
    df = pd.DataFrame({"ecr": ecrs, "nawp": nawps})
    print("ECR statistics:")
    print(ecrs.describe())
    print("NAWP statistics:")
    print(nawps.describe())
    corr_coeff = ecrs.corr(nawps)
    print("Correlation coefficient:", corr_coeff)
    plt.scatter(ecrs, nawps)
    plt.xlabel("ECR")
    plt.ylabel("NAWP")
    plt.title("NAWP vs ECR")
    plt.show()

    plt.figure(figsize=(8,6))
    hb = plt.hexbin(ecrs, nawps, gridsize=50, cmap='inferno', bins='log')

    # Add colorbar
    plt.colorbar(label='log(count)')
    plt.xlabel('ECR')
    plt.ylabel('NAWP')
    plt.title('Density Plot: NAWP vs ECR')
    plt.show()

    plt.figure(figsize=(8,6))
    sns.kdeplot(x=ecrs, y=nawps, cmap="coolwarm", fill=True, levels=50, alpha=0.5)

    plt.scatter(ecrs, nawps, s=1, color='black', alpha=0.3)  # Overlay scatterplot for context
    plt.xlabel('ECR')
    plt.ylabel('NAWP')
    plt.title('Density Contour: NAWP vs ECR')
    plt.show()