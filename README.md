#README
Socket Programming Project

# Statement of Work (SOW)

## Project Title: Connect 4 - ONLINE PEW PEW POW THE ACTION GAME BWAHHHHHHH

**Team:** Lukas Elerson

## Project Objective
To create an online, browser-based Connect 4 game.

## Scope

### Inclusions
- Online connectivity
- Simple browser-based GUI
- Basic Connect Four functionality
- Server-Client Architecture: The game must implement a clear server-client architecture, with the server handling game state and communication between clients.
- Game Logic: The game must accurately implement the rules of the game (as defined in your SOW):
Alternating turns between players.Determining the winner.
Handling draw conditions.
-Multiplayer Capability: The game should allow multiple clients to connect and play simultaneously.
Error Handling: The game should gracefully handle common errors, such as network failures, invalid input, or unexpected game states.

### Exclusions
- None

## Deliverables
- Fully functioning Python script to handle game mechanics COMPLETE
- Optional: GUI implemented using an HTML library if not handled by the Python script DID NOT COMPLETE

### Key Milestones
- **Sprint 0:** [Form teams, Setup Tools, Submit SOW] - Sept 08-Sept 22 COMLETE
- **Sprint 1:** [Socket Programming, TCP Client Server] -  Sept 22-Oct 06 COMLETE
- **Sprint 2:** [Develop Game Message Protocol, Manage Client connections] -  Oct 06-Oct 20 COMLETE
- **Sprint 3:** [Multi-player functionality, Synchronize state across clients] - Oct 20-Nov 03 COMLETE
- **Sprint 4:** [Game play, Game State] - Nov 03-Nov 17 COMPLETE
- **Sprint 5:** [Implement Error Handling and Testing] - Nov 17-Dec 6 COMPLETE

### Task Breakdown
- **Task 1:** [Implement Server] - Estimated Duration: [8/1]  COMPLETE
- **Task 2:** [Implement Client] - Estimated Duration: [8/1]  COMLETE
- **Task 3:** [Sync State] - Estimated Duration: [8]  COMPLETE
- **Task 4:** [Gameplay, Gamestate, UI] - Estimated Duration [8] COMLETE

## Technical Requirements

### Hardware
- Windows or linux machine  

### Software
- **Programming Languages:** Python
- **Libraries:** socket, threading, json, argparse, logging
- **Operating Systems:** Windows, Linux

## Assumptions
- Will require available network
- will require modern browser than can support gui

## Roles and Responsibilities
- **Project Manager:** [Lukas Eelrson] - [Keeping with required timelines and expectations]
- **Developers:** [Lukas Elerson] - [Developing all code required]
- **Testers:** [Lukas Elerson] - [TEsting functionality of code]

## Communication Plan
Single person team, so will not be accounted for
- **Channels:** N/A
- **Frequency:** N/A
- **Decision-Making:** N/A

## Additional Notes
- run using Python3, has not been tested with Python2

- Server can now be ran using following command:
    "python3 server.py -p PORT" 
    ex. "python3 server.py -p 12345"

- Client can be ran using following command:
    "python3 client.py -i SERVER_ID -p PORT" .
    ex. "python3 client.py -i 0.0.0.0 -p 12345"

## Functionalities

- Connect 4 game, runs in CLI. Players can "move", "chat", and exit game
- Chat functionality allows players to communicate while playing
- Players can play a full game of Connect 4 

## Known Issues

- I was unable to implement a way to gracefully handle when a player disconnects. As far as what I should do with the remaining player
- The state of the game is saves when a player leaves, that player is not able to rejoin and play because they get a new ID so it will always not be their turn
- There is an issue that appears from time to time that I am unable to fix where a client will randomly just stop updating. Ihave not been able to find
any reason behind this or been able to recreate this issue, it just seems to happen at random times.




