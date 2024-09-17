import matplotlib.pyplot as plt
import matplotlib.ticker as tkr  
import pandas as pd

def sizeof_fmt(x, pos):
    if x<0:
        return ""
    for x_unit in ['bytes', 'kB', 'MB', 'GB', 'TB']:
        if x < 1024:
            return "%3.0f %s" % (x, x_unit)
        x /= 1024

# Main function
def main():
    # Read the file
    file = open("data.txt", "r")
    lines = file.readlines()

    start_data = []
    middle_data = []
    end_data = []    

    for i in range(0, len(lines), 1):
        line = lines[i]
        line = line.split(",")

        size = int(line[0])

        start_new = int(line[1])
        start_old = int(line[2])
        start_data.append([size, start_new, start_old])

        middle_new = int(line[3])
        middle_old = int(line[4])
        middle_data.append([size, middle_new, middle_old])

        end_new = int(line[5])
        end_old = int(line[6])
        end_data.append([size, end_new, end_old])
    file.close()

    start_df = pd.DataFrame(start_data, columns=["size", "new", "old"])
    middle_df = pd.DataFrame(middle_data, columns=["size", "new", "old"])
    end_df = pd.DataFrame(end_data, columns=["size", "new", "old"])

    # Smooth the data by taking a rolling average of 10 points for the "new" and "old" columns
    start_df["new"] = start_df["new"].rolling(window=10).mean()
    start_df["old"] = start_df["old"].rolling(window=10).mean()

    middle_df["new"] = middle_df["new"].rolling(window=10).mean()
    middle_df["old"] = middle_df["old"].rolling(window=10).mean()

    end_df["new"] = end_df["new"].rolling(window=10).mean()
    end_df["old"] = end_df["old"].rolling(window=10).mean()

    # Plot each DataFrame as a seperate plot using subplots. So, 3x1 grid of plots
    fig, ax = plt.subplots(3, 1, figsize=(10, 10))

    # Plot the start data
    ax[0].plot(start_df["size"], start_df["new"], label="new")
    ax[0].plot(start_df["size"], start_df["old"], label="old")
    ax[0].set_title("Point at the start")
    ax[0].xlabel = "Items"

    # Plot the middle data
    ax[1].plot(middle_df["size"], middle_df["new"], label="new")
    ax[1].plot(middle_df["size"], middle_df["old"], label="old")
    ax[1].set_title("Point at the middle")

    # Plot the end data
    ax[2].plot(end_df["size"], end_df["new"], label="new")
    ax[2].plot(end_df["size"], end_df["old"], label="old")
    ax[2].set_title("Point at the end")


    plt.xlabel("Items")
    plt.ylabel("Cycles")

    plt.legend()
    plt.savefig("graph.png")



main()