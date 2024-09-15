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

    plt.gca().xaxis.set_major_formatter(tkr.FuncFormatter(sizeof_fmt))
    plt.plot(df_to_plot["size"], df_to_plot["new"].rolling(15).median(), label="new")
    plt.plot(df_to_plot["size"], df_to_plot["old"].rolling(15).median(), label="old")
    

    plt.xlabel("size(bytes)")
    plt.ylabel("ns")
    
    plt.xscale('log')
    plt.yscale('log')

    simple_formatter = lambda x, _: "%0.1f" % x
    plt.gca().yaxis.set_major_formatter(tkr.FuncFormatter(simple_formatter))
    plt.gca().yaxis.set_minor_formatter(tkr.FuncFormatter(simple_formatter))
    plt.gca().grid(True, which="major", linestyle="--", linewidth=1)
    
    plt.gca().yaxis.set_major_locator(tkr.LogLocator(base=10.0, subs=list(range(0, 10, 2)), numticks=1))
    plt.legend()

    plt.savefig("graph.png")
    plt.show()

if __name__ == "__main__": main()