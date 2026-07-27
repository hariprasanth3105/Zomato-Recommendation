# Bengaluru Restaurant Recommendation System

A content-based restaurant recommendation engine built using the Zomato Bengaluru dataset. The system ranks restaurants based on user preferences such as location, cuisine, budget, and rating.

> **Click this link to try the Streamlit app: https://zomato-recommendation-fdnseidwjd4uuawsfysvke.streamlit.app**

## Project Overview

This project helps users discover the most suitable restaurants in Bengaluru through a transparent and explainable scoring system. It combines data cleaning, exploratory analysis, market opportunity insights, and a recommendation engine deployed as a Streamlit web application.

### Key Features

- Content-based recommendation engine
- Supports multiple location and cuisine preferences
- Budget and minimum rating filters
- Transparent scoring logic (Rating + Popularity + Budget Fit + Preference Match)
- Bonus for restaurants offering table booking
- Interactive Streamlit web app

## Business Context

The Bengaluru restaurant market is highly competitive. This project aims to:

1. Help users find restaurants that best match their preferences
2. Provide market insights for aspiring restaurant owners
3. Identify underserved cuisine-location opportunities

## Recommendation Logic

The system uses a two-layer approach:

### 1. Hard Filters
- Preferred Location(s)
- Preferred Cuisine(s)
- Maximum Budget
- Minimum Rating

### 2. Soft Scoring (Final Score out of 100)

| Component            | Weight | Description                              |
|----------------------|--------|------------------------------------------|
| Rating Score         | 35%    | Higher rated restaurants score better    |
| Popularity Score     | 25%    | Based on number of votes (log scaled)    |
| Budget Fit Score     | 20%    | How well the cost matches the user budget|
| Cuisine Match        | 10%    | Partial match using full cuisine list    |
| Location Match       | 10%    | Match with selected locations            |
| Book Table Bonus     | +5     | Bonus if table booking is available      |

## Dataset

- **Source**: Zomato Bengaluru Restaurants Dataset
- **Original Size**: ~51,700 rows
- **After Cleaning**: 12,530 unique restaurants
- **Key Cleaning Steps**:
  - Removed duplicate listings of the same restaurant
  - Standardized Rating and Cost columns
  - Created `PRIMARY_REST_TYPE` and `PRIMARY_CUISINE`
  - Created cleaned location groups

## Project Structure

bengaluru-restaurant-recommender/

│

├── recommendation.py                     # Streamlit application

├── zomato_recommender.csv 

├── requirements.txt

└── README.md





