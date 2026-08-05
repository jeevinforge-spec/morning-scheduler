"""
Morning Scheduler
------------------
Checks the current time against a hardcoded daily schedule and speaks
the next upcoming event out loud.

Works on Windows (pyttsx3 / SAPI5) and on Android under Termux
(termux-tts-speak, from the termux-api package).
"""

import shutil
import subprocess
from datetime import datetime

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
    """Return the first event later than 'now', or None if the day is done."""
    for time_str, description in sorted(schedule):
        event_time = datetime.strptime(time_str, "%H:%M").time()
        if event_time > now:
            return time_str, description
    return None


def format_time_for_speech(time_str):
    """Turn '08:30' into '8:30 AM' so it's spoken naturally, not as digits."""
    return datetime.strptime(time_str, "%H:%M").strftime("%I:%M %p").lstrip("0")


def speak(text, voice_index=1, rate=175):
    """Speak 'text' using whichever engine this device actually has."""
    # Android / Termux: use the phone's own TTS engine.
    if shutil.which("termux-tts-speak"):
        subprocess.run(["termux-tts-speak", text])
        return

    # Windows: import here, not at the top, so this file still runs on
    # Android where pyttsx3 isn't installed.
    import pyttsx3

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[voice_index].id)
    engine.setProperty("rate", rate)
    engine.say(text)
    engine.runAndWait()


def main():
    now = datetime.now().time()
    next_event = get_next_event(SCHEDULE, now)

    if next_event:
        time_str, description = next_event
        message = f"Your next event is {description} at {format_time_for_speech(time_str)}."
    else:
        message = "You have no more events scheduled for today."

    print(message)
    speak(message)


if __name__ == "__main__":
    main()