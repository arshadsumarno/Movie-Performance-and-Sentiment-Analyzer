# Movie Performance and Sentiment Analyzer

https://github.com/user-attachments/assets/431e89bd-a400-426a-a194-7c40f1b76fd8


## About the Project

This project analyzes movie franchise sentiment from fans and compares it to financial performance over time. The sentiment score is calculated using AI (VADER) and the YouTube comment section of each trailer, while the performance coefficient is derived from box office returns and production budgets.

The goal is to explore how fan reactions correlate with financial success and answer questions like:
- How reactionary do fans become on social media during periods of under or overperformance?
- Are fan sentiments aligned with actual success?


## Key Features

1. **Sentiment Analysis**
   - Extracts the top 100 comments from each trailer's YouTube page using the YouTube API.
   - Sentiment scores are calculated on a 0.00-1.00 scale using VADER, an AI tool specifically attuned to social media sentiments.

2. **Performance Coefficient**
   - Derived from production budget, box office returns, and calculated metrics like profit and ROI percentage.
   - Scaled using z-scores and a sigmoid function to provide relative comparisons across a franchise.

3. **Interactive Dashboard**
   - A web application built with Plotly Dash allows users to explore data for different movie franchises.
   - Graphs show sentiment and performance metrics over time, providing insights into trends.


## How It Works

### Sentiment Analysis Process
1. **Data Gathering**
   - Trailers for each movie are identified using The Movie DB API.
   - The Google Cloud YouTube API is used to fetch the top 100 comments for each trailer.
2. **Sentiment Calculation**
   - Sentiment is analyzed using VADER, producing a sentiment score between 0.00 and 1.00.
   - Data is stored in a structured table representing each movie’s sentiment.

### Performance Coefficient Process
1. **Data Gathering**
   - Movie statistics (e.g., production budget, box office) are collected via The Movie DB API.
2. **Scaling**
   - Financial metrics are normalized using z-scores relative to the franchise's overall performance.
   - A sigmoid function compresses these values into a 0.00-1.00 scale, ensuring balance and smooth scaling.


## Technologies Used

- **Python**: Data processing and analysis.
- **Dash & Plotly**: Interactive web application and visualizations.
- **APIs**:
  - [The Movie DB API](https://developers.themoviedb.org/3/getting-started) for movie data.
  - [YouTube Data API](https://developers.google.com/youtube/registering_an_application) for comments extraction.
- **VADER**: Sentiment analysis tailored for social media data.


## How to Run the Project

1. Clone this repository:
   ```bash
   git clone https://github.com/arshadsumarno/Movie-Performance-and-Sentiment-Analyzer.git
   python .\app\app_dash.py
