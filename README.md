# Connect 4 (Ingescape Circle - Whiteboard)

Project developed by **Bastien LALANNE** and **Marc GUEDON** during the third year of engineering school in Robotic and Interactive Systems at UPSSITECH.
This is a Connect 4 game developed using the Ingescape Circle platform and the Whiteboard. \
Here is the [demonstration video](https://youtu.be/lwDcB8jhxZw).

## Installation

Copy the folders ```Puissance4_View``` and ```Puissance4_Controller``` into the ```sandbox``` folder of your Ingescape installation. \
**WARNING**: Ensure that the folder ```Puissance4_View/data``` remains in this directory! \
The libraries ```pathlib```, ```keyboard``` and ```threading``` are required for the agents to function. Install them if they are not already installed (e.g., ```pip install keyboard```).

## Instructions

### Starting the game

**Automatically** \
You can run the ```launcher.exe``` executable. First, you will have to choose your ```Ingescape Circle v4``` executable via the file explorer, then you will have to choose the port and the device for the connection. \
Everything will be configured and launched automatically, all you have to do is play.

**Manually** \
You can start Ingescape Circle v4 and open ```puissance4.igssystem```. You will also need to start the Whiteboard. \
Make sure the port is the same in Circle, the Whiteboard, as well as in the main files of ```Puissance4_View``` and ```Puissance4_Controller```. \
To start the game, first execute the ```main.py``` file in ```Puissance4_View```, then execute the ```main.py``` file in ```Puissance4_Controller```. \
The game will then start automatically.

### Connect 4 Rules Reminder

The goal of Connect 4 is to align four of your colored tokens horizontally, vertically, or diagonally before your opponent to win the round. \
The grid contains 7 columns and 6 rows, so once a column is full, no more tokens can be placed in it. Turn by turn, the two players will drop tokens into the grid, trying to align four tokens. The token falls to the lowest available slot in the chosen column. \
The game is declared a draw if all columns are filled without either player managing to align four tokens.

**Enjoy the game!**

### Playing the game

To play our Connect 4, all commands are displayed directly on the Whiteboard as well as in the Whiteboard chat. \
In the color selection phase, press the left/right arrow keys (←/→) to change the color, then press "Enter" to confirm your choice. \
During the game phase, press the left/right arrow keys (←/→) to change the column, then press the down arrow key (↓) to confirm the column.

## Known bugs

The game may freeze if the user spams the down arrow key (↓) during the game phase. We have mitigated the occurrence of this bug, but it is unfortunately still present. If this bug occurs, you will need to restart the execution of ```Puissance4_View``` and ```Puissance4_Controller```.