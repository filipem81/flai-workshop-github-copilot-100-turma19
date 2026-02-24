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
        "participants": []
    },
    "Programming Class": {
        "name": "Programming Class",
        "description": "Introduction to Python programming",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
        "category": "intellectual",
        "participants": []
    },
    "Gym Class": {
        "name": "Gym Class",
        "description": "Physical education and fitness training",
        "schedule": "Daily, 3:00 PM - 4:30 PM",
        "category": "sports",
        "participants": []
    },
    "Soccer Team": {
        "name": "Soccer Team",
        "description": "Competitive soccer training and matches",
        "schedule": "Mondays, Wednesdays, and Fridays, 4:00 PM - 6:00 PM",
        "category": "sports",
        "participants": []
    },
    "Swimming Club": {
        "name": "Swimming Club",
        "description": "Learn swimming techniques and compete in meets",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
        "category": "sports",
        "participants": []
    },
    "Art Studio": {
        "name": "Art Studio",
        "description": "Painting, drawing, and mixed media exploration",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:30 PM",
        "category": "artistic",
        "participants": []
    },
    "Drama Club": {
        "name": "Drama Club",
        "description": "Acting, theater performance, and stage production",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "category": "artistic",
        "participants": []
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
        "participants": []
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
