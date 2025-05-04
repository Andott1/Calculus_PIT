import sys
import os
import glob
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                             QTabWidget, QFrame, QSizePolicy, QStackedWidget, QTextEdit, QStackedLayout, QDesktopWidget, QSpacerItem, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase, QLinearGradient, QBrush, QPainter, QPainterPath, QIcon, QPixmap, QCursor
from datetime import datetime
import numpy as np
import sympy as sp
from scipy.integrate import quad, cumulative_trapezoid
from graph import PlotWidget 

# -----------------------------------------------
# Resource Manager and Finder
# -----------------------------------------------

class AssetManager:
    def __init__(self):
        """
        Initialize the AssetManager with proper path resolution for both development
        and PyInstaller bundled environments.
        """
        # Base directories to check for assets
        self.asset_dirs = [
            "Assets/App Screenshots",
            "Assets/Fonts",
            "Assets/Icons",
            "Assets/Screens",
        ]
        
        # Map to cache resolved asset paths
        self.asset_cache = {}
        
        # Print the base directory for debugging
        print(f"Base directory: {self.get_base_dir()}")
        
        # Pre-scan assets to populate cache
        self.scan_assets()
    
    def get_base_dir(self):
        """
            the base directory for assets, handling both development and PyInstaller environments.
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            return sys._MEIPASS
        else:
        # When running normally (like python main.py)
            return os.path.dirname(os.path.abspath(__file__))
    
    def scan_assets(self):
        """
        Scan all asset directories and populate the asset cache.
        """
        base_dir = self.get_base_dir()
        print(f"Scanning assets in: {base_dir}")
        
        # Scan each asset directory
        for asset_dir in self.asset_dirs:
            full_dir_path = os.path.join(base_dir, asset_dir)
            
            if os.path.exists(full_dir_path):
                print(f"Found asset directory: {full_dir_path}")
                
                # Scan all files in this directory and subdirectories
                for root, _, files in os.walk(full_dir_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        # Get the relative path from the base directory
                        rel_path = os.path.relpath(full_path, base_dir)
                        # Store in cache with normalized path
                        normalized_path = rel_path.replace('\\', '/')
                        self.asset_cache[normalized_path] = full_path
                        
                        # Also store with simplified path (for robustness)
                        simple_path = os.path.join(asset_dir, file).replace('\\', '/')
                        self.asset_cache[simple_path] = full_path
                        
                        print(f"Cached asset: {normalized_path} -> {full_path}")
            else:
                print(f"Asset directory not found: {full_dir_path}")
        
        print(f"Total assets cached: {len(self.asset_cache)}")
        
        # Try to find assets with recursive glob pattern (fallback method)
        self.find_assets_with_glob()
    
    def find_assets_with_glob(self):
        """
        Use glob to find assets recursively as a fallback method.
        """
        base_dir = self.get_base_dir()
        
        # Search for all files in the Assets directory
        for pattern in ["Assets/**/*.*", "Assets/*.*"]:
            for file_path in glob.glob(os.path.join(base_dir, pattern), recursive=True):
                if os.path.isfile(file_path):
                    # Get filename
                    filename = os.path.basename(file_path)
                    # Add to cache with just the filename as key (most permissive)
                    self.asset_cache[filename] = file_path
                    
                    # Also add with partial path
                    rel_path = os.path.relpath(file_path, base_dir)
                    self.asset_cache[rel_path.replace('\\', '/')] = file_path
    
    def resolve_asset(self, asset_path):
        """
        Resolve an asset path to its full path, handling both development and PyInstaller environments.
        
        Args:
            asset_path (str): The relative path to the asset (e.g., "Assets/Fonts/Roboto.ttf")
            
        Returns:
            str: The full path to the asset, or None if not found
        """
        # Normalize the path
        normalized_path = asset_path.replace('\\', '/')
        
        # Check if the asset is in the cache
        if normalized_path in self.asset_cache:
            return self.asset_cache[normalized_path]
        
        # Try with just the filename
        filename = os.path.basename(normalized_path)
        if filename in self.asset_cache:
            return self.asset_cache[filename]
        
        # If not in cache, try direct resolution
        base_dir = self.get_base_dir()
        full_path = os.path.join(base_dir, normalized_path)
        
        if os.path.exists(full_path):
            # Add to cache for future lookups
            self.asset_cache[normalized_path] = full_path
            return full_path
        
        # Try to find the file by searching all subdirectories
        for root, _, files in os.walk(base_dir):
            if filename in files:
                full_path = os.path.join(root, filename)
                self.asset_cache[normalized_path] = full_path
                return full_path
        
        # Asset not found
        print(f"Asset not found: {asset_path}")
        return None
    
    def load_asset(self, asset_path):
        """
        Resolve and return the full path to an asset.
        
        Args:
            asset_path (str): The relative path to the asset
            
        Returns:
            str: The full path to the asset, or None if not found
        """
        return self.resolve_asset(asset_path)
    
    def load_pixmap(self, image_path):
        """
        Load an image as a QPixmap, with robust error handling.
        
        Args:
            image_path (str): The relative path to the image
            
        Returns:
            QPixmap: The loaded pixmap, or an empty pixmap if loading failed
        """
        resolved_path = self.resolve_asset(image_path)
        if not resolved_path:
            print(f"Image not found: {image_path}")
            return QPixmap()
        
        pixmap = QPixmap(resolved_path)
        if pixmap.isNull():
            print(f"Failed to load image as pixmap: {resolved_path}")
            
            # Try alternative paths
            filename = os.path.basename(image_path)
            for key, path in self.asset_cache.items():
                if filename in key and key != image_path:
                    print(f"Trying alternative path: {path}")
                    alt_pixmap = QPixmap(path)
                    if not alt_pixmap.isNull():
                        return alt_pixmap
            
            return QPixmap()
        
        return pixmap
    
    def load_fonts(self):
        """
        Load all fonts in the Fonts directory.
        
        Returns:
            list: A list of loaded font family names
        """
        loaded_families = []
        font_dir = os.path.join(self.get_base_dir(), "Assets", "Fonts")
        
        if not os.path.exists(font_dir):
            print(f"Font directory not found: {font_dir}")
            # Try to find fonts using the asset cache
            for key, path in self.asset_cache.items():
                if "Fonts" in key and path.lower().endswith(('.ttf', '.otf')):
                    font_id = QFontDatabase.addApplicationFont(path)
                    if font_id != -1:
                        families = QFontDatabase.applicationFontFamilies(font_id)
                        print(f"Loaded font: {path} → {families}")
                        loaded_families.extend(families)
                    else:
                        print(f"Failed to load font: {path}")
            
            return loaded_families
        
        print(f"Loading fonts from: {font_dir}")
        
        # Find all font files
        font_files = []
        for ext in ['.ttf', '.otf']:
            font_files.extend(glob.glob(os.path.join(font_dir, f"**/*{ext}"), recursive=True))
        
        # Load each font
        for font_path in font_files:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"Loaded font: {font_path} → {families}")
                loaded_families.extend(families)
            else:
                print(f"Failed to load font: {font_path}")
        
        return loaded_families
    
    def get_font_dir(self):
        """
        Get the directory containing fonts.
        
        Returns:
            str: The full path to the fonts directory, or None if not found
        """
        font_dir = "Assets/Fonts"
        resolved = self.resolve_asset(font_dir)
        if resolved:
            return os.path.dirname(resolved)
        
        # Fallback: try to find any font file and return its directory
        for key, path in self.asset_cache.items():
            if "Fonts" in key and os.path.exists(path):
                return os.path.dirname(path)
        
        # Last resort: return the base Assets directory
        return os.path.join(self.get_base_dir(), "Assets")

# Create a singleton instance
asset_manager = AssetManager()
    
# -----------------------------------------------
# Custom Widgets
# -----------------------------------------------

class RoundedWidget(QWidget):
    def __init__(self, parent=None, radius=20, bg_color="#FFFFFF"):
        super().__init__(parent)
        self.radius = radius
        self.bg_color = bg_color
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), self.radius, self.radius)
        
        painter.setClipPath(path)
        painter.fillPath(path, QBrush(QColor(self.bg_color)))


class CircleButtonBack(QPushButton):
    def __init__(self, parent=None, on_back_pressed=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)

        icon_path = asset_manager.load_asset("Assets/Icons/back_icon.png")
        icon = QIcon(icon_path)
        if icon.isNull():
            print(f"Failed to load icon: {icon_path}")
        else:
            self.setIcon(icon)

        icon_size = self.size() * 0.5
        self.setIconSize(icon_size)

        self.setStyleSheet("""
            QPushButton {
                background-color: #9191DC;
                border-radius: 25px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7777B2;
            }
            QPushButton:pressed {
                background-color: #55557D;
            }
        """)

        if on_back_pressed:
            self.clicked.connect(on_back_pressed)

class CircleButtonInfo(QPushButton):
    def __init__(self, parent=None, on_info_pressed=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        
        icon_path = asset_manager.load_asset("Assets/Icons/group_icon.png")  # Ensure this points to the correct image path
        icon = QIcon(icon_path)
        print(f"Resolved icon path: {icon_path}")
        if icon.isNull():
            print(f"Failed to load icon: {icon_path}")
        else:
            self.setIcon(icon)
        
        icon_size = self.size() * 0.4  # 40% of button size
        self.setIconSize(icon_size)

        self.setStyleSheet("""
            QPushButton {
                background-color: #9191DC;
                border-radius: 25px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7777B2;
            }
            QPushButton:pressed {
                background-color: #55557D;
            }
        """)

        if on_info_pressed:
            self.clicked.connect(on_info_pressed)

# -----------------------------------------------
# Main Application
# -----------------------------------------------

class GraphiqueApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Graphique')
        self.resize_window_to_percentage()
        self.center_window()
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Outer container with rounded corners
        outer_container = RoundedWidget(radius=30, bg_color=QColor(255, 255, 255, 250))
        outer_layout = QVBoxLayout(outer_container)
        outer_layout.setContentsMargins(30, 30, 30, 30)
        outer_layout.setSpacing(25)
        main_layout.addWidget(outer_container)
        
        # Top Section (Back Button, Title, and DateTime)
        top_layout = self.create_top_section()
        outer_layout.addLayout(top_layout)
        
        # Content Section (Left and Right Panels)
        content_layout = self.create_content_section()
        outer_layout.addLayout(content_layout, 1)

        # Set image background for the main window
        self.setAutoFillBackground(True)
        
        self.set_image_background(asset_manager.load_asset("Assets/Screens/main_screen.png"))

    def resize_window_to_percentage(self):
        # Get the screen's dimensions
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Define window size as a percentage of the screen size
        window_width_percentage = 0.75  # 75% of the screen width
        window_height_percentage = 0.8  # 80% of the screen height

        # Calculate window's size based on the percentages
        window_width = int(screen_width * window_width_percentage)
        window_height = int(screen_height * window_height_percentage)

        # Set initial window size but allow manual resizing
        self.resize(window_width, window_height)

        if hasattr(self, 'plot_widget'):
            min_plot_width = int(window_width * 0.5)
            min_plot_height = int(window_height * 0.75)
            self.plot_widget.setMinimumWidth(min_plot_width)
            self.plot_widget.setMinimumHeight(min_plot_height)

    def center_window(self):
        # Get the screen's dimensions
        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()

        # Get the window's current size after it is shown
        window_width = self.frameGeometry().width()
        window_height = self.frameGeometry().height()

        # Calculate the top-left position to center the window
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2

        # Move the window to the calculated position
        self.move(x_pos, y_pos)
    
    def create_top_section(self):
        top_layout = QHBoxLayout()
        top_layout.setSpacing(25)

        # Back button (circle)
        self.back_button = CircleButtonBack(on_back_pressed=self.back_to_splash)
        top_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # Title section
        title_widget = QWidget()
        title_widget.setStyleSheet("background-color: rgba(200, 200, 200, 0); border-radius: 10px;")
        title_layout = QVBoxLayout(title_widget)
        title_layout.setAlignment(Qt.AlignVCenter)
        
        title_label = QLabel("GRAPHIQUE")
        title_label.setFont(QFont("Roboto Condensed", 24, QFont.ExtraBold))
        title_label.setStyleSheet("color: #55557D;")  # Replace with your desired color
        title_label.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(title_label)
        top_layout.addWidget(title_widget, 1)

        # DateTime section
        datetime_widget = self.create_datetime_section()
        top_layout.addWidget(datetime_widget, alignment=Qt.AlignRight)

        # Info button (circle)
        self.info_button = CircleButtonInfo(on_info_pressed=self.show_info_dialog)
        top_layout.addWidget(self.info_button, alignment=Qt.AlignCenter)
        
        return top_layout

    def create_datetime_section(self):
        datetime_widget = QWidget()
        datetime_widget.setStyleSheet("background-color: rgba(200, 200, 200, 0); border-radius: 10px;")
        datetime_layout = QVBoxLayout(datetime_widget)
        datetime_layout.setContentsMargins(10, 5, 10, 5)
        datetime_layout.setAlignment(Qt.AlignCenter)

        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont("Roboto", 14, QFont.Medium))
        self.datetime_label.setStyleSheet("color: #55557D;")
        self.datetime_label.setAlignment(Qt.AlignCenter)

        self.datetime_timer = QTimer()
        self.datetime_timer.timeout.connect(self.update_datetime)
        self.datetime_timer.start(1000)
        self.update_datetime()

        datetime_layout.addWidget(self.datetime_label)
        
        return datetime_widget
    
    def create_content_section(self):
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)
        
        # Left Panel (controls)
        left_panel = self.create_left_panel()
        content_layout.addWidget(left_panel, 1)

        # Right Panel (graph and details tabs)
        right_panel = self.create_right_panel()
        content_layout.addWidget(right_panel, 2)
        
        return content_layout
    
    def create_left_panel(self):
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: rgba(145, 145, 220, 0.25); border-radius: 20px;")
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.setSpacing(25)
        left_layout.setContentsMargins(15, 15, 15, 15)

        control_panel = self.create_control_panel()
        control_panel.setStyleSheet("background-color: rgba(145, 145, 220, 0.9); border-radius: 20px;")
        left_layout.addWidget(control_panel)
        left_layout.addStretch()

        return left_panel

    def create_control_panel(self):
        control_panel = RoundedWidget(radius=20)
        control_layout = QVBoxLayout(control_panel)
        control_layout.setContentsMargins(20, 20, 20, 20)
        control_layout.setSpacing(10)

        # Function input
        function_label = QLabel("  Enter Function")
        function_label.setFont(QFont("Roboto", 18, QFont.Bold))
        function_label.setStyleSheet("color: #55557D; background-color: rgba(145, 145, 220, 0)")
        control_layout.addWidget(function_label)
        
        function_input = self.create_input_field("Enter function (e.g., x**2 + 2*x)", "Enter Function")
        self.function_input = function_input
        control_layout.addWidget(function_input)

        control_layout.addSpacing(15)

        # X-Range inputs
        range_label = QLabel("  X-Range (min, max)")
        range_label.setFont(QFont("Roboto", 18, QFont.Bold))
        range_label.setStyleSheet("color: #55557D; background-color: rgba(145, 145, 220, 0)")
        control_layout.addWidget(range_label)

        range_layout = self.create_range_inputs()
        control_layout.addLayout(range_layout)

        control_layout.addSpacing(15)

        # Derivative order input
        derivative_label = QLabel("  Derivative Order")
        derivative_label.setFont(QFont("Roboto", 18, QFont.Bold))
        derivative_label.setStyleSheet("color: #55557D; background-color: rgba(145, 145, 220, 0)")
        control_layout.addWidget(derivative_label)

        derivative_input = self.create_input_field("Enter derivative order (e.g., 1)", "Derivative Order")
        self.derivative_input = derivative_input
        control_layout.addWidget(derivative_input)

        control_layout.addSpacing(10)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setFixedHeight(4)  # Fixed Height
        separator.setFixedWidth(300)  # Fixed Width

        separator.setStyleSheet("""
            QFrame {
                border-radius: 2px;
                color: #666666;          /* Line color (used for shadows) */
                background-color: rgba(145, 145, 220, 0.25); /* Actual line color */
            }
        """)

        control_layout.addWidget(separator)
        
        control_layout.setAlignment(separator, Qt.AlignHCenter)

        control_layout.addSpacing(10)

        # Buttons
        buttons_layout = self.create_buttons_layout()
        control_layout.addLayout(buttons_layout)

        control_layout.addSpacing(10)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setFixedHeight(4)  # Fixed Height
        separator.setFixedWidth(300)  # Fixed Width

        separator.setStyleSheet("""
            QFrame {
                border-radius: 2px;
                color: #666666;          /* Line color (used for shadows) */
                background-color: rgba(145, 145, 220, 0.25); /* Actual line color */
            }
        """)

        control_layout.addWidget(separator)
        
        control_layout.setAlignment(separator, Qt.AlignHCenter)

        control_layout.addSpacing(10)

        # Switch Button
        toggle_button = self.create_toggle_button()
        control_layout.addWidget(toggle_button)

        return control_panel

    def create_input_field(self, placeholder, label): # Function input fields styling
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet("""
            QLineEdit {
                border-radius: 10px;
                padding: 10px;
                background-color: rgba(145, 145, 220, 0.25);
                font-family: 'Roboto Medium';
                font-size: 12px;
                color: #7777B2; /* <-- Font color */
            }
                                  
            QLineEdit:focus {
                font-family: 'Roboto Light';
                font-size: 12px;
                border: 2px solid #7777B2; /* Blue border on focus */
                background-color: rgba(145, 145, 220, 0.15); /* Optional light background */
            }
        """)
        input_field.setMinimumHeight(40)
        return input_field

    def create_range_inputs(self): # X-range input fields styling
        range_layout = QHBoxLayout()
        range_layout.setSpacing(15)

        min_input = self.create_input_field("Min (e.g., -10)", "Min")
        max_input = self.create_input_field("Max (e.g., 10)", "Max")

        # Store input fields as instance attributes for later access
        self.x_min_entry = min_input
        self.x_max_entry = max_input

        range_layout.addWidget(min_input)
        range_layout.addWidget(max_input)

        return range_layout
    
    def create_buttons_layout(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        plot_button = self.create_button("PLOT")
        plot_button.clicked.connect(self.plot)
        save_button = self.create_button("Save Graph")
        save_button.clicked.connect(self.save_plot)
        
        buttons_layout.addWidget(plot_button)
        buttons_layout.addWidget(save_button)

        return buttons_layout

    def create_button(self, text): # Plot, Save Graph buttons styling
        button = QPushButton(text)

        button.setStyleSheet("""
            QPushButton {
                background-color: #9191DC;
                color: white;
                border-radius: 20px;
                padding: 10px;
                font-family: 'Roboto Black';
                font-size: 20px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #7777B2;
            }
            QPushButton:pressed {
                background-color: #55557D;
            }
        """)
        return button

    def create_right_panel(self):
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: rgba(145, 145, 220, 0.25); border-radius: 10px;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(15, 15, 15, 15)

        stacked_widget = self.create_stacked_widget()
        right_layout.addWidget(stacked_widget)

        return right_panel

    def create_stacked_widget(self):
        stacked_widget = QStackedWidget()

        # Create the layout for the graph_tab
        graph_tab = QWidget()
        graph_tab.setStyleSheet("background-color: #FFFFFF;")
        graph_layout = QVBoxLayout(graph_tab)
        self.plot_widget = PlotWidget()
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add the graph box to the graph tab layout
        graph_layout.addWidget(self.plot_widget)
        
        # Add the graph tab to the stacked widget
        stacked_widget.addWidget(graph_tab)

        details_tab = QWidget()
        details_tab.setStyleSheet("background-color: #FFFFFF;")
        
        # Create the layout for the details_tab
        details_layout = QVBoxLayout(details_tab)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Function details will appear here...")
        self.result_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_box.setStyleSheet("""
            background-color: #FFFFFF;
            padding: 0px;
            border: none;
            font-size: 14px;
            font-family: 'Roboto';
            color: #333;
        """)

        # Add the result box to the details tab layout
        details_layout.addWidget(self.result_box)

        # Add the details tab to the stacked widget
        stacked_widget.addWidget(details_tab)

        return stacked_widget

    def create_toggle_button(self): # Switch to graph or details button styling
        toggle_button = QPushButton("Switch to Details")
        toggle_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(145, 145, 220, 0.25);
                color: #7777B2;
                border-radius: 20px;
                padding: 10px;
                font-family: 'Roboto ExtraBold';
                font-size: 20px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: rgba(145, 145, 220, 0.5);
                color: #55557D;
            }
            QPushButton:pressed {
                background-color: #7777B2;
            }
        """)
        toggle_button.clicked.connect(self.toggle_view)
        return toggle_button

    def toggle_view(self):      # Switch to graph or details button logic
        stacked_widget = self.findChild(QStackedWidget)
        current_index = stacked_widget.currentIndex()
        new_index = 1 - current_index
        stacked_widget.setCurrentIndex(new_index)

        toggle_button = self.sender()
        if new_index == 0:
            toggle_button.setText("Switch to Details")
        else:
            toggle_button.setText("Switch to Graph")

    def update_datetime(self):  # Date time update realtime
        current_time = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")
        self.datetime_label.setText(current_time)
    
    def back_to_splash(self):   # Back button logic
        self.close()
        self.splash = SplashScreen()
        self.splash.show()

    def show_info_dialog(self): # Info button logic
        QMessageBox.information(
            self,
            "Group Members",
            """
            <span style="font-size: 18px; font-weight: bold; color: #333;">GROUP MEMBERS:</span><br><br>
            <span style="font-size: 16px; font-weight: normal; color: #333;">1. Kurt Andre Olaer</span><br>
            <span style="font-size: 16px; font-weight: normal; color: #333;">2. James Dominic Tion</span><br>
            <span style="font-size: 16px; font-weight: normal; color: #333;">3. Mariel Laplap</span><br>
            <span style="font-size: 16px; font-weight: normal; color: #333;">4. Gwynette Galleros</span><br>
            <span style="font-size: 16px; font-weight: normal; color: #333;">5. Yasser Tomawis</span>
            """,
            QMessageBox.Ok
        )
    

    # Main app background logic 1
    def set_image_background(self, image_path): 
        self.image_path = image_path
        self.update_background()


    # Main app background logic 2
    def update_background(self):    
        palette = self.palette()
        pixmap = QPixmap(self.image_path)
        
        # Scale the image based on the current window size
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        
        # Set the image as the background
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)


    # Update the image background whenever the window is resized
    def resizeEvent(self, event):
        self.update_background()
        super().resizeEvent(event)


    # Reading the function input logic
    def parse_function(self, func_str):
        x = sp.Symbol('x')
        try:
            func = sp.sympify(func_str)
            return func, x
        except sp.SympifyError:
            self.warning(warning="Invalid function syntax.\nExample: 3*x**2 + 2*x - 4")
            return None, None
    

    # Translates derivative function logic
    def numerical_derivative(self, func, x_val, dx=1e-5):
        return (func.subs('x', x_val + dx).evalf() - func.subs('x', x_val - dx).evalf()) / (2 * dx)
    

    # Plotting of graph logic
    def plot(self):
        func_str = self.function_input.text()
        try:
            x_min = float(self.x_min_entry.text())
            x_max = float(self.x_max_entry.text())
        except ValueError:
            self.warning(warning="Invalid range input.")
            return
        
        func, x = self.parse_function(func_str)
        if func is None:
            return

        # Get the derivative order from the input
        try:
            derivative_order = int(self.derivative_input.text())
        except ValueError:
            self.warning(warning="Invalid derivative order input.")
            return

        # List to store all derivatives and their numerical values
        derivatives = [func]
        x_vals = np.linspace(x_min, x_max, 400)

        # Initialize lists for the values of the function and its derivatives
        y_vals_list = []
        dy_vals_list = []

        # Calculate the original function's values for each x_val
        y_vals_list.append(np.array([float(func.subs(x, val).evalf()) for val in x_vals], dtype=np.float64))
        dy_vals_list.append(np.array([self.numerical_derivative(func, val) for val in x_vals], dtype=np.float64))

        # Calculate derivatives from 1 up to the desired order and add them to lists
        for i in range(1, derivative_order + 1):
            func_diff = sp.diff(derivatives[-1], x)  # Calculate next derivative
            derivatives.append(func_diff)

            # Calculate the numerical values for the derivative
            dy_vals = np.array([self.numerical_derivative(derivatives[i], val) for val in x_vals], dtype=np.float64)
            dy_vals_list.append(dy_vals)

            # Also add the values for the current derivative
            y_vals_list.append(np.array([float(derivatives[i].subs(x, val).evalf()) for val in x_vals], dtype=np.float64))

        # Calculate the symbolic integral of the original function
        func_integral = sp.integrate(func, x)
        
        # Calculate the integral values
        int_vals = cumulative_trapezoid(y_vals_list[0], x_vals, initial=0)

        # Update the result box with the original function, derivatives, and integral
        derivative_text = ""
        for i in range(1, derivative_order + 1):
            if i < derivative_order:
                derivative_text += f"<b>Derivative [{i}]</b>:<br>  f^{i}(x) = {sp.simplify(derivatives[i])}<br><br>"
            else:
                derivative_text += f"<b>Derivative [{i}]</b>:<br>  f^{i}(x) = {sp.simplify(derivatives[i])}"

        # Simplify the function and derivative text
        simplified_func = sp.simplify(func)
        simplified_integral = sp.simplify(func_integral)

        # Convert the expression to string and replace symbols
        formatted_func = str(simplified_func).replace('**', '^').replace('*', '')
        formatted_integral = str(simplified_integral).replace('**', '^').replace('*', '')

        # Construct the derivative text similarly, if applicable
        derivative_text = derivative_text.replace('**', '^').replace('*', '')

        # Set the result box styles
        self.result_box.setStyleSheet("QTextEdit { padding: 0px; margin: 0px; }")  # Remove padding and margin from QTextEdit

        # Set the contents for result box with HTML styling
        self.result_box.setHtml(
            f"""
            <div style="line-height: 1.6; color: #333; font-family: 'Roboto'; margin: 0; padding: 0;">
                <!-- Original Function -->
                <div style="color: #55557D; font-size: 26px; font-weight: bold; margin-bottom: 5px;">Original Function:</div>
                <div style="color: #55557D; font-size: 22px; margin-left: 15px; margin-top: 0;">f(x) = {formatted_func}</div>

                <!-- Derivatives -->
                <div style="color: #55557D; font-size: 26px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;">Derivatives:</div>
                <div style="color: #55557D; margin-left: 15px; font-size: 22px; margin-top: 0;">{derivative_text}</div>

                <!-- Integral -->
                <div style="color: #55557D; font-size: 26px; font-weight: bold; margin-top: 15px; margin-bottom: 5px;">Integral:</div>
                <div style="color: #55557D; margin-left: 15px; font-size: 22px; margin-top: 0;">∫f(x)dx = {formatted_integral} + C</div>
            </div>
            """
        )

        # Plot the original function and all derivatives
        self.plot_widget.animate_plot(x_vals, y_vals_list, dy_vals_list, int_vals)


    # Save current graph as image
    def save_plot(self):
        """Opens a file dialog to save the plot as an image."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)", options=options)
        
        if file_name:
            self.plot_widget.save_plot(file_name)
            print(f"Plot saved as: {file_name}")


    # Warning popup box
    def warning(self, warning):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(warning)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec() 


# Splash screen logic
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.load_custom_font()
        self.setWindowTitle("Welcome to Graphique")
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Center and scale window to percent of screen
        screen_geometry = QDesktopWidget().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        window_width = int(screen_width * 0.55)
        window_height = int(screen_height * 0.6)

        self.setFixedSize(window_width, window_height)

        # Load and scale splash image
        splash_path = asset_manager.load_asset("Assets/Screens/splash_screen.png")
        splash_image = QPixmap(splash_path)

        if splash_image.isNull():
            print(f"Failed to load image: {splash_path}")
        else:
            print("Splash screen image loaded successfully.")

        scaled_image = splash_image.scaled(window_width, window_height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        # Image label (background)
        self.image_label = QLabel(self)
        self.image_label.setPixmap(scaled_image)
        self.image_label.setGeometry(0, 0, window_width, window_height)
        self.image_label.setScaledContents(True)

        # Overlay layout on top of image
        overlay_layout = QVBoxLayout(self)
        overlay_layout.setContentsMargins(20, 20, 20, 50)
        overlay_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Start button
        self.start_button = QPushButton("Start Graphing", self)
        button_width = int(screen_width * 0.125)
        button_height = int(screen_height * 0.075)
        self.start_button.setFixedSize(button_width, button_height)
        self.start_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_button.setVisible(False)
        self.start_button.clicked.connect(self.launch_main)

        # Button styling
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(145, 145, 220, 0.5);
                color: #FFFFFF;
                border-radius: 20px;
                padding: 10px;
                font-family: 'Roboto ExtraBold';
                font-size: 20px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: rgba(145, 145, 220, 0.75);
                color: #55557D;
            }
            QPushButton:pressed {
                background-color: #7777B2;
            }
        """)

        overlay_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.setLayout(overlay_layout)

        QTimer.singleShot(1000, self.animate_button)


    # Loads custom font in Assets/Fonts folder
    def load_custom_font(self):
        font_dir = asset_manager.load_asset("Assets/Fonts")
        if not font_dir or not os.path.exists(font_dir):
            print(f"Font directory not found: {font_dir}")
            return

        print(f"Loading fonts from: {font_dir}")
        loaded_families = []

        # Use glob to find all .ttf files recursively
        font_paths = glob.glob(os.path.join(font_dir, '**', '*.ttf'), recursive=True)

        for font_path in font_paths:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"Loaded font: {font_path} → {families}")
                loaded_families.extend(families)
            else:
                print(f"Failed to load font: {font_path}")

        if loaded_families:
            font = QFont(loaded_families[0])
            QApplication.setFont(font)
            print(f"Application font set to: {loaded_families[0]}")
        else:
            print("No fonts were loaded.")


    # Simple button animation
    def animate_button(self):
        self.start_button.setVisible(True)
        self.start_button.update()

        self.anim = QPropertyAnimation(self.start_button, b"geometry")
        self.anim.setDuration(500)
        self.anim.setStartValue(QRect(
            self.start_button.x(),
            self.start_button.y() + 50,
            self.start_button.width(),
            self.start_button.height()
        ))
        self.anim.setEndValue(self.start_button.geometry())
        self.anim.setEasingCurve(QEasingCurve.OutBack)
        self.anim.start()


    # Splash screen show logic
    def launch_main(self):
        self.close()
        self.main = GraphiqueApp()
        self.main.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())