import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from landingpage import LandingPage
from visualizerpage import VisualizerPage

class MainApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.stacked_widget = QStackedWidget()

        # Initialize pages
        self.landing_page = LandingPage(self.stacked_widget)
        self.visualizer_page = VisualizerPage(self.stacked_widget)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.landing_page)
        self.stacked_widget.addWidget(self.visualizer_page)

        self.stacked_widget.setCurrentIndex(0)  # Start with Landing Page
        self.stacked_widget.show()

if __name__ == "__main__":
    app = MainApp()
    sys.exit(app.exec_())
