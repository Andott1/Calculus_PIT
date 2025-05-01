from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class LandingPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graphique.")
        self.setGeometry(100, 100, 800, 500)

        # Set purple background color for the entire window using AutoFillBackground
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#A020F0"))  # Set exact purple color
        self.setPalette(p)

        # Create and style the title label
        title_label = QLabel("Graphique", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Amaranth", 125, QFont.Bold))
        title_label.setStyleSheet("color: white;")

        # Tagline
        tagline_label = QLabel("Graph, Differentiate, Integrate —effortlessly.", self)
        tagline_label.setAlignment(Qt.AlignCenter)
        tagline_label.setFont(QFont("MOntserrat", 22))
        tagline_label.setStyleSheet("color: white;")

        # Button to switch to visualizer page with chic design
        visualizer_button = QPushButton("Try it now!")
        visualizer_button.setFont(QFont("Poppins", 18))
        visualizer_button.setStyleSheet("""
            QPushButton {
                background-color: white; 
                color: #A020F0; 
                padding: 15px 70px;
                border-radius: 12px; 
                font-size: 18px; 
                border: 2px solid #A020F0;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #A020F0;
                color: white;
                box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background-color: #8B00B2;
                color: white;
            }
        """)
        visualizer_button.clicked.connect(self.switchToVisualizer)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(tagline_label)  # Added tagline below title
        layout.addSpacing(50)
        layout.addWidget(visualizer_button, alignment=Qt.AlignCenter)

        # Center the layout contents
        layout.setAlignment(Qt.AlignCenter)

        # Set the layout for the window
        self.setLayout(layout)

    def switchToVisualizer(self):
        self.stacked_widget.setCurrentIndex(1)  # Switch to VisualizerPage
