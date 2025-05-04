import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation

class PlotWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(5, 4), dpi=100)
        super().__init__(self.figure)
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        
        # Add data cursor for interactive data points
        self.data_cursor = None
        self.annotation = None
        self._drag_start = None

        self.figure.canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.figure.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.figure.canvas.mpl_connect('button_release_event', self.on_release)

        
        # Store data for hover functionality
        self.x_data = None
        self.y_data = None

    def plot_function(self, x_vals, y_vals_list, dy_vals_list, int_vals, title="Function Visualization"):
        # Clear the figure before plotting
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        
        # Set modern style for the plot
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Set figure background color
        self.figure.patch.set_facecolor('white')
        self.ax.set_facecolor('white')
        
        # Plot the original function with better styling
        self.ax.plot(x_vals, y_vals_list[0], label='Original Function', 
                    color='#8E87F4', linewidth=2.5)
        
        # Store data for hover functionality
        self.x_data = x_vals
        self.y_data = y_vals_list[0]

        # Plot all derivatives with a color gradient
        colors = ['#FD8FD4', '#FF9E6D', '#74C7EC']
        for i in range(1, len(y_vals_list)):
            self.ax.plot(x_vals, y_vals_list[i], 
                        label=f'{i}th Derivative', 
                        color=colors[(i-1) % len(colors)],
                        linewidth=2, linestyle='--')

        # Plot the integral (if provided) with better styling
        if int_vals is not None:
            self.ax.plot(x_vals, int_vals, label='Integral', 
                        color='#6C5CE7', linewidth=2, linestyle=':')
            
            # Add shaded area under the original function
            self.shade_area_under_curve(x_vals, y_vals_list[0], color='#8E87F4', alpha=0.1)

        # Draw a horizontal and vertical line through the origin
        self.ax.axhline(0, color='#ddd', linewidth=0.8, zorder=0)
        self.ax.axvline(0, color='#ddd', linewidth=0.8, zorder=0)

        # Set title and labels with better styling
        self.ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        self.ax.set_xlabel("x", fontsize=12, fontweight='medium', labelpad=10)
        self.ax.set_ylabel("y", fontsize=12, fontweight='medium', labelpad=10)
        
        # Customize grid
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Customize ticks
        self.ax.tick_params(axis='both', which='major', labelsize=10)
        
        # Add subtle spines
        for spine in self.ax.spines.values():
            spine.set_visible(True)
            spine.set_color('#ddd')
            spine.set_linewidth(0.8)

        # Set legend properties with better styling
        legend = self.ax.legend(
            loc='upper right',
            fontsize=10,
            frameon=True,
            framealpha=0.95,
            facecolor='white',
            edgecolor='#ddd',
            borderpad=1,
            labelspacing=1.2
        )
        
        # Add a subtle shadow effect to the plot
        self.figure.tight_layout(pad=3.0)
        
        # Drawing the plot
        self.draw()

    def on_hover(self, event):
        # Only show data cursor if we're inside the axes
        if event.inaxes == self.ax and self.x_data is not None and self.y_data is not None:
            # Find the closest point
            x, y = event.xdata, event.ydata
            distances = np.sqrt((self.x_data - x)**2 + (self.y_data - y)**2)
            index = np.argmin(distances)
            
            # Only show if we're close enough to a point
            if distances[index] < 0.5:  # Adjust threshold as needed
                x_point, y_point = self.x_data[index], self.y_data[index]
                
                # Create or update annotation
                if self.annotation is None:
                    self.annotation = self.ax.annotate(
                        f"x: {x_point:.2f}\ny: {y_point:.2f}",
                        xy=(x_point, y_point),
                        xytext=(20, 20),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8, ec="#ddd"),
                        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3", color="#8E87F4")
                    )
                else:
                    self.annotation.xy = (x_point, y_point)
                    self.annotation.set_text(f"x: {x_point:.2f}\ny: {y_point:.2f}")
                    self.annotation.set_visible(True)
                    
                self.draw_idle()
            elif self.annotation is not None:
                self.annotation.set_visible(False)
                self.draw_idle()
    
    def on_scroll(self, event):
        base_scale = 1.1
        ax = self.ax

        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        x_range = (x_max - x_min)
        y_range = (y_max - y_min)

        xdata = event.xdata
        ydata = event.ydata

        if xdata is None or ydata is None:
            return

        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            scale_factor = 1

        new_width = x_range * scale_factor
        new_height = y_range * scale_factor

        relx = (xdata - x_min) / x_range
        rely = (ydata - y_min) / y_range

        ax.set_xlim([xdata - new_width * relx, xdata + new_width * (1 - relx)])
        ax.set_ylim([ydata - new_height * rely, ydata + new_height * (1 - rely)])
        self.draw_idle()

    def on_press(self, event):
        if event.button == 1 and event.inaxes == self.ax:  # Left click
            self._drag_start = (event.xdata, event.ydata)
            self._xlim_start = self.ax.get_xlim()
            self._ylim_start = self.ax.get_ylim()

    def on_drag(self, event):
        if self._drag_start and event.inaxes == self.ax:
            dx = event.xdata - self._drag_start[0]
            dy = event.ydata - self._drag_start[1]

            new_xlim = (self._xlim_start[0] - dx, self._xlim_start[1] - dx)
            new_ylim = (self._ylim_start[0] - dy, self._ylim_start[1] - dy)

            self.ax.set_xlim(new_xlim)
            self.ax.set_ylim(new_ylim)
            self.ax.figure.canvas.draw_idle()

    def on_release(self, event):
        self._drag_start = None

    def shade_area_under_curve(self, x_vals, y_vals, color='#8E87F4', alpha=0.2):
        """Add shaded area under the curve for better visualization of the integral."""
        # Create a polygon for the area under the curve
        zero_line = np.zeros_like(y_vals)
        self.ax.fill_between(x_vals, y_vals, zero_line, 
                            color=color, alpha=alpha, 
                            interpolate=True)
        self.draw_idle()

    def animate_plot(self, x_vals, y_vals_list, dy_vals_list, int_vals):
        """Create an animated transition when plotting."""
        # Clear the figure
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        
        # Set up the plot with styling
        plt.style.use('seaborn-v0_8-whitegrid')
        self.figure.patch.set_facecolor('white')
        self.ax.set_facecolor('white')
        
        # Set up empty lines
        lines = []
        line_original, = self.ax.plot([], [], label='Original Function', 
                                    color='#8E87F4', linewidth=2.5)
        lines.append(line_original)
        
        colors = ['#FD8FD4', '#FF9E6D', '#74C7EC']
        for i in range(1, len(y_vals_list)):
            line_deriv, = self.ax.plot([], [], 
                                    label=f'{i}th Derivative', 
                                    color=colors[(i-1) % len(colors)],
                                    linewidth=2, linestyle='--')
            lines.append(line_deriv)
        
        if int_vals is not None:
            line_integral, = self.ax.plot([], [], label='Integral', 
                                        color='#6C5CE7', linewidth=2, linestyle=':')
            lines.append(line_integral)
        
        # Set up axes and styling
        self.ax.axhline(0, color='#ddd', linewidth=0.8, zorder=0)
        self.ax.axvline(0, color='#ddd', linewidth=0.8, zorder=0)
        self.ax.set_title("Function Visualization", fontsize=14, fontweight='bold', pad=15)
        self.ax.set_xlabel("x", fontsize=12, fontweight='medium', labelpad=10)
        self.ax.set_ylabel("y", fontsize=12, fontweight='medium', labelpad=10)
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Set axis limits
        all_y_values = np.concatenate(y_vals_list)
        if int_vals is not None:
            all_y_values = np.concatenate([all_y_values, int_vals])
        
        y_min, y_max = np.min(all_y_values), np.max(all_y_values)
        y_range = y_max - y_min
        
        self.ax.set_xlim(np.min(x_vals), np.max(x_vals))
        self.ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)

        # Add shaded area under the integral curve (if integral data exists)
        self.shade_area_under_curve(x_vals, y_vals_list[0], color='#6C5CE7', alpha=0.1)
        
        # Add legend
        self.ax.legend(
            loc='upper left',
            fontsize=10,
            frameon=True,
            framealpha=0.5,
            facecolor='white',
            edgecolor='#ddd',
            borderpad=1,
            labelspacing=1.2
        )
        
        # Animation function
        def init():
            for line in lines:
                line.set_data([], [])
            return lines
        
        def animate(frame):
            # Calculate the number of points to show in this frame
            n_points = int((frame + 1) * len(x_vals) / 20)
            
            # Update each line with the data up to n_points
            lines[0].set_data(x_vals[:n_points], y_vals_list[0][:n_points])
            
            for i in range(1, len(y_vals_list)):
                lines[i].set_data(x_vals[:n_points], y_vals_list[i][:n_points])
            
            if int_vals is not None:
                lines[-1].set_data(x_vals[:n_points], int_vals[:n_points])
            
            return lines
        
        # Create animation
        ani = animation.FuncAnimation(
            self.figure, animate, frames=20, 
            init_func=init, blit=True, interval=50,
            repeat=False  # Animation stops after one full playthrough
        )
        
        # Store data for hover functionality
        self.x_data = x_vals
        self.y_data = y_vals_list[0]
        
        self.draw()
        return ani

    def save_plot(self, file_name):
        # Save the current figure as an image with higher quality
        self.figure.savefig(file_name, dpi=300, bbox_inches='tight')