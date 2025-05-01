
style = """
QWidget {
    font-family: 'Arial', sans-serif;
    
}

QLineEdit {
    font-size: 14px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-bottom: 15px;
}

QLineEdit:focus {
    border-color: #007ACC;
}

QPushButton {
    font-size: 14px;
    padding: 8px;
    border-radius: 4px;
    background-color: #007ACC;
    color: white;
    font-weight: bold;
    margin: 5px 0;
}

QPushButton:hover {
    background-color: #005f99;
}

/* Custom styling for the range layout and its elements */
QHBoxLayout {
    margin-top: 10px;
}

QLabel[for="range-label"] {
    font-size: 14px;
    font-weight: bold;
    margin-right: 10px;
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

/* Style for the result QTextEdit */
QTextEdit {
    font-size: 13px;
    background-color: #f4f4f4;
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 8px;
    color: #333;
}

/* Style for the graph area */
QScrollArea {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 8px;
    background-color: white;
}



"""

main_panel_style = """
    QWidget {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #62b84f, stop: 1 #ffffff);
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
        border-radius: 10px;
        padding: 8px;
        background-color: rgba(0, 0, 0, 0.05);
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
        background-color: #007ACC;
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
    QWidget {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 8px;
        background-color: white;
    }
"""

right_panel_style = """
    QWidget {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 8px;
        background-color: white;
    }
"""