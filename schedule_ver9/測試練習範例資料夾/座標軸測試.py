
import matplotlib.pyplot as plt
def main():
    chosen = int(input("1.十字座標  2.一般座標 ："))
    if chosen == 1:
        cross_axes()
    else:
        general()
      
    
def cross_axes():
    x = [0,1,2,3,4,5]
    fig, ax = plt.subplots()
    ax.plot(x)
    ax.set_xlim(-6,6)
    ax.set_ylim(-6,6)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_position(('axes',0.5))
    ax.spines['left'].set_position(('axes',0.5))
    plt.show()

def general():
    x = [0,1,2,3,4,5]
    fig, ax = plt.subplots()
    ax.plot(x)
    ax.set_xlim(-6,6)
    ax.set_ylim(-6,6)
    plt.show()

main()
