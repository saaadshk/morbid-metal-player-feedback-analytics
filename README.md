# Morbid Metal Player Feedback Analytics Dashboard

A web-based analytics platform that collects, processes, and visualizes Steam player feedback for Morbid Metal using Python, text analytics, and interactive dashboards.

## Overview

This project analyzes player reviews published after the Early Access release of Morbid Metal to uncover player sentiment, feedback trends, and gameplay-related discussion topics.

The project follows a complete analytics workflow:

- Data Collection
- Data Cleaning
- Language Filtering
- Topic Classification
- Sentiment Analysis
- Exploratory Data Analysis
- Interactive Dashboard Development

## Features

### Data Collection
- Steam review extraction using Steam Web API
- Automated review collection pipeline
- Early Access review analysis

### Text Analytics
- Review preprocessing and cleaning
- Topic tagging and categorization
- Sentiment classification
- Review language analysis

### Topics Analyzed
- Combat
- Character Switching
- Visuals
- Bosses
- Performance
- Content Quantity
- Build Variety
- Enemy Variety
- Replayability
- Level Design
- Bugs
- Difficulty

### Dashboard Features
- Recommendation Rate KPI
- Review Volume Tracking
- Topic Mention Analysis
- Positive vs Negative Topic Comparison
- Player Feedback Insights
- Interactive Visualizations

## Project Structure

```text
Morbid Metal/
│
├── data/
│   ├── morbid_metal_reviews.csv
│   ├── morbid_metal_tagged_reviews.csv
│   └── topic_summary.csv
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   └── analytics.ipynb
│
├── requirements.txt
│
└── README.md
```

## Technologies Used

- Python
- Pandas
- Plotly
- Dash
- NumPy
- Steam Web API
- Jupyter Notebook

## Dashboard Preview

The dashboard provides:

- Player feedback KPIs
- Topic-level sentiment analysis
- Interactive visualizations
- Stakeholder-focused insights
- Data-driven reporting

## How to Run

### 1. Clone Repository

```bash
git clone <repository-url>
cd morbid-metal-analytics
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate Environment

Mac/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Dashboard

```bash
python dashboard/app.py
```

Open:

```text
http://127.0.0.1:8050
```

## Key Skills Demonstrated

- Data Collection
- Data Cleaning
- Exploratory Data Analysis
- Text Analytics
- Sentiment Analysis
- Feature Engineering
- Data Visualization
- Dashboard Development
- Product Analytics
- Player Feedback Analysis
- Stakeholder Reporting

## Future Enhancements

- NLP-based topic modeling
- Word cloud analysis
- Review trend analysis
- Temporal sentiment tracking
- Automated dashboard deployment
- Advanced player segmentation

## Author

Saad Shaikh