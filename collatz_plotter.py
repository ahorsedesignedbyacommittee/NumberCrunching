from matplotlib import pyplot as plt

fp = open("collatz_data.txt", "r")
x = []
y = []
for line in fp:
    line_list = line.split(",")
    x.append(int(line_list[0]))
    y.append(int(line_list[1]))
fp.close()
plt.scatter(x,y, s = 1)
plt.show()
