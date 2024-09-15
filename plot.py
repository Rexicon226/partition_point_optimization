import matplotlib.pyplot as plt
import matplotlib.ticker as tkr  
import pandas as pd

def main():
    file = open("data.txt", "r")
    lines = file.readlines()

    data = []

    for i in range(0, len(lines), 1):
        line = lines[i]
        line = line.split(",")

        size = int(line[0])

        new_time = float(line[1])
        old_time = float(line[2])

        data.append([size, new_time, old_time])

    file.close()

    df = pd.DataFrame(data, columns=["size", "new", "old"])

    df_to_plot = df

    plt.plot(df_to_plot["size"], df_to_plot["new"].rolling(15).median(), label="new (branchless)")
    plt.plot(df_to_plot["size"], df_to_plot["old"].rolling(15).median(), label="old")
    

    plt.xlabel("size(bytes)")
    plt.ylabel("runtime(ns)")
    
    plt.xscale('log')
    plt.yscale('log')

    simple_formatter = lambda x, _: "%0.1f" % x
    
    
    plt.gca().yaxis.set_major_formatter(tkr.FuncFormatter(simple_formatter))
    plt.gca().yaxis.set_minor_formatter(tkr.FuncFormatter(simple_formatter))
    plt.gca().grid(True, which="both", axis="y", linestyle="--", linewidth=1)
    plt.gca().grid(True, which="major", axis="x", linestyle="--", linewidth=1)
    
    plt.gca().yaxis.set_major_locator(tkr.LogLocator(base=10.0, subs=[], numticks=1))
    plt.gca().yaxis.set_minor_locator(tkr.LogLocator(base=10.0, subs=list(range(0, 10, 2)), numticks=1))
    plt.legend()

    plt.title("partition point benchmark")

    plt.savefig("graph.png")
    plt.show()

if __name__ == "__main__": main()