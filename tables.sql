
DROP TABLE  Coaches_, Play_,Play_for_, Record_,TEAM, PLAYER, COACH, GAME, STATLINE CASCADE;



CREATE TABLE TEAM(
team_id INTEGER,
team_name CHAR(20) UNIQUE,
region CHAR(20),
PRIMARY KEY(team_id)
);

CREATE TABLE PLAYER(
player_id INTEGER,
player_first_name CHAR(20),
player_last_name CHAR(20),
player_dob DATE,
career_wins INTEGER,
career_games INTEGER,
PRIMARY KEY(player_id)
);

CREATE TABLE COACH(
coach_id INTEGER,
coach_first_name CHAR(20),
coach_last_name CHAR(20),
coach_dob DATE,
career_wins INTEGER,
career_games INTEGER,
PRIMARY KEY(coach_id)
);

CREATE TABLE GAME(
game_id INTEGER,
home_team_id INTEGER, 
away_team_id INTEGER,
points_home_team INTEGER,
points_away_team INTEGER,
PRIMARY KEY(game_id)
);

CREATE TABLE STATLINE(
game_id INTEGER,
minutes_played INTEGER, 
field_goals INTEGER,
field_goals_attempted INTEGER,
three_pointers INTEGER,
three_pointers_attempted INTEGER,
free_throws INTEGER,
free_throws_attempted INTEGER,
offensive_rebounds INTEGER,
defensive_rebounds INTEGER,
assists INTEGER,
steals INTEGER,
blocks INTEGER,
turnovers INTEGER,
personal_fouls INTEGER,
points INTEGER,
player_id INTEGER,
PRIMARY KEY(game_id, player_id),
FOREIGN KEY(game_id) REFERENCES GAME,
FOREIGN KEY(player_id) REFERENCES PLAYER
);




CREATE TABLE Coaches_(
coach_id INTEGER,
team_id INTEGER,
contract_start_date DATE,
contract_end_date DATE,
total_contract_size INTEGER,
PRIMARY KEY(coach_id),
FOREIGN KEY(coach_id) REFERENCES COACH,
FOREIGN KEY(team_id) REFERENCES TEAM
);


CREATE TABLE Play_(
home_team_id INTEGER,
away_team_id INTEGER,
game_id INTEGER,
home_team_name CHAR(20),
away_team_name CHAR(20),
PRIMARY KEY(game_id), 
FOREIGN KEY(game_id) REFERENCES GAME,
FOREIGN KEY(home_team_id) REFERENCES TEAM,
FOREIGN KEY(away_team_id) REFERENCES TEAM
);

CREATE TABLE Play_for_(
player_id INTEGER,
team_id INTEGER,
contract_start_date DATE,
contract_end_date DATE,
total_contract_size INTEGER,
player_first_name CHAR(20),
player_last_name CHAR(20),
team_name CHAR(20) UNIQUE,
region CHAR(20),
PRIMARY KEY(player_id, team_id), 
FOREIGN KEY(player_id) REFERENCES PLAYER,
FOREIGN KEY(team_id) REFERENCES TEAM
);

CREATE TABLE Record_(
player_id INTEGER,
game_id INTEGER,
PRIMARY KEY(player_id, game_id),
FOREIGN KEY(player_id) REFERENCES PLAYER,
FOREIGN KEY(game_id) REFERENCES GAME
);
