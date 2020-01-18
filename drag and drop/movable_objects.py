import matplotlib
import matplotlib.pyplot as plt

class Movableobj:
    def __init__(self, circle, ax):
        self.ax = ax
        self.circle = circle
        self.ax.figure.canvas.mpl_connect('pick_event', self.onpick)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.onrelease)
        self.picked = None

    def inc(self, iterable, dx):
        newdata = []
        for i in range(len(iterable)):
            newdata.append(iterable[i] + dx)
        return newdata

    def onmove(self, event):
        if not event.inaxes:
            return

        if not self.picked:
            return

        dx = event.xdata - self.startcoords[0]
        dy = event.ydata - self.startcoords[1]

        if type(self.picked) == matplotlib.patches.Circle:
            self.picked.set_center((self.center[0] + dx, self.center[1] + dy))
        elif type(self.picked) == matplotlib.lines.Line2D:
            self.picked.set_data(self.inc(self.data[0], dx), self.inc(self.data[1], dy))
        else:
            pass
        self.ax.figure.canvas.draw()

    def onpick(self, event):
        self.picked = event.artist
        # print(type(self.picked))
        if type(self.picked) == matplotlib.patches.Circle:
            self.center = self.picked.get_center()
        elif type(self.picked) == matplotlib.lines.Line2D:
            self.data = self.picked.get_data()
        else:
            self.picked = None
        self.startcoords = (event.mouseevent.xdata, event.mouseevent.ydata)

    def onrelease(self, event):
        if self.picked:
            self.picked = None


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_aspect('equal')
    ax.grid(True)

    circle = plt.Circle((0, 0), 1, color='r', picker=0)
    ax.add_artist(circle)

    circlebuilder = Movableobj(circle, ax)

    line = ax.plot([1, 2], [2, 4], 'b', picker=2)[0]
    m = Movableobj(line, ax)

    dot = ax.plot([1], [2], 'og', picker=2)[0]
    d = Movableobj(dot, ax)

    plt.show()
