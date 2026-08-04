"""
Morning Scheduler
------------------
Checks the current time against a hardcoded daily schedule and speaks
the next upcoming event out loud using Windows text-to-speech.
"""

from datetime import datetime
import pyttsx3

# --- 1. The hardcoded schedule ---
# Each entry is (time as "HH:MM" in 24-hour format, event description).
# Feel free to edit these to match your actual day.
SCHEDULE = [
    ("07:00", "Wake up and stretch"),
    ("07:30", "Breakfast"),
    ("08:30", "Stand-up meeting"),
    ("09:00", "Deep work block"),
    ("12:00", "Lunch"),
    ("13:00", "Team sync"),
    ("15:00", "Gym"),
    ("18:00", "Dinner"),
    ("21:00", "Wind down and read"),
]


def get_next_event(schedule, now):
    """
    Walk through the schedule and return the first event whose time
    is still later than 'now'. Returns None if the day is done.
    """
    for time_str, description in schedule:
        # Turn "07:30" into a real time object we can compare against 'now'.
        event_time = datetime.strptime(time_str, "%H:%M").time()
        if event_time > now:
            return time_str, description
    return None


def speak(text, voice_index=1, rate=175):
    """Speak 'text' using the selected Windows voice."""
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voice_index].id)

    engine.setProperty("rate", rate)  # words per minute; default ~200

    engine.say(text)
    engine.runAndWait()

def main():
    now = datetime.now().time()
    next_event = get_next_event(SCHEDULE, now)

    if next_event:
        time_str, description = next_event
        message = f"Your next event is {description} at {time_str}."
    else:
        message = "You have no more events scheduled for today."

    print(message)  # also show it in the terminal
    speak(message)


if __name__ == "__main__":
    main()
