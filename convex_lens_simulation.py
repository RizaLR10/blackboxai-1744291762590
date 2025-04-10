import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ConvexLensSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulasi Lensa Cembung")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input variables
        self.object_size = tk.DoubleVar(value=100)
        self.object_distance = tk.DoubleVar(value=300)
        self.focal_length = tk.DoubleVar(value=150)
        
        # Create input fields
        self.create_input_fields()
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, pady=10)
        
        # Initial plot
        self.update_plot()
        
    def create_input_fields(self):
        # Object size input
        ttk.Label(self.main_frame, text="Ukuran Benda (cm):").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.object_size, width=10).grid(row=0, column=1, pady=5)
        
        # Object distance input
        ttk.Label(self.main_frame, text="Jarak Benda (cm):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.object_distance, width=10).grid(row=1, column=1, pady=5)
        
        # Focal length input
        ttk.Label(self.main_frame, text="Titik Fokus Lensa (cm):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(self.main_frame, textvariable=self.focal_length, width=10).grid(row=2, column=1, pady=5)
        
        # Update button
        ttk.Button(self.main_frame, text="Update", command=self.update_plot).grid(row=3, column=0, columnspan=2, pady=10)
        
    def calculate_image(self):
        # Get values from input
        h = self.object_size.get()
        u = self.object_distance.get()
        f = self.focal_length.get()
        
        # Calculate image distance (v) using lens formula: 1/f = 1/u + 1/v
        v = (u * f) / (u - f)
        
        # Calculate image height using magnification formula: h'/h = -v/u
        h_image = -h * v / u
        
        return v, h_image
        
    def update_plot(self):
        self.ax.clear()
        
        # Get values
        u = self.object_distance.get()
        h = self.object_size.get()
        f = self.focal_length.get()
        v, h_image = self.calculate_image()
        
        # Set up the plot
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linestyle='-', linewidth=2)  # Lens line
        
        # Draw focal points
        self.ax.plot([-f, f], [0, 0], 'ko', label='Focal Points')
        self.ax.text(-f, -10, 'F', fontsize=12)
        self.ax.text(f, -10, 'F', fontsize=12)
        
        # Draw object
        self.ax.arrow(-u, 0, 0, h, head_width=5, head_length=10, fc='blue', ec='blue')
        
        # Draw image
        if v > 0:  # Real image
            self.ax.arrow(v, 0, 0, h_image, head_width=5, head_length=10, fc='red', ec='red')
        
        # Draw principal rays
        # Ray 1: Parallel to optical axis
        self.ax.plot([-u, 0], [h, h], 'r--')
        self.ax.plot([0, v], [h, h_image], 'r--')
        
        # Ray 2: Through focal point
        self.ax.plot([-u, 0], [h, 0], 'g--')
        self.ax.plot([0, v], [0, h_image], 'g--')
        
        # Set plot limits and labels
        max_x = max(abs(u), abs(v)) * 1.2
        max_y = max(abs(h), abs(h_image)) * 1.2
        self.ax.set_xlim(-max_x, max_x)
        self.ax.set_ylim(-max_y, max_y)
        
        # Add text showing calculations
        info_text = f'Jarak Bayangan = {v:.1f} cm\nUkuran Bayangan = {abs(h_image):.1f} cm'
        self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvexLensSimulation(root)
    root.mainloop()
