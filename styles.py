# Modern styles for Function Visualizer (Graphique)

style = """
QWidget {
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    font-size: 10pt;
}

/* Style for the horizontal spacing for components */
QSpacerItem {
    height: 12px;
}

/* Style for error messages */
QMessageBox {
    font-size: 14px;
    background-color: #f8d7da;
    color: #721c24;
    border-radius: 8px;
    padding: 15px;
}
"""

main_panel_style = """
    QWidget {
        margin: 0;
        padding: 20px; 
        background-color: #f8f9fa;
    }
"""

header_panel_style = """
    QWidget {
        border: none;
        border-radius: 12px;
        padding: 15px;
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #8E87F4, stop: 1 #FD8FD4
        );
    }

    QLabel {
        font-size: 26px;
        font-weight: bold;
        color: white;
        margin: 10px 0;
        text-align: center;
    }
"""

left_panel_style = """
    QVBoxLayout {
        margin: 0;
        padding: 20px; 
    }

    QWidget[for="left-widget"] {
        border-radius: 12px;
        padding: 20px;
        background-color: white;
        border: 1px solid #e9ecef;
    }

    QLabel[for="function-label"], QLabel[for="derivative-order-label"], QLabel[for="x-range-label"] {
        font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
        font-size: 16px;
        font-weight: bold;
        padding: 5px 0;
        color: #495057;
    }   

    QLabel[for="func-help-icon"], QLabel[for="deriv-help-icon"] {
        color: #8E87F4;
        border-radius: 10px;
        font-size: 14px;
        font-weight: bold;
        padding: 5px;
    }

    QLabel[for="func-help-icon"]:hover, QLabel[for="deriv-help-icon"]:hover {
        background-color: rgba(142, 135, 244, 0.1);
    }

    QLineEdit {
        font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
        font-size: 14px;
        padding: 10px;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        margin-bottom: 15px;
        background-color: #f8f9fa;
    }

    QLineEdit:focus {
        border-color: #8E87F4;
        background-color: white;
    }
    
    QLineEdit::placeholder {
        font-size: 13px;
        color: #adb5bd;
    }

    QPushButton[for="plot-button"] {
        font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
        font-size: 16px;
        padding: 12px;
        border-radius: 8px;
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #8E87F4, stop: 1 #FD8FD4
        );
        color: white;
        font-weight: bold;
        margin: 5px 0;
        border: none;
    }

    QPushButton:hover[for="plot-button"] {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #7A74E0, stop: 1 #E97CC0
        );
    }

    QPushButton:pressed[for="plot-button"] {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #6A64D0, stop: 1 #D96CB0
        );
    }

    QPushButton[for="save-plot-button"] {
        font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
        font-size: 14px;
        color: #8E87F4;
        padding: 12px;
        border-radius: 8px;
        background-color: white;
        font-weight: bold;
        margin: 5px 0;
        border: 2px solid #8E87F4;
    }

    QPushButton:hover[for="save-plot-button"] {
        background-color: rgba(142, 135, 244, 0.1);
    }

    QPushButton:pressed[for="save-plot-button"] {
        background-color: rgba(142, 135, 244, 0.2);
    }
"""

center_panel_style = """
    QScrollArea {
        border: none;
        padding: 0px;
        background-color: white;
        border-radius: 12px;
        border: 1px solid #e9ecef;
    }
"""

right_panel_style = """
    QTextEdit {
        font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
        font-size: 14px;
        font-weight: medium;
        color: #495057;
        border-radius: 12px;
        padding: 15px;
        background-color: white;
        border: 1px solid #e9ecef;
        line-height: 1.5;
    }
"""

tab_style = """
    QTabWidget::pane {
        border: 1px solid #e9ecef;
        border-radius: 8px;
        background-color: white;
        top: -1px;
    }
    
    QTabBar::tab {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-bottom: none;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        padding: 8px 12px;
        margin-right: 2px;
        color: #495057;
    }
    
    QTabBar::tab:selected {
        background-color: white;
        border-bottom: 1px solid white;
        color: #8E87F4;
        font-weight: bold;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #e9ecef;
    }
"""

splashscreen_style = """
    QWidget {
        background-color: #f8f9fa;
    }
    
    QPushButton {
        font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
        font-size: 16px;
        padding: 12px 24px;
        border-radius: 25px;
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #8E87F4, stop: 1 #FD8FD4
        );
        color: white;
        font-weight: bold;
        border: none;
    }
    
    QPushButton:hover {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #7A74E0, stop: 1 #E97CC0
        );
    }
    
    QPushButton:pressed {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 0,
            stop: 0 #6A64D0, stop: 1 #D96CB0
        );
    }
"""