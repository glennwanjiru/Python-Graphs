import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

st.set_page_config(page_title="Interactive Graphs", layout="wide")

class DraggablePoint:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

# Sample data
x = [1.0, 2.0, 3.0, 4.0, 5.0]
y = [10.0, 11.0, 12.0, 13.0, 14.0]
points = [DraggablePoint(i, x[i], y[i]) for i in range(len(x))]

def update_curve():
    points_sorted = sorted(points, key=lambda p: p.x)
    x_sorted = [p.x for p in points_sorted]
    y_sorted = [p.y for p in points_sorted]
    cs = CubicSpline(x_sorted, y_sorted, bc_type='natural')
    x_new = np.linspace(min(x_sorted), max(x_sorted), 500)
    y_new = cs(x_new)
    return x_new, y_new

def plot_graph():
    fig, ax = plt.subplots()
    points_sorted = sorted(points, key=lambda p: p.x)
    x_sorted = [p.x for p in points_sorted]
    y_sorted = [p.y for p in points_sorted]
    
    ax.scatter(x_sorted, y_sorted, color='blue')
    x_new, y_new = update_curve()
    ax.plot(x_new, y_new, color='red')
    
    for p in points:
        ax.annotate(f"({p.x:.2f}, {p.y:.2f})", (p.x, p.y))
    
    ax.set_title('Interactive Line Chart with Draggable Points')
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.grid(True)
    
    st.pyplot(fig)

st.title("Interactive Graphs with Draggable Points")

col1, col2 = st.columns([3, 1])

with col1:
    st.header("Graph")
    plot_graph()

with col2:
    st.header("Adjust Points")
    for p in points:
        p.x = st.slider(f"X value of point {p.index}", 0.0, 10.0, float(p.x), 0.1)
        p.y = st.slider(f"Y value of point {p.index}", 0.0, 20.0, float(p.y), 0.1)

st.write("Drag the sliders to adjust the points and see the updated graph.")
