# Predicting real yield from a photovoltaic system

## Overview
The goal of this project is to predict the actual yield of small photovoltaic systems built on building roofs and courtyards, depending on weather conditions, using deep learning. A solar panel is a renewable energy source that converts sunlight into electricity. The output of the solar panel depends on many factors, such as solar radiation, temperature, geographical location, humidity, atmospheric pressure, air quality (dustiness), etc. In order to improve the efficiency and reliability of the solar panel, it is necessary to predict these factors and their influence on the output. I find its application in the possibility of more accurate and reliable calculations in energy efficiency projects.

## Idea
My idea is that every user can enter the maximum power of their photovoltaic system, the geographical location and the meteorological conditions to predict the actual production power.

## Results
My model is able to predict the actual yield of a photovoltaic system with avg 14 persent diffrens for 1000 hours or 41 days. The model is trained on a dataset of 40 000 samples plus 20 000 generated samples. 

## Experiments
The experiments are contained in the [link](https://drive.google.com/drive/folders/19UkABNrchZw8OIpmZLVCNRwQ7EqImuUb?usp=sharing)

## Import
You can import my model `the_best.h5` with the comand:
```model = tf.keras.models.load_model('the_best.h5')```