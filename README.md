# Drowsiness Detection System

## Overview

The Drowsiness Detection System is a Python-based project that aims to address some common challenges in drowsiness detection systems. It focuses on improving the accuracy of drowsiness detection, alerting the driver at an early stage, and notifying a third party or emergency contact about the situation. This project utilizes facial analysis techniques to monitor a driver's face for early signs of drowsiness.

### Challenges in Drowsiness Detection

1. **False Alarms:** One challenge in drowsiness detection systems is the occurrence of false alarms, where the system issues a warning even when the driver is not drowsy.

2. **Late Warnings:** Many systems only alert the driver when they are already in a deeply drowsy state, missing early warning signs.

3. **Third-Party Notification:** Most drowsiness detection systems do not notify a third party or emergency contact about the situation, potentially risking safety.

### Objectives

This project has three primary objectives:

1. **Drowsiness Detection and Classification:** Develop a system that accurately detects and classifies the driver's drowsiness state.

2. **Early Symptom Detection:** Analyze a drowsy driver's facial cues to detect early symptoms and provide immediate alerts.

3. **Third-Party Notification:** Create a drowsiness detection system that can alert the drowsy driver and notify a third party via text message and email.

### System Architecture

The diagram below illustrates the overall architecture of the system:
Here's a breakdown of the process:

- Input video footage is provided to the system.
- A face detector locates the driver's face in the image.
- Features of the face, including the eyes and mouth, are extracted.
- The extracted features are fed into trained Convolutional Neural Network (CNN) models for classification.
- The system determines if the driver is yawning or if their eyes are open or closed.
- If the driver is predicted to be drowsy, an alert is triggered to regain their concentration.

### Facial Analysis

For face detection, the system employs Dlib, which uses Histogram of Oriented Gradients (HOG) and Support Vector Machines (SVM) to identify and construct 68 landmarks on the face. These landmarks include the eyes, nose, mouth, and jawline.

- The points from 49 to 68 are used to locate the mouth in the face.
- Dlib's 68 landmark model is utilized to crop the eyes and mouth images for analysis.

#### Eye Classification Model

The eye classification model is trained using the MRL eye dataset, which undergoes data preprocessing, including grayscale conversion and resizing. Three individual CNN models and an ensemble CNN model are built for training, and evaluation metrics are used to measure the classification performance.

#### Mouth Yawn Classification Model

For the mouth yawn classification model, the Yawn dataset is used. Data augmentation is applied to prepare the dataset for training. Similar to the eye model, three individual CNN models and an ensemble CNN model are constructed, and evaluation metrics are employed to assess classification performance.

### Ensemble Learning

In this project, ensemble learning is utilized as the final classification method for both the eyes and mouth yawn classification. The ensemble model averages the output from the individual classification models, using the average of predictions as the final prediction.

### Results

Both the classification of eyes and mouth yawn have achieved promising performance. The ensemble models have significantly increased accuracy, with eye classification reaching 97.4% accuracy and mouth yawn classification achieving 96.5%.

## Installation

### Prerequisites

Before running the Drowsiness Detection System, you need to ensure you have the following software and libraries installed:

- Python 3.x: You can download Python from the official [Python website](https://www.python.org/downloads/).

### Instructions

1. Clone the GitHub repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/drowsiness-detection.git
   cd drowsiness-detection

   pip install numpy argparse dlib opencv-python matplotlib tensorflow pillow pyttsx3 \
   pythonnet twilio imutils geocoder pygame

2. Download the pre-trained shape predictor model for face detection:
   You can download the model from the Dlib official website.
   Once downloaded, unzip the file and place it in the project directory.

3. Download the pre-trained eye and mouth yawn models:

   These models can be obtained from your training process or another source, and they       should be placed in the project directory under the specified paths in your code          (e.g., Version2-Eye Model and Version2-Mouth Model).

4. Prepare the sound files:

   Place an audio file named alarm.mp3 in the project directory for the alarm sound.
   Configure your email and Twilio credentials:

5. Configure your email and Twilio credentials:
   Update the following variables in your code with your own email and Twilio account        information:

   ```bash
   SENDER_EMAIL and SENDER_PASSWORD for email alert.
   account_sid and auth_token for Twilio SMS alert.

6. Launch the application:

   Run the application using the provided Python script:
   ```bash
   python DrowsinessDetectionSystem.py

7. Use the system:

   The application will start capturing video from your webcam and monitoring for            drowsiness. You can interact with the system through the graphical user interface         (GUI) provided.

Note: Ensure that you have a working webcam or camera connected to your machine to use this system.

Feel free to customize the installation instructions further if there are any additional details or specific requirements for your project.


To use the Drowsiness Detection System, follow these instructions:

1. Launch the application by running the provided Python script.

2. The system will start capturing video from your webcam, analyzing your facial features, and monitoring for signs of drowsiness.

3. The graphical user interface (GUI) provides the following functionality:
   - **Volume Control:** Click the volume button to mute/unmute the alarm sound.
   - **Settings:** Click the settings button to customize the email address for receiving alerts. By default, it's set to 'bellelim0621@gmail.com'.
   - **Alerts:** The system will trigger both warnings and alarms when drowsiness is detected.
   - **Multiple Instances of Drowsiness:** If the system detects multiple instances of drowsiness, it will send an email and SMS to your emergency contact.

4. Ensure you have a functional webcam or camera connected to your machine to use this system effectively.


## Contributing

If you would like to contribute to this project, you are welcome to do so. Here are some ways you can get involved:

- Fork the repository on GitHub.
- Make your desired changes or enhancements to the project.
- Create a pull request with a clear description of the changes you've made.

## Acknowledgments

We would like to give credit to the following libraries, tools, and individuals for their contributions to this project:

- [Dlib](http://dlib.net/): Used for face detection and shape prediction.
- [OpenCV](https://opencv.org/): Used for image processing and video capture.
- [TensorFlow](https://www.tensorflow.org/): Used for training and deploying the eye and mouth yawn models.
- [Pillow](https://pillow.readthedocs.io/en/stable/): Used for image manipulation.
- [Pyttsx3](https://github.com/nateshmbhat/pyttsx3): Used for text-to-speech functionality.
- [Twilio](https://www.twilio.com/): Used for SMS alerting.
- [Geocoder](https://geocoder.readthedocs.io/): Used for retrieving the current location.
- [pygame](https://www.pygame.org/): Used for playing alarm sounds.

Special thanks to all the contributors and developers of these tools and libraries.

## Contact

For any questions or feedback regarding this project, please feel free to reach out to:

- Your Name: Belle Lim
- Email: bellelim0621@gmail.com
