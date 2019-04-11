COMS 4111 Intro to Database Porject 1

Jun Hyek Jang, UNI: jj2883

1) Postgresql
User id: jj2883

2) URL of application
http://35.237.59.40:8111/

3) Implementation from Part 1

I implemented the application such that the webpage lists all the information on NBA Players, Teams Games and Statlines. Using the available database, user can search up various specific informations such as the teams that players are affiliated with, games they have played and the game stats of the players in a game.

Since my partner dropped the class after the midterm, I did not include the information on the Coaches or Owners as I have stated in the contingency plan.

4)
The first page that I think was interesting was the 'Player' page. The 'Player' page displays the list of players, and if an user wants to know specific information such as teams they play for, they can use this page to search specific information. For example, if an user wants to know which team a specific player plays in, the webpage takes in the user input from a search bar and runs a query to select the team name from Player and Play_for_ tables and display the result on the webpage.

The second page that I think was interesting was the 'Statline'. The 'Statline' page displays the list of game statlines that players achieved in respective games. The users can use this page to search up for the players and game that each statline corresponds to. If an user wants to know which player recorded which statline, the webpage takes in the user input from a search bar and runs a query to select the player names from Player and Records_ tables and display the result on the webpage.