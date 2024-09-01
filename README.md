# Rock, Paper, Scissors, Lizard, Spock

Welcome to the GitHub repository for a multiplayer "Rock, Paper, Scissors, Lizard, Spock" game! This project brings the popular game variation to life using Python and Socket.IO for real-time gameplay between multiple players.

## Description

"Rock, Paper, Scissors, Lizard, Spock" is an expansion of the classic decision-making game that adds two new elements, increasing the complexity and fun. This implementation allows players from different devices to connect to a central server and compete against each other in real-time.

## Features

- **Multiplayer Gameplay**: Connect and play with friends or random players.
- **Real-time Updates**: Game moves and results are updated in real-time.
- **Dynamic Room Management**: Players can join existing games or start new ones.
- **Extendable Framework**: Easy to modify and extend with additional features or rules.

## Tech Stack

- **Python**: Core programming language.
- **Socket.IO**: Enables real-time bidirectional event-based communication.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or higher installed on your machine. You also need to install the following packages:

- `socketio`
- `aiohttp`
- `python-socketio[client]`

### Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/rock-paper-scissors-lizard-spock.git
cd rock-paper-scissors-lizard-spock
pip install aiohttp python-socketio
```

### Running the Server

To start the server, run:
```bash
python server.py
```
### Running the Client

Open another terminal and start the client:

```bash
python client.py
```

## How to Play

After starting the client, you will be prompted to choose your move:

1. Rock
2. Paper
3. Scissors
4. Lizard
5. Spock
0. Quit Game

Enter the number corresponding to your choice and based on it server with respond.

## Contributing
Interested in contributing? Great! Here's how you can help:

1. Fork the repository.
2. Create your feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a pull request.

## License
Distributed under the MIT License. See LICENSE for more information.