Project Name: Airline Live Tracking and Analysis

😊 Project Overview:

The application pulls live aircraft position data from the OpenSky Network's public aviation API and renders it on an interactive map, refreshing automatically every 45 seconds. Beyond live tracking, it includes a flight-analysis module that reconstructs an individual aircraft's trajectory from raw position data to calculate distance flown, average speed, and maximum altitude. A separate historical analytics module processes large-scale flight datasets (17,000+ records spanning 3 years) to surface traffic trends, identify the busiest routes, and rank airports by volume.

⭐Key Features:

Live tracking: Real-time global aircraft positions with altitude, speed, and heading, searchable by flight callsign Flight analysis: Reconstructs recent flight path from raw ADS-B waypoints; computes distance and speed Historical analytics: Processes multi-year flight records to report monthly trends, busiest routes, and top airports Resilient data handling: Gracefully handles missing fields, multiple timestamp formats, and inconsistent real-world API responses

🤷‍♂️ Technologies Used:

--> Python

--> Pandas

--> Matplotlib

--> Stramlit

--> plotpy

📂 Dataset

--> Airline Dataset for Analysis | kaggle

✈️ Live Tracking

--> Used OpenSky API Key

----> The Python program converts the JSON response into a structured format such as a Pandas DataFrame, where each row represents an aircraft and the columns contain its details.
