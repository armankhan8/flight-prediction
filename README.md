# Flight Price Prediction Web Application

This is a web application that predicts flight prices based on various parameters using machine learning. The application is built using Flask and includes a trained model for price prediction.

## Prerequisites

Before running this project, make sure you have the following installed:
- Python 3.8 or higher
- Conda (for virtual environment management)
- Git (optional, for cloning the repository)

## Project Structure

```
├── app.py              # Main Flask application
├── model.py           # Model training and prediction logic
├── model.pkl          # Trained model file
├── pre.py            # Data preprocessing script
├── requirements.txt   # Project dependencies
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates
└── dataset/          # Dataset directory
```

## Installation Steps

1. **Clone the Repository** (if using Git)
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # Create virtual environment
   conda create -n flight_env python=3.8
   
   # Activate virtual environment
   conda activate flight_env
   ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask Server**
   ```bash
   python app.py
   ```

2. **Access the Web Application**
   - Open your web browser
   - Go to: http://127.0.0.1:5000/

## Features

- Flight price prediction based on various parameters
- User-friendly web interface
- Real-time predictions
- Input validation and error handling

## Technical Details

The application uses:
- Flask 2.0.2 for the web framework
- scikit-learn for machine learning
- pandas and numpy for data manipulation
- HTML/CSS for frontend

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly
2. Check if the virtual environment is activated
3. Verify that Python 3.8 or higher is being used
4. Ensure all required files are present in the project directory

## Support

For any questions or issues, please contact:
[Your Contact Information]

## License

[Your License Information]