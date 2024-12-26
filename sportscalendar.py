import requests
from datetime import datetime, timedelta
import pytz
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Define constants
API_KEY = "86979342bc054be5b015d51cbf103ec0"
BASE_URL = "https://api.football-data.org/v4/teams/57/matches"  # Arsenal's matches endpoint
HEADERS = {"X-Auth-Token": API_KEY}
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Authenticate with Google Calendar API
def authenticate_google_calendar():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("calendar", "v3", credentials=creds)

# Fetch existing events from Google Calendar
def get_existing_events(service):
    now = datetime.utcnow().isoformat() + "Z"
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    existing_events = {
        event["summary"]: event["start"].get("dateTime", event["start"].get("date"))
        for event in events
    }
    return existing_events

# Add match details to Google Calendar
def add_to_google_calendar(service, match, brisbane_date, existing_events):
    event_summary = f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}"
    event_start_time = brisbane_date.isoformat()

    # Check if the event already exists
    if event_summary in existing_events and existing_events[event_summary] == event_start_time:
        print(f"Event already exists: {event_summary} on {event_start_time}")
        return

    event = {
        "summary": event_summary,
        "location": match.get("venue", "TBA"),
        "description": f"Competition: {match['competition']['name']}",
        "start": {
            "dateTime": event_start_time,
            "timeZone": "Australia/Brisbane",
        },
        "end": {
            "dateTime": (brisbane_date + timedelta(hours=2)).isoformat(),  # Assuming 2-hour match duration
            "timeZone": "Australia/Brisbane",
        },
    }

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {created_event.get('htmlLink')}")

# Fetch Arsenal matches and add them to Google Calendar
def get_arsenal_matches_with_calendar():
    params = {"status": "SCHEDULED"}  # Retrieve only upcoming matches

    try:
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        response.raise_for_status()
        matches = response.json().get("matches", [])

        if not matches:
            print("No upcoming matches found for Arsenal.")
            return

        service = authenticate_google_calendar()
        existing_events = get_existing_events(service)

        # Brisbane timezone
        brisbane_tz = pytz.timezone("Australia/Brisbane")

        for match in matches:
            # Convert UTC date to Brisbane time
            utc_date = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
            brisbane_date = utc_date.replace(tzinfo=pytz.utc).astimezone(brisbane_tz)

            # Print match details
            competition = match["competition"]["name"]
            home_team = match["homeTeam"]["name"]
            away_team = match["awayTeam"]["name"]
            venue = match.get("venue", "TBA")
            print(f"Competition: {competition}")
            print(f"Date: {brisbane_date.strftime('%Y-%m-%d %H:%M:%S')} (Brisbane Time)")
            print(f"Match: {home_team} vs {away_team}")
            print(f"Venue: {venue}")
            print("-" * 40)

            # Add to Google Calendar
            add_to_google_calendar(service, match, brisbane_date, existing_events)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Run the function
if __name__ == "__main__":
    get_arsenal_matches_with_calendar()
