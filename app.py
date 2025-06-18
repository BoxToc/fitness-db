import random
import streamlit as st
from yt_extractor import get_info           # Module to extract YouTube metadata
import database_service as dbs              # Custom module to interact with HarperDB


# Cache the workout list to avoid repeated DB calls
@st.cache_data
def get_workouts():
    return dbs.get_all_workouts()

# Convert duration in seconds to a MM:SS or HH:MM:SS string
def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60*60)) % 24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text

# App title
st.title("Workout APP")

# Sidebar menu
menu_options = ("Today's workout", "All workouts", "Add workout")
selection = st.sidebar.selectbox("Menu", menu_options)

# View All Workouts
if selection == "All workouts":
    st.markdown("## All workouts")
    
    workouts = get_workouts()
    if workouts:
        for wo in workouts:
            url = "https://youtu.be/" + wo["video_id"]
            st.text(wo['title'])
            st.text(f"{wo['channel']} - {get_duration_text(wo['duration'])}")
            
            # Delete workout button
            ok = st.button('Delete workout', key=wo["video_id"])
            if ok:
                dbs.delete_workout(wo["video_id"])
                st.cache_data.clear()  # Clear cache to reflect deletion
                st.rerun()             # Rerun app to update UI

            st.video(url)
    else:
        st.text("No workouts in Database!")

# Add New Workout
elif selection == "Add workout":
    st.markdown("## Add workout")
    
    url = st.text_input('Please enter the video URL')
    if url:
        workout_data = get_info(url)  # Get video metadata
        if workout_data is None:
            st.text("Could not find video")
        else:
            st.text(workout_data['title'])
            st.text(workout_data['channel'])
            st.video(url)

            # Add workout to database
            if st.button("Add workout"):
                dbs.insert_workout(workout_data)
                st.text("Added workout!")
                st.cache_data.clear()  # Refresh the workout list

# Today's Workout
else:
    st.markdown("## Today's workout")
    
    workouts = get_workouts()
    if not workouts:
        st.text("No workouts in Database!")
    else:
        # Try fetching today’s workout
        wo = dbs.get_workout_today()
        
        if not wo:
            # If not defined, randomly select one
            n = len(workouts)
            idx = random.randint(0, n - 1)
            wo = workouts[idx]
            dbs.update_workout_today(wo, insert=True)
        else:
            wo = wo[0]  # Use existing one

        # Button to shuffle and get a different workout
        if st.button("Choose another workout"):
            n = len(workouts)
            if n > 1:
                idx = random.randint(0, n - 1)
                wo_new = workouts[idx]
                while wo_new['video_id'] == wo['video_id']:  # Avoid same video
                    idx = random.randint(0, n - 1)
                    wo_new = workouts[idx]
                wo = wo_new
                dbs.update_workout_today(wo)

        # Display selected workout
        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo['title'])
        st.text(f"{wo['channel']} - {get_duration_text(wo['duration'])}")
        st.video(url)
