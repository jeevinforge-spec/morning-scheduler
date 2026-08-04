import pyttsx3

engine = pyttsx3.init()
for index, voice in enumerate(engine.getProperty("voices")):
    print(index, voice.name, voice.id)