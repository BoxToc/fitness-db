Fitness DB 

A personal workout tracker that lets you store, organize, and view your favorite YouTube workouts using HarperDB and Streamlit. Tired of messy playlists and repetitive workouts? Build your own fitness dashboard. 

Demo
  - https://vimeo.com/1094425257/409a76bbc7?share=copy

Features 
  - Add YouTube workouts by pasting a link 
  - View all workouts with title, channel, and duration 
  - Today’s workout randomly picks one from your saved list 
  - Delete any workout anytime 
  - Uses HarperDB as the backend database 
  - Data is pulled with yt_dlp and displayed in a clean Streamlit UI 

Tech Stack 
  - Python 
  - Streamlit 
  - HarperDB 
  - yt_dlp 
  - Hosted locally (can also use HarperDB Cloud)

Folder Structure 
  - workoutapp/ <-- app.py <-- Streamlit UI <-- yt_extractor.py <-- YouTube metadata fetcher <-- database_service.py <-- Database functions (insert, fetch, delete) <-- send_workout.js ← (optional) script to test POSTing to API 
    yaml Copy Edit 

Setup 
  - Clone the repo ```bash git clone https://github.com/BoxToc/fitness-db.git cd fitness-db Install dependencies 
  - bash Copy Edit pip install -r requirements.txt Set up HarperDB 
  - Make sure HarperDB is running locally or via HarperDB Cloud 
  - Configure your url, username, and password inside database_service.py 
  - Run the app 
  - bash Copy Edit streamlit run app.py *This project is designed for local use or small personal deployments* 
