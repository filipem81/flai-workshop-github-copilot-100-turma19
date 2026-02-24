"""
Tests for the High School Management System API
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original participants
    original_participants = {
        name: activity["participants"].copy()
        for name, activity in activities.items()
    }
    yield
    # Restore original participants after test
    for name, activity in activities.items():
        activity["participants"] = original_participants[name].copy()


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_redirects_to_static(self, client):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Tests for the /activities endpoint"""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns 200"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        data = response.json()
        
        # Check that we have activities
        assert len(data) > 0
        
        # Check some expected activities
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_has_correct_structure(self, client):
        """Test that activities have the correct structure"""
        response = client.get("/activities")
        data = response.json()
        
        # Check structure of first activity
        chess_club = data["Chess Club"]
        assert "name" in chess_club
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "category" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)


class TestSignupEndpoint:
    """Tests for the activity signup endpoint"""

    def test_signup_for_existing_activity(self, client):
        """Test signing up for an existing activity"""
        response = client.post(
            "/activities/Chess Club/signup?email=test.student@mergington.edu"
        )
        assert response.status_code == 200
        assert "test.student@mergington.edu" in response.json()["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant"""
        email = "new.student@mergington.edu"
        client.post(f"/activities/Chess Club/signup?email={email}")
        
        # Verify the participant was added
        response = client.get("/activities")
        data = response.json()
        assert email in data["Chess Club"]["participants"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test signing up for a non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_multiple_students(self, client):
        """Test signing up multiple students for the same activity"""
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        
        for email in emails:
            response = client.post(f"/activities/Debate Team/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all were added
        response = client.get("/activities")
        data = response.json()
        for email in emails:
            assert email in data["Debate Team"]["participants"]


class TestRemoveParticipantEndpoint:
    """Tests for the remove participant endpoint"""

    def test_remove_existing_participant(self, client):
        """Test removing an existing participant"""
        # First add a participant
        email = "temp.student@mergington.edu"
        client.post(f"/activities/Chess Club/signup?email={email}")
        
        # Then remove them
        response = client.delete(f"/activities/Chess Club/participants/{email}")
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_remove_participant_actually_removes(self, client):
        """Test that removing a participant actually removes them"""
        # Add a participant
        email = "temp.student@mergington.edu"
        client.post(f"/activities/Chess Club/signup?email={email}")
        
        # Remove the participant
        client.delete(f"/activities/Chess Club/participants/{email}")
        
        # Verify they were removed
        response = client.get("/activities")
        data = response.json()
        assert email not in data["Chess Club"]["participants"]

    def test_remove_from_nonexistent_activity(self, client):
        """Test removing participant from non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/participants/test@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_remove_nonexistent_participant(self, client):
        """Test removing a participant that's not registered"""
        response = client.delete(
            "/activities/Chess Club/participants/nonexistent@mergington.edu"
        )
        assert response.status_code == 404
        assert "Participant not found" in response.json()["detail"]

    def test_remove_participant_from_original_list(self, client):
        """Test removing a participant that was in the original list"""
        # Get original participant from Chess Club
        response = client.get("/activities")
        original_email = response.json()["Chess Club"]["participants"][0]
        
        # Remove the participant
        response = client.delete(f"/activities/Chess Club/participants/{original_email}")
        assert response.status_code == 200
        
        # Verify they were removed
        response = client.get("/activities")
        data = response.json()
        assert original_email not in data["Chess Club"]["participants"]


class TestActivityCategories:
    """Tests for activity categories"""

    def test_activities_have_valid_categories(self, client):
        """Test that all activities have valid categories"""
        response = client.get("/activities")
        data = response.json()
        
        valid_categories = {"intellectual", "sports", "artistic"}
        
        for activity_name, activity in data.items():
            assert activity["category"] in valid_categories, \
                f"{activity_name} has invalid category: {activity['category']}"

    def test_filter_by_category_intellectual(self, client):
        """Test filtering intellectual activities"""
        response = client.get("/activities")
        data = response.json()
        
        intellectual = {
            name: activity for name, activity in data.items()
            if activity["category"] == "intellectual"
        }
        
        assert len(intellectual) >= 4  # Chess Club, Programming Class, Debate Team, Science Club
        assert "Chess Club" in intellectual
        assert "Programming Class" in intellectual

    def test_filter_by_category_sports(self, client):
        """Test filtering sports activities"""
        response = client.get("/activities")
        data = response.json()
        
        sports = {
            name: activity for name, activity in data.items()
            if activity["category"] == "sports"
        }
        
        assert len(sports) >= 3  # Gym Class, Soccer Team, Swimming Club
        assert "Gym Class" in sports
        assert "Soccer Team" in sports

    def test_filter_by_category_artistic(self, client):
        """Test filtering artistic activities"""
        response = client.get("/activities")
        data = response.json()
        
        artistic = {
            name: activity for name, activity in data.items()
            if activity["category"] == "artistic"
        }
        
        assert len(artistic) >= 2  # Art Studio, Drama Club
        assert "Art Studio" in artistic
        assert "Drama Club" in artistic
