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


## Usage

[Provide usage instructions as previously mentioned]

## Contributing

[Explain how others can contribute to your project if desired]

## License

[Specify the project's license, e.g., MIT License]

## Acknowledgments

[Give credit to any libraries, tools, or individuals who contributed to the project]

## Contact

[Provide contact information for questions or feedback]
