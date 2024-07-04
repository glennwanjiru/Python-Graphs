import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

class DraggablePoint:
    def __init__(self, point, points, update_curve_callback, index):
        self.point = point
        self.points = points
        self.update_curve_callback = update_curve_callback
        self.index = index
        self.press = None

    def connect(self):
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        contains, _ = self.point.contains(event)
        if not contains: return
        self.press = self.point.get_xdata(), self.point.get_ydata(), event.xdata, event.ydata

    def on_release(self, event):
        self.press = None
        self.point.figure.canvas.draw()

    def on_motion(self, event):
        if self.press is None: return
        if event.inaxes != self.point.axes: return
        xpress, ypress, xorig, yorig = self.press
        dx = event.xdata - xorig
        dy = event.ydata - yorig
        new_x = xpress + dx
        new_y = ypress + dy
        self.point.set_xdata(new_x)
        self.point.set_ydata(new_y)
        self.points[self.index] = (new_x, new_y)
        self.update_curve_callback()
        self.point.figure.canvas.draw()

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 11, 12, 13, 14]
points = list(zip(x, y))

fig, ax = plt.subplots()

# Create initial scatter plot
scatter = ax.scatter(x, y, color='blue', picker=True)

# Function to update the smooth curve
def update_curve():
    points_sorted = sorted(points)
    x_sorted, y_sorted = zip(*points_sorted)
    cs = CubicSpline(x_sorted, y_sorted, bc_type='natural')
    x_new = np.linspace(min(x_sorted), max(x_sorted), 500)
    y_new = cs(x_new)
    curve.set_data(x_new, y_new)
    scatter.set_offsets(points_sorted)
    fig.canvas.draw()

# Initial smooth curve
cs = CubicSpline(x, y, bc_type='natural')
x_new = np.linspace(min(x), max(x), 500)
y_new = cs(x_new)
curve, = ax.plot(x_new, y_new, color='red')

# Draggable points
draggable_points = []
for i, (x_val, y_val) in enumerate(points):
    point, = ax.plot(x_val, y_val, 'bo', markersize=10)
    dp = DraggablePoint(point, points, update_curve, i)
    dp.connect()
    draggable_points.append(dp)

# Customize the layout
ax.set_title('Interactive Line Chart with Draggable Points')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.grid(True)

# Display the figure
plt.show()
