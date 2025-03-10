# Predicting real yield from a photovoltaic system

## Overview
The goal of this project is to predict the actual yield of small photovoltaic systems built on building roofs and courtyards, depending on weather conditions, using deep learning. A solar panel is a renewable energy source that converts sunlight into electricity. The output of the solar panel depends on many factors, such as solar radiation, temperature, geographical location, humidity, atmospheric pressure, air quality (dustiness), etc. In order to improve the efficiency and reliability of the solar panel, it is necessary to predict these factors and their influence on the output. I find its application in the possibility of more accurate and reliable calculations in energy efficiency projects.

## Idea
My idea is that every user can enter the maximum power of their photovoltaic system, the geographical location and the meteorological conditions to predict the actual production power.

## Results
My model is able to predict the actual yield of a photovoltaic system with an average 14 percent difference for 41 days. The model is trained on a dataset of 50000 examples. Additionally, new synthetic data has been created using Series GAN.

A ipynb and a new program have been created. An exe file for users to download will be added soon. A comparison with the PHOTOVOLTAIC GEOGRAPHICAL INFORMATION SYSTEM shows that the new model is more accurate.

### Comparison Table

The data is calculated using ratio of predicted to actual values.

| Station | Power (kWh) | New model | PHOTOVOLTAIC GEOGRAPHICAL INFORMATION SYSTEM |
|---------|--------------|----------------------|----------------------------------------------|
| **Alverston Close** | 3.29 | 112.1946 | 160.5176 |
| **Bancroft Close** | 1.89 | 91.58 | 89.32 |
| **Forest Road** | 3.29 | 100.25 | 98.54 |
| **Maple Drive East** | 3.83 | 90.50 | 122.64 |
| **Suffolk Road** | 1.52 | 85.12 | 123.11 |
| **YMCA** | 0.60 | 113.63 | 103.46 |

The data represents the mae for each model's prediction.

| Station               | Power (kWh)  | New model                 | PHOTOVOLTAIC GEOGRAPHICAL INFORMATION SYSTEM|
|-----------------------|------------- |---------------------------|---------------------------------------------|
| **Alverston Close**   | 3.29         | 0.8682                   | 3.1245                                       |
| **Bancroft Close**    | 1.89         | 0.9621                   | 2.4334                                       |
| **Forest Road**       | 3.29         | 2.3178                   | 3.4004                                       |
| **Maple Drive East**  | 3.83         | 1.0108                   | 4.1890                                       |
| **Suffolk Road**      | 1.52         | 0.2605                   | 1.7255                                       |
| **YMCA**              | 0.60         | 0.1325                   | 0.3509                                       |

## Experiments
The experiments are contained in the [link](https://drive.google.com/drive/folders/19UkABNrchZw8OIpmZLVCNRwQ7EqImuUb?usp=sharing)

## Import
You can import my model `the_best.h5` with the comand:
```model = tf.keras.models.load_model('the_best.h5')```

Shield: [![CC BY-NC-ND 4.0][cc-by-nc-nd-shield]][cc-by-nc-nd]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-NoDerivs 4.0 International License][cc-by-nc-nd].

[![CC BY-NC-ND 3.0]]
[cc-by-nc-nd]: http://creativecommons.org/licenses/by-nc-nd/4.0/
[cc-by-nc-nd-image]: https://licensebuttons.net/l/by-nc-nd/4.0/88x31.png
[cc-by-nc-nd-shield]: https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg
