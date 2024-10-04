# Dicoding Collection Dashboard

## Overview
This project focuses on exploring and analyzing the *Bike Sharing Dataset*. It utilizes various analytical techniques to uncover insights into bike rental behaviors influenced by environmental and seasonal factors. The goal is to comprehensively analyze the dataset, highlighting trends, patterns, and key metrics related to bike rentals. By examining the correlations between rental counts and factors such as weather conditions, time of year, and significant events, this project aims to enhance our understanding of urban mobility dynamics and the effectiveness of bike-sharing systems.


## Data Source
The data used in this project comes from the following source:

- [Bike Sharing Dataset](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)


## Requirements
To run this project, you need to install the following Python packages:

- Babel==2.11.0
- matplotlib==3.8.4
- numpy==1.26.4
- pandas==2.2.2
- seaborn==0.13.2
- streamlit==1.32.0


You can find the required packages listed in the requirements.txt file.

## Installation

### Clone the Repository
First, clone the repository:

git clone https://github.com/Igoo0/Proyek-Streamlit.git

cd Proyek-Streamlit

## Create a virtual environment
python -m venv venv

## Activate the virtual environment
### On Windows
venv\Scripts\activate

## Install Dependencies
### Install the required packages:

pip install -r requirements.txt

## Prepare Data
Ensure that you have the following CSV files in the ./Data/ directory:
hour.csv

Adjust the file paths in dashboard.py if necessary.

## Running the Dashboard
### Run the Streamlit application:

streamlit run Dashboard\dashboard.py 
