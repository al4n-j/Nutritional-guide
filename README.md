# Nutritional Guide

The **Nutritional Guide** is a tool designed to help individuals with food allergies by identifying fruits and vegetables in images and providing recommendations based on their specific allergies. The application uses Convolutional Neural Networks (CNN) to identify the items and cross-references the user's allergy information to determine if the identified items are safe for consumption.

## Food Dataset :
## Dataset
[Fruit and Vegetable Image Recognition Dataset](https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition)

## Features

- **Allergy Information Storage**: Users can input their allergy details, which are securely stored for future use.
- **Image Recognition**: Users can upload a photo of fruits or vegetables, and the app will identify the items using a CNN model.
- **Safety Check**: Once the fruits or vegetables are identified, the app checks the stored allergy information to determine whether the item is safe for the user.
- **Recommendations**: Based on the safety check, the app provides a recommendation on whether the food is safe to consume.

## Technologies Used

- **Python**: Backend development
- **TensorFlow / Keras**: For building and training the CNN model
- **Flask/Django**: Web framework for building the API and user interface
- **SQLite/MySQL**: For storing user allergy data
- **OpenCV / PIL**: For image preprocessing
- **GitHub Actions**: For Continuous Integration/Deployment (CI/CD)

**Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/nutritional-guide.git
    cd nutritional-guide
    ```


**Upload an image**:
    Once the server is running, navigate to the upload section, and upload an image of fruits or vegetables to check if it's safe based on the user's allergies.

## Usage

1. Create a user profile with allergy details.
2. Upload an image of fruits or vegetables.
3. Get a safety recommendation based on your allergies.

