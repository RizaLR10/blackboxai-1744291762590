import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

class ConvexLensSimulation:
    def __init__(self):
        # Default values
        self.object_size = 100
        self.object_distance = 300
        self.focal_length = 150
        
    def calculate_image(self):
        # Get values
        h = self.object_size
        u = self.object_distance
        f = self.focal_length
        
        # Calculate image distance (v) using lens formula: 1/f = 1/u + 1/v
        v = (u * f) / (u - f)
        
        # Calculate image height using magnification formula: h'/h = -v/u
        h_image = -h * v / u
        
        return v, h_image
        
    def create_plot(self):
        # Clear previous plot
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
        
        # Add text showing calculations
        info_text = f'Jarak Bayangan = {v:.1f} cm\nUkuran Bayangan = {abs(h_image):.1f} cm'
        plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.title('Simulasi Lensa Cembung', pad=20, fontsize=14)
        plt.xlabel('Jarak (cm)', labelpad=10)
        plt.ylabel('Tinggi (cm)', labelpad=10)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Save plot with high DPI for better quality
        plt.savefig('lens_simulation.png', dpi=300, bbox_inches='tight')
        
        # Create HTML file with the image and input form
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Simulasi Lensa Cembung</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Inter', sans-serif; }}
            </style>
        </head>
        <body class="bg-gray-50 p-8">
            <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8">
                <h1 class="text-3xl font-bold text-center mb-8 text-gray-800">Simulasi Lensa Cembung</h1>
                
                <div class="mb-8">
                    <img src="lens_simulation.png" alt="Lens Simulation" class="w-full rounded-lg shadow-md">
                </div>
                
                <form id="simulationForm" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Ukuran Benda (cm):</label>
                        <input type="number" id="objectSize" value="{self.object_size}" min="1" 
                               class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Jarak Benda (cm):</label>
                        <input type="number" id="objectDistance" value="{self.object_distance}" min="1"
                               class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    
                    <div class="space-y-2">
                        <label class="block text-sm font-semibold text-gray-700">Titik Fokus (cm):</label>
                        <input type="number" id="focalLength" value="{self.focal_length}" min="1"
                               class="w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                </form>
                
                <div class="bg-blue-50 rounded-xl p-6">
                    <h2 class="text-xl font-semibold mb-4 text-blue-900">Hasil Perhitungan:</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-white rounded-lg p-4 shadow-sm">
                            <p class="text-sm text-gray-600">Jarak Bayangan:</p>
                            <p class="text-2xl font-semibold text-blue-600">{v:.1f} cm</p>
                        </div>
                        <div class="bg-white rounded-lg p-4 shadow-sm">
                            <p class="text-sm text-gray-600">Ukuran Bayangan:</p>
                            <p class="text-2xl font-semibold text-blue-600">{abs(h_image):.1f} cm</p>
                        </div>
                    </div>
                </div>
                
                <div class="mt-8 text-center text-sm text-gray-600">
                    <p>Klik refresh halaman untuk melihat perubahan setelah mengubah nilai input.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open('lens_simulation.html', 'w') as f:
            f.write(html_content)

# Create simulation and generate plot
sim = ConvexLensSimulation()
sim.create_plot()
