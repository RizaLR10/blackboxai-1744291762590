from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io
import base64
matplotlib.use('Agg')

app = Flask(__name__)

class ConvexLensSimulation:
    def __init__(self, object_size=100, object_distance=300, focal_length=150):
        self.object_size = object_size
        self.object_distance = object_distance
        self.focal_length = focal_length
        
    def calculate_image(self):
        h = self.object_size
        u = self.object_distance
        f = self.focal_length
        
        # Calculate image distance (v) using lens formula: 1/f = 1/u + 1/v
        v = (u * f) / (u - f)
        
        # Calculate image height using magnification formula: h'/h = -v/u
        h_image = -h * v / u
        
        return v, h_image
        
    def create_plot(self):
        plt.clf()
        
        # Get values
        u = self.object_distance
        h = self.object_size
        f = self.focal_length
        v, h_image = self.calculate_image()
        
        # Create figure with larger size and white background
        fig = plt.figure(figsize=(12, 8), facecolor='white')
        ax = fig.add_subplot(111)
        ax.set_facecolor('white')
        
        # Set up the plot
        plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        plt.axvline(x=0, color='k', linestyle='-', linewidth=2)  # Lens line
        
        # Draw focal points
        plt.plot([-f, f], [0, 0], 'ko')
        plt.text(-f, -10, 'F', fontsize=12)
        plt.text(f, -10, 'F', fontsize=12)
        
        # Draw object
        plt.arrow(-u, 0, 0, h, head_width=5, head_length=10, fc='blue', ec='blue', label='Objek')
        
        # Draw image
        if v > 0:  # Real image
            plt.arrow(v, 0, 0, h_image, head_width=5, head_length=10, fc='red', ec='red', label='Bayangan')
        
        # Draw principal rays
        # Ray 1: Parallel to optical axis
        plt.plot([-u, 0], [h, h], 'r--', alpha=0.6)
        plt.plot([0, v], [h, h_image], 'r--', alpha=0.6)
        
        # Ray 2: Through focal point
        plt.plot([-u, 0], [h, 0], 'g--', alpha=0.6)
        plt.plot([0, v], [0, h_image], 'g--', alpha=0.6)
        
        # Set plot limits and labels
        max_x = max(abs(u), abs(v)) * 1.2
        max_y = max(abs(h), abs(h_image)) * 1.2
        plt.xlim(-max_x, max_x)
        plt.ylim(-max_y, max_y)
        
        plt.title('Simulasi Lensa Cembung', pad=20, fontsize=14)
        plt.xlabel('Jarak (cm)', labelpad=10)
        plt.ylabel('Tinggi (cm)', labelpad=10)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Save plot to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf, v, h_image

@app.route('/')
def index():
    sim = ConvexLensSimulation()
    buf, v, h_image = sim.create_plot()
    image_base64 = base64.b64encode(buf.getvalue()).decode()
    
    return render_template('index.html', 
                         object_size=sim.object_size,
                         object_distance=sim.object_distance,
                         focal_length=sim.focal_length,
                         image_distance=f"{v:.1f}",
                         image_size=f"{abs(h_image):.1f}",
                         initial_image=f"data:image/png;base64,{image_base64}")

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        sim = ConvexLensSimulation()
    else:
        data = request.json
        sim = ConvexLensSimulation(
            object_size=float(data['object_size']),
            object_distance=float(data['object_distance']),
            focal_length=float(data['focal_length'])
        )
    
    buf, v, h_image = sim.create_plot()
    image_base64 = base64.b64encode(buf.getvalue()).decode()
    
    return jsonify({
        'image': f'data:image/png;base64,{image_base64}',
        'image_distance': f"{v:.1f}",
        'image_size': f"{abs(h_image):.1f}"
    })

if __name__ == '__main__':
    app.run(port=8000)
