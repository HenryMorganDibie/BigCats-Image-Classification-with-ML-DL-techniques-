# -*- coding: utf-8 -*-
"""Copy of BigCats Image Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-KRyzeJJqR3_uczM5BtPVvOyNvcSf0P1

Loading Dataset and Description
"""

!unzip 'drive/MyDrive/Big Cats Image Classification/archive (18).zip' -d 'drive/MyDrive/Big Cats Image Classification/'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

Wildcats = pd.read_csv('drive/MyDrive/Big Cats Image Classification/WILDCATS.CSV')
Wildcats

"""Explanatory Data Analysis Of Big Cats Image Classification"""

import pandas as pd
import matplotlib.pyplot as plt


# Print the shape of the DataFrame
print(Wildcats.shape)

# Check for missing values
print(Wildcats.isnull().sum())

# Get unique values of the 'scientific name' column
print(Wildcats['scientific name'].unique())

# Plot a bar chart of the frequency of each 'scientific name' value
Wildcats['scientific name'].value_counts().plot(kind='bar')
plt.title('Frequency of scientific name values')
plt.xlabel('Scientific name')
plt.ylabel('Frequency')
plt.show()

# Plot a pie chart of the distribution of 'data set' values
Wildcats['data set'].value_counts().plot(kind='pie')
plt.title('Distribution of data set values')
plt.show()

Wildcats['labels'].value_counts().median()

train = 'drive/MyDrive/Big Cats Image Classification/train'
train

test = 'drive/MyDrive/Big Cats Image Classification/test'

validation = 'drive/MyDrive/Big Cats Image Classification/valid'

"""Training Model using convolutional neural network and later got a better performance using MobileNetV2 """

import tensorflow as tf
from tensorflow.keras import layers, models

# Load and preprocess the dataset
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(
    train,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

validation_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
validation_generator = validation_datagen.flow_from_directory(
    validation,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(
    test,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

# Define the neural network architecture
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train the neural network
history = model.fit_generator(
    train_generator,
    steps_per_epoch=train_generator.n // train_generator.batch_size,
    epochs=10,
    validation_data=validation_generator,
    validation_steps=validation_generator.n // validation_generator.batch_size)

# Evaluate the neural network
test_loss, test_acc = model.evaluate_generator(test_generator, steps=test_generator.n // test_generator.batch_size)
print('Test accuracy:', test_acc)

print("Test accuracy: {:.2%}".format(test_acc))

"""Using Transfer learning to improve the accuracy of my image classification model"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# set up the data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

# load the pre-trained MobileNetV2 model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# add a new top layer for our own classification task
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)
predictions = Dense(10, activation='softmax')(x)

# create a new model for our own classification task
model = Model(inputs=base_model.input, outputs=predictions)

# freeze the pre-trained layers
for layer in base_model.layers:
    layer.trainable = False

# compile the model
model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# train the model
history = model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator)

# evaluate the model on the test data
test_generator = test_datagen.flow_from_directory(
    test,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical')

test_loss, test_acc = model.evaluate(test_generator)
print('Test accuracy:', test_acc)

print("Test accuracy: {:.2%}".format(test_acc))

