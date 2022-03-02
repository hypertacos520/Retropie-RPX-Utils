# Retropie RPX Utils

Retropie RPX Utils are a collection of utilities I felt were missing from Retropie. The aim of these utilities are to provide more modern console features to a Retropie based system.

Some of these features include:

- System Level Screenshots
- Ingame System Menu (Pauses Game)
- Notification Overlay 
- On-Screen Keyboard (Not Currently Implemented)

The reason for making these tools are to enhance the user experience for a custom handheld I've been developing, [RP3P](https://github.com/hypertacos520/RP3P-Handheld). More features may be added based on the needs of that particular project.

How it Currently Works:

Overlays are rendered to the Raspberry Pi display output using DispmanX and PyGame. PyGame is inherently inefficient for this usecase, so both the graphic resources in the overlay and pygame itself are initialized when the function is called, then removed once execution has finished. This helps reduce both memory and cpu usage. A similar method is used when rendering the in-game overlay, however, the currently running game process pauses execution when this menu is displayed. Based on the option picked in this menu, the game process will either resume where it left off, or terminate to the main menu.

Python Libraries (WIP List): 

Library | Language / Platform | URL / Source
------- | ------------------- | ------------
[raspi2png](https://github.com/AndrewFromMelbourne/raspi2png) | C / Raspberry Pi | Included as Submodule
[gamepad](https://github.com/piborg/Gamepad) | Python / Raspberry Pi | Included as Submodule
[pydispmanx](https://github.com/eclispe/pyDispmanx) | C / Raspberry Pi | Included as Submodule
pygame  |Python / Raspberry Pi| pip install pygame
pillow  |Python / Raspberry Pi| pip install pillow

Current Goals:

- Add User Callable On-Screen Keyboard
- Rewrite systemFunctions.py in C for faster System-Level operations