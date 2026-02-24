"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
# ...existing code...
# Sample activities
activities = {
    "Chess Club": {
        "name": "Chess Club",
        "description": "Learn and play chess with fellow students",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "category": "intellectual",
        "participants": ["alice.smith@mergington.edu", "bob.jones@mergington.edu", "carol.white@mergington.edu"]
    },
    "Programming Class": {
        "name": "Programming Class",
        "description": "Introduction to Python programming",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "category": "intellectual",
        "participants": ["david.brown@mergington.edu", "emma.davis@mergington.edu"]
    },
    "Gym Class": {
        "name": "Gym Class",
        "description": "Physical education and fitness training",
        "schedule": "Daily, 3:00 PM - 4:30 PM",
        "category": "sports",
        "participants": ["frank.miller@mergington.edu", "grace.wilson@mergington.edu", "henry.moore@mergington.edu", "iris.taylor@mergington.edu"]
    },
    "Soccer Team": {
        "name": "Soccer Team",
        "description": "Competitive soccer training and matches",
        "schedule": "Mondays, Wednesdays, and Fridays, 4:00 PM - 6:00 PM",
        "category": "sports",
        "participants": ["jack.anderson@mergington.edu", "kate.thomas@mergington.edu"]
    },
    "Swimming Club": {
        "name": "Swimming Club",
        "description": "Learn swimming techniques and compete in meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "category": "sports",
        "participants": ["liam.jackson@mergington.edu"]
    },
    "Art Studio": {
        "name": "Art Studio",
        "description": "Painting, drawing, and mixed media exploration",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:30 PM",
        "category": "artistic",
        "participants": ["mia.martin@mergington.edu", "noah.garcia@mergington.edu", "olivia.lopez@mergington.edu"]
    },
    "Drama Club": {
        "name": "Drama Club",
        "description": "Acting, theater performance, and stage production",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "category": "artistic",
        "participants": ["peter.lee@mergington.edu", "quinn.harris@mergington.edu"]
    },
    "Debate Team": {
        "name": "Debate Team",
        "description": "Develop critical thinking and public speaking skills",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "category": "intellectual",
        "participants": []
    },
    "Science Club": {
        "name": "Science Club",
        "description": "Hands-on experiments and science competitions",
        "schedule": "Thursdays and Fridays, 3:30 PM - 5:30 PM",
        "category": "intellectual",
        "participants": ["rachel.clark@mergington.edu"]
    }
}
# 


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/participants/{email}")
def remove_participant(activity_name: str, email: str):
    """Remove a participant from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if participant is registered
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in this activity")

    # Remove participant
    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
