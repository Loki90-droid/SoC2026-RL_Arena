# DESCRIPTION OF ALL WORK TILL MIDTERM

## WEEK-1

It was a basic python 2D array(board) based game which was just taking input and updating the board.

It was pretty straight forward,given all the files(utils) required.

## WEEK-2

I think from this week the tileman.io result was being visible,yea i basically gave death logic in the `update()` method of the class `Game`

I completed the drawing function of grid and the players which were just pygame.draw.line and pygame.draw.rect

For the movement of the players I created a dict for next positions of each player and found out with these next positions who will die and made movements only for the alive players.

## WEEK-3

I loved learning about the flood-fill algo, i was also learning about chess engines using RL

So while exploring alpha beta pruningI learned some what about BFS and DFS it was nice implementing that,
and how here we can flood fill from boundary and find what all are left over cells as the territory of our player.

Yeah here I just updated the death logics as required and added the reconnecting logic,I also used faded colors for trails and gave a small territory to each player in the start.

I learnt about that `pygame.surfarray.blit_array()` method which helped to draw the board in one go and I used numpy array searching to
find the color cells faster.

I am thinking of adding the feature of capturing enemy's territory also as in paper.io.

## WEEK-4

I first explored the CartPole example to understand how Gymnasium environments interact with a PPO agent.

For the maze environment,the action space was defined with four possible movements and the observation space as a 10×10 grid for the maze. The observation keeps track of walls, empty cells, the goal position and the current position of the agent.

The `reset()` function puts the agent back at the starting position at the start of every episode, the `step()` function handles movement, checks whether the next cell is valid and gives rewards and penalties based on the action taken. A visited array was maintained to discourage the agent from revisiting the same cells repeatedly.

A maximum step limit was introduced to prune episodes that run for too long, and the observations were normalized before given to the model.Finally, the maze was represented as RGB combination using numpy and rendered using Pygame to visualize the trained agent reaching to the goal.
