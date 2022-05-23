The client is a kivy app, using https://github.com/kivy-garden/garden.joystick. Because I had trouble building the app for Android, I included the `garden.joystick` module in the `garden_joystick` folder (sans `examples`).

run `buildozer android debug` to get the apk (some dependencies are needed for buildozer)