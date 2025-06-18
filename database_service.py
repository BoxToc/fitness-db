import harperdb

# HarperDB cloud instance credentials

# For local testing
# url = "http://localhost:9925"
# username = "HDB_ADMIN"
# password = "YOUR_PW"

# Initialize HarperDB client
db = harperdb.HarperDB(
    url=url,
    username=username,
    password=password
)

# Constants for schema and table names
SCHEMA = "workout_repo"
TABLE = "workouts"
TABLE_TODAY = "workout_today"

# Insert a new workout into the main workouts table
def insert_workout(workout_data):
    return db.insert(SCHEMA, TABLE, [workout_data])

# Delete a workout from the main table by video ID
def delete_workout(workout_id):
    return db.delete(SCHEMA, TABLE, [workout_id])

# Fetch all workouts (lightweight columns only)
def get_all_workouts():
    try:
        return db.sql(f"SELECT video_id, channel, title, duration FROM {SCHEMA}.{TABLE}")
    except harperdb.exceptions.HarperDBError:
        #return an empty list if DB errors occur
        return []

# Fetch today’s selected workout
def get_workout_today():
    return db.sql(f"SELECT * FROM {SCHEMA}.{TABLE_TODAY} WHERE id = 0")

# Insert or update the workout of the day
def update_workout_today(workout_data, insert=False):
    workout_data['id'] = 0
    if insert:
        return db.insert(SCHEMA, TABLE_TODAY, [workout_data])
    return db.update(SCHEMA, TABLE_TODAY, [workout_data])
