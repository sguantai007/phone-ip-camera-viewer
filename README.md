# Phone IP Camera Viewer

## Project Description

This project is a Python-based camera viewer that uses a phone as an IP camera. It connects to the phone camera over a Wi-Fi network and displays a live video stream on a computer.

The application uses OpenCV to process and display video frames, while Requests checks whether the camera is reachable before the video stream starts.

## Features

- Connects to a phone IP camera over Wi-Fi.
- Displays a live video stream.
- Resizes video frames while maintaining their aspect ratio.
- Displays the current timestamp, camera name, resolution, and estimated FPS.
- Captures screenshots of the live video.
- Records video and saves recordings.
- Detects connection problems and attempts to reconnect.
- Handles errors without displaying unnecessary Python tracebacks.
- Supports safe shutdown using Esc or Ctrl+C.
- Automatically releases the camera and closes OpenCV windows when the program exits.

## Technologies Used

- **Python** – Main programming language.
- **OpenCV** – Video capture, image processing and display.
- **Requests** – Checks camera connectivity.
- **NumPy** – Supports image and frame processing.

## Project Structure

```text
camera-viewer-project/
│
├── main.py
├── config.ini
├── requirements.txt
├── README.md
│
├── screenshots/
├── recordings/
├── evidence/
│
└── .gitignore
```

## Installation

1. Clone or download the project from GitHub.
2. Open the project folder in your terminal.
3. Create a virtual environment:

   `python -m venv .venv`

4. Activate the virtual environment in Windows PowerShell:

   `.venv\Scripts\Activate.ps1`

5. Install the required libraries:

   `pip install -r requirements.txt`

## Camera Configuration

The application uses a phone running IP Camera Lite as the camera source.

1. Connect the phone and computer to the same Wi-Fi network.
2. Open IP Camera Lite on the phone.
3. Start the camera stream.
4. Open `config.ini` in the project folder.
5. Enter the camera name and current MJPEG stream URL.

Example configuration:

```ini
[CAMERA]
name = Phone Camera
url = YOUR_CAMERA_STREAM_URL
```

Replace the example URL with the actual stream URL displayed by the phone application.

Keep `config.ini` private because it may contain connection details.

## Running the Application

After activating the virtual environment and configuring the camera, run:

`python main.py`

The application checks the camera connection before opening the live video stream.

## Keyboard Controls

| Key | Action |
|---|---|
| R | Start or stop video recording |
| S | Capture a screenshot |
| Esc | Exit the application |

Ctrl+C can also be used in the terminal to interrupt the program safely.

## Output Files

- **screenshots/** – Stores captured screenshots.
- **recordings/** – Stores recorded video files.
- **evidence/** – Stores screenshots used to document the test results.

## Testing

The application was tested using 10 test cases covering:

- Live stream startup.
- Invalid camera URLs.
- Unavailable cameras.
- Video overlays.
- Video resizing.
- Screenshot capture.
- Video recording.
- Connection loss and reconnection.
- Safe exit using Esc during recording.
- Safe exit using Ctrl+C during recording.


## Conclusion

This project demonstrates how Python and OpenCV can be used to create a live IP camera viewer with additional features such as video resizing, overlays, screenshot capture, video recording, connection monitoring and error handling.