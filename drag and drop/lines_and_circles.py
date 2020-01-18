import matplotlib.pyplot as plt
from movable_object import Movableobj

class Circlebuilder:
    #TODO: добавить возможность перетаскивать объекты мышью
    def __init__(self, ax):
        self.ax = ax
        self.circle = plt.Circle((0, 0), 0, color='r', picker=0)
        self.movablecircle = Movableobj(self.circle, self.ax)
        self.ax.add_artist(self.circle)
        self.line = self.ax.plot([], [], 'b', picker=2)[0]
        self.movableline = Movableobj(self.line, self.ax)
        self.dots = []
        self.movabledots = []
        for i in range(3):
            self.dots.append(self.ax.plot([], [], 'og', picker=2)[0])
            # self.movabledots.append(Movableobj(self.dots[i], self.ax))
        self.cid1 = self.ax.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.cid2 = self.ax.figure.canvas.mpl_connect('motion_notify_event', self.onmove)
        self.xclickcoords = []
        self.yclickcoords = []

    def get_circledata(self, xs, ys):
        if len(xs) != 3 or len(ys) != 3:
            print('Длина списков не равна 3', xs, ys)
            return 0, 0, 0
        a1 = xs[0]; b1 = xs[1]; c1 = xs[2]
        a2 = ys[0]; b2 = ys[1]; c2 = ys[2]
        m = 0.5*(b1**2 + b2**2 - a1**2 - a2**2 - (b1-a1)**2 - (b2-a2)**2)
        l = 0.5*(c1**2 + c2**2 - a1**2 - a2**2)
        d = (b1 - a1)*(c2 - a2) - (c1 - a1)*(b2 - a2)
        if d**2 < 0.00001:
            return 0, 0, 0
        o1 = (m*(c2 - a2) - l*(b2 - a2))/d
        o2 = (-m*(c1 - a1) + l*(b1 - a1))/d
        r = ((a1 - o1)**2 + (a2 - o2)**2)**0.5
        return o1, o2, r

    def clearax(self):
        for i in range(3):
            self.dots[i].set_data([], [])
        self.line.set_data([], [])
        self.circle.set_radius(0)

    def onclick(self, event):
        if not event.inaxes:
            return
        self.xclickcoords.append(event.xdata)
        self.yclickcoords.append(event.ydata)
        if len(self.yclickcoords) == 1:
            self.clearax()
            self.dots[0].set_data([event.xdata], [event.ydata])
        elif len(self.yclickcoords) == 2:
            self.dots[1].set_data([event.xdata], [event.ydata])
            self.line.set_data(self.xclickcoords, self.yclickcoords)
        else:
            self.dots[2].set_data([event.xdata], [event.ydata])
            o1, o2, r = self.get_circledata(self.xclickcoords, self.yclickcoords)
            self.circle.set_radius(r)
            self.circle.set_center((o1, o2))
            self.xclickcoords.clear()
            self.yclickcoords.clear()

            self.ax.figure.canvas.mpl_disconnect(self.cid1)
            self.ax.figure.canvas.mpl_disconnect(self.cid2)

        self.ax.figure.canvas.draw()

    def onmove(self, event):
        if not event.inaxes:
            return
        xmclickcoords = self.xclickcoords + [event.xdata]
        ymclickcoords = self.yclickcoords + [event.ydata]
        if len(ymclickcoords) == 1:
            # self.dots[0].set_data(event.xdata, event.ydata)
            pass
        elif len(ymclickcoords) == 2:
            self.dots[1].set_data(event.xdata, event.ydata)
            self.line.set_data(xmclickcoords, ymclickcoords)
        else:
            o1, o2, r = self.get_circledata(xmclickcoords, ymclickcoords)
            self.circle.set_radius(r)
            self.circle.set_center((o1, o2))
            self.dots[2].set_data(xmclickcoords, ymclickcoords)
        self.ax.figure.canvas.draw()

    def getdata(self):
        #TODO: вернуть объект
        pass


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_aspect('equal')
    ax.grid(True)

    circlebuilder = Circlebuilder(ax)
    # a = Movableobj(circlebuilder.circle, ax)
    plt.show()
