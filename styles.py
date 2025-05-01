
style = """
QWidget {
    font-family: 'Arial', sans-serif;
    
}

/* Style for the horizontal spacing for components */
QSpacerItem {
    height: 10px;
}

/* Style for error messages */
QMessageBox {
    font-size: 14px;
    background-color: #f8d7da;
    color: #721c24;
    border-radius: 5px;
    padding: 15px;
}

"""

main_panel_style = """
    QWidget {
        margin: 0;
        padding: 15px; 
    }
"""

header_panel_style = """
    QWidget {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 8px;
        background-color: white;
    }

    QLabel {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin: 10px 0;
        text-align: center;
    }
"""

left_panel_style = """
    QVBoxLayout {
        margin: 0;
        padding: 15px; 
    }

    QWidget[for="left-widget"] {
        border-radius: 20px;
        padding: 8px;
        background-color: rgba(0, 0, 0, 0.10);
    }

    QLabel[for="function-label"], QLabel[for="derivative-order-label"], QLabel[for="x-range-label"] {
        font-family: "Roboto", "Arial", sans-serif;
        font-size: 18px;
        font-weight: bold;
        padding: 0px 5px;
    }   

    QLabel[for="func-help-icon"], QLabel[for="deriv-help-icon"] {
        color: rgba(0, 0, 0, 0.5); /* rgba(red, green, blue, alpha) */
        border-radius: 16px;
        font-size: 14px;
        font-weight: bold;
        padding: 7.5px;
    }

    QLineEdit {
        font-family: "Roboto", "Arial", sans-serif;
        font-size: 14px;
        padding: 7.5px;
        border: 1.5px solid white;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    QLineEdit:focus {
        border-color: #007ACC;
    }
    
    QLineEdit::placeholder {
        font-size: 12px;
        color: rgba(230, 230, 230, 0.1);
    }

    QPushButton[for="plot-button"] {
        font-family: "Roboto", "Arial", sans-serif;
        font-size: 20px;
        padding: 15px;
        border-radius: 25px;
        background: qlineargradient(
            x1: 0, y1: 0, x2: 1, y2: 1,
            stop: 0 #007ACC, stop: 1 #00AFFF
        );  /* Gradient from #007ACC (blue) to #00AFFF (light blue) */
        color: white;
        font-weight: bold;
        margin: 2.5px 0;
    }

    QPushButton:hover[for="plot-button"] {
        background-color: #005f99;
    }

    QPushButton[for="save-plot-button"] {
        font-family: "Roboto", "Arial", sans-serif;
        font-size: 14px;
        color: rgba(15, 15, 15, 0.5);
        padding: 15px;
        border-radius: 20px;
        background-color: #d6d6d6;
        font-weight: bold;
        margin: 5px 0;
    }

    QPushButton:hover[for="save-plot-button"] {
        background-color: #adadad;
    }
"""

center_panel_style = """
    QScrollArea {
        border: 10px solid rgba(0, 0, 0, 0.05);  /* Transparent border */
        padding: 0px;
        background-color: rgba(0, 0, 0, 0.05);  /* Transparent background */
    }
"""

right_panel_style = """
    QTextEdit {
        font-family: "Roboto", "Arial", sans-serif;
        font-size: 14px;
        font-weight: medium;
        color: rgba(0, 0, 0, 0.75);
        border-radius: 20px;
        padding: 12px;
        background-color: rgba(0, 0, 0, 0.10);
    }
"""