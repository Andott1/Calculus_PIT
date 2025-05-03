# 📈 Function Visualizer (Graphique)

**Graphique** is a PyQt5-powered graphical application that allows users to input and visualize mathematical functions, their derivatives (up to any order), and their integrals over a specified domain. It is useful for students, educators, and professionals who want to better understand calculus concepts through visual representation.

![Function Visualizer (Graphique)](Assets/splash_screen.png)

---

## ✨ Features

- 🧮 Input and visualize mathematical functions of `x`
- 🔁 Compute and plot higher-order derivatives
- ∫ Compute and show symbolic integral
- 📊 Graph original function, derivatives, and area under the curve
- 💾 Save graph output as PNG/JPG
- 🖼️ Smooth and responsive UI with a welcome splash screen
- 🔍 Scrollable graph area for large visualizations
- ❓ Help tooltips and warnings for invalid input

---

## 🖼️ Screenshots

| Splash Screen                              | Main Window                                |
|-------------------------------------------|--------------------------------------------|
| ![Splash Screen](Assets/App%20Screenshots/Splash%20Screen.png) | ![Main Window](Assets/App%20Screenshots/Main%20Screen.png) |

---

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Dependencies

The application requires the following Python packages:

- Python 3.6+
- PyQt5
- NumPy
- SymPy
- SciPy
- Matplotlib

### Installation Steps

1. Clone or download this repository:

```bash
git clone https://github.com/Andott1/Discrete_PIT.git
cd Discrete_PIT
```

1. Install the required dependencies:

```bash
pip install pyqt5 numpy sympy scipy matplotlib
```

or

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, simply execute the main.py file:

```bash
python main.py
```

The application will start with a splash screen, followed by the main application window.

## Project Structure

```bash
FunctionVisualizer/
├── Assets/
│   └── App Screenshots/
│   │   ├── Splash Screen.png     # Splash screen screenshot
│   │   └── Main Screen.png       # Main screen screenshot
│   ├── Resources/
│   ├── splash_screen.png     # Splash screen image
│   └── main_screen.png       # Main screen image
├── styles.py                     # Centralized Qt style definitions
├── graph.py                      # Plotting widget using Matplotlib
├── main.py                       # Main application logic and UI
├── requirements.txt              # (Optional) List of required packages
└── README.md                     # This file
```

## Usage

1. **Enter a Function**: Input a valid expression like 3*x**2 + 2*x - 4
2. **Set X Range**: Specify minimum and maximum values (e.g., -10 to 10)
3. **Choose Derivative Order**: Optional, set to 1 for first derivative, 2 for second, etc.
4. **Click Plot**: Visualize the function, its derivatives, and integral
5. **Save Graph**: Export the plotted graph to an image file
6. **View Results**: Symbolic derivative and integral will be shown on the side panel

## Troubleshooting

### Common Issues

1. **Graph not appearing**:

- Ensure your input expression is valid Python math syntax (e.g., use x**2 not x^2)
- Check console for errors
- Try using a simpler function

1. **Missing images**:

- Make sure the Assets/App Screenshots/ folder contains the correct images
- Supported formats: PNG, JPG

1. **Invalid Function Input**:

- Only use valid variable x
- Constants like pi and e are supported via sympy

## Development

### To modify the UI or logic

1. Edit main.py for main functionality and UI logic
2. Modify graph.py to customize how plots appear
3. Tweak styles.py to change application styling

## License

This project is provided for educational and non-commercial use only.
All rights reserved by the original developer.
