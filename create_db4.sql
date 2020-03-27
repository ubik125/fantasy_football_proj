USE fantasy_football;

create table player (
	player_id int not null,
    player_name varchar(30) not null,
    primary key (player_id)
    );

create table team (
	team_id int not null,
	team_name varchar(30) not null,
	team_slug varchar(30),
	team_gender enum('M', 'F'),
	is_national bool,
	primary key (team_id)
	);
    
create table season (
	season_id int not null,
	season_name varchar(30) not null,
	primary key (season_id)
	);

create table tournament (
	tournament_id int not null,
	tournament_name varchar(30) not null,
	primary key(tournament_id)
	);

create table team_season (
	team_season_id int  not null auto_increment,
    team_id int not null,
    season_id int not null,
    primary key (team_season_id),
    foreign key (team_id) references team(team_id)
    on update cascade
    on delete cascade,
    foreign key (season_id) references season(season_id)
    on update cascade
    on delete cascade
    );
    
create table season_tournament (
	season_tourn_id int not null auto_increment,
    season_id int not null,
    tournament_id int not null,
    primary key (season_tourn_id),
    foreign key (season_id) references season(season_id)
    on update cascade
    on delete cascade,
    foreign key (tournament_id) references tournament(tournament_id)
    on update cascade
    on delete cascade
    );
    
create table player_team_season (
	player_team_season_id int not null auto_increment,
	player_id int not null,
    team_season_id int not null,
    is_active bool,
    primary key (player_team_season_id),
    foreign key (team_season_id) references team_season(team_season_id)
    on update cascade
    on delete cascade,
    foreign key (player_id) references player(player_id)
    on update cascade
    on delete cascade
    );

create table matches (
	match_id int not null,
    match_name varchar(30) not null,
    season_tourn_id int not null,
	home_team_season_id int not null,
    away_team_season_id int not null,
	start_hour time,
	match_date date,
    stadium varchar(60), 
    country varchar(20),
    primary key (match_id),
    foreign key (season_tourn_id) references season_tournament(season_tourn_id)
    on update cascade
    on delete cascade,
    foreign key (home_team_season_id) references team_season(team_season_id)
    on update cascade
    on delete cascade,
    foreign key (away_team_season_id) references team_season(team_season_id)
    on update cascade
    on delete cascade
    );
    
create table player_match_stats (
	player_match_stats_id int not null auto_increment,
    player_team_season_id int not null,
    match_id int not null,
	goals tinyint, 
	goal_assist smallint,
	total_tackle smallint,
	total_pass smallint,
	total_duels smallint,
	ground_duels smallint,
	aerial_duels smallint,
	minutes_played smallint,
	position char(1), 
	rating char(3),
	shots_on_target smallint,
	shots_off_target smallint,
	shots_blocked smallint,
	total_contest smallint,
	total_clearance smallint,
	outfielder_block smallint,
	interception_won smallint,
	challenge_lost smallint,
	touches smallint,
	accurate_pass smallint,
	key_pass smallint,
	total_cross smallint,
	total_longballs smallint,
	possession_lost smallint,
	fouls smallint,
	fouls_suffered smallint, 
	saves smallint,
	punches smallint,
	runs_out smallint,
	good_high_claim smallint,
	primary key (player_match_stats_id),
    foreign key (player_team_season_id) references player_team_season(player_team_season_id)
    on update cascade
    on delete cascade,
    foreign key (match_id) references matches(match_id)
    on update cascade
    on delete cascade
    ); 

CREATE TABLE match_stats (
	match_stats_id INT NOT NULL AUTO_INCREMENT,
	match_id INT NOT NULL,
	home_score TINYINT,
	away_score TINYINT,
	home_best_player_id INT NOT NULL,
	away_best_player_id INT NOT NULL,
    home_formation VARCHAR(6),
	 away_formation VARCHAR(6),
	 away_1st_accurate_passes SMALLINT,
	 away_1st_aerials_won SMALLINT,
	 away_1st_ball_possession SMALLINT,
	 away_1st_big_chances SMALLINT,
	 away_1st_big_chances_missed SMALLINT,
	 away_1st_blocked_shots SMALLINT,
	 away_1st_clearances SMALLINT,
	 away_1st_corner_kicks SMALLINT,
	 away_1st_counter_attacks SMALLINT,
	 away_1st_crosses SMALLINT,
	 away_1st_dribbles SMALLINT,
	 away_1st_duels_won SMALLINT,
	 away_1st_goalkeeper_saves SMALLINT,
	 away_1st_hit_woodwork SMALLINT,
	 away_1st_interceptions SMALLINT,
	 away_1st_long_balls SMALLINT,
	 away_1st_offsides SMALLINT,
	 away_1st_passes SMALLINT,
	 away_1st_possession_lost SMALLINT,
	 away_1st_red_cards SMALLINT,
	 away_1st_shots_inside_box SMALLINT,
	 away_1st_shots_off_target SMALLINT,
	 away_1st_shots_on_target SMALLINT,
	 away_1st_shots_outside_box SMALLINT,
	 away_1st_tackles SMALLINT,
	 away_1st_total_shots SMALLINT,
	 away_1st_yellow_cards SMALLINT,
	 away_2nd_accurate_passes SMALLINT,
	 away_2nd_aerials_won SMALLINT,
	 away_2nd_ball_possession SMALLINT,
	 away_2nd_big_chances SMALLINT,
	 away_2nd_big_chances_missed SMALLINT,
	 away_2nd_blocked_shots SMALLINT,
	 away_2nd_clearances SMALLINT,
	 away_2nd_corner_kicks SMALLINT,
	 away_2nd_counter_attacks SMALLINT,
	 away_2nd_crosses SMALLINT,
	 away_2nd_dribbles SMALLINT,
	 away_2nd_duels_won SMALLINT,
	 away_2nd_goalkeeper_saves SMALLINT,
	 away_2nd_hit_woodwork SMALLINT,
	 away_2nd_interceptions SMALLINT,
	 away_2nd_long_balls SMALLINT,
	 away_2nd_offsides SMALLINT,
	 away_2nd_passes SMALLINT,
	 away_2nd_possession_lost SMALLINT,
	 away_2nd_red_cards SMALLINT,
	 away_2nd_shots_inside_box SMALLINT,
	 away_2nd_shots_off_target SMALLINT,
	 away_2nd_shots_on_target SMALLINT,
	 away_2nd_shots_outside_box SMALLINT,
	 away_2nd_tackles SMALLINT,
	 away_2nd_total_shots SMALLINT,
	 away_2nd_yellow_cards SMALLINT,
	 away_tot_accurate_passes SMALLINT,
	 away_tot_aerials_won SMALLINT,
	 away_tot_ball_possession SMALLINT,
	 away_tot_big_chances SMALLINT,
	 away_tot_big_chances_missed SMALLINT,
	 away_tot_blocked_shots SMALLINT,
	 away_tot_clearances SMALLINT,
	 away_tot_corner_kicks SMALLINT,
	 away_tot_counter_attacks SMALLINT,
	 away_tot_crosses SMALLINT,
	 away_tot_dribbles SMALLINT,
	 away_tot_duels_won SMALLINT,
	 away_tot_fouls SMALLINT,
	 away_tot_goalkeeper_saves SMALLINT,
	 away_tot_hit_woodwork SMALLINT,
	 away_tot_interceptions SMALLINT,
	 away_tot_long_balls SMALLINT,
	 away_tot_offsides SMALLINT,
	 away_tot_passes SMALLINT,
	 away_tot_possession_lost SMALLINT,
	 away_tot_red_cards SMALLINT,
	 away_tot_shots_inside_box SMALLINT,
	 away_tot_shots_off_target SMALLINT,
	 away_tot_shots_on_target SMALLINT,
	 away_tot_shots_outside_box SMALLINT,
	 away_tot_tackles SMALLINT,
	 away_tot_total_shots SMALLINT,
	 away_tot_yellow_cards SMALLINT,
	 home_1st_accurate_passes SMALLINT,
	 home_1st_aerials_won SMALLINT,
	 home_1st_ball_possession SMALLINT,
	 home_1st_big_chances SMALLINT,
	 home_1st_big_chances_missed SMALLINT,
	 home_1st_blocked_shots SMALLINT,
	 home_1st_clearances SMALLINT,
	 home_1st_corner_kicks SMALLINT,
	 home_1st_counter_attacks SMALLINT,
	 home_1st_crosses SMALLINT,
	 home_1st_dribbles SMALLINT,
	 home_1st_duels_won SMALLINT,
	 home_1st_goalkeeper_saves SMALLINT,
	 home_1st_hit_woodwork SMALLINT,
	 home_1st_interceptions SMALLINT,
	 home_1st_long_balls SMALLINT,
	 home_1st_offsides SMALLINT,
	 home_1st_passes SMALLINT,
	 home_1st_possession_lost SMALLINT,
	 home_1st_red_cards SMALLINT,
	 home_1st_shots_inside_box SMALLINT,
	 home_1st_shots_off_target SMALLINT,
	 home_1st_shots_on_target SMALLINT,
	 home_1st_shots_outside_box SMALLINT,
	 home_1st_tackles SMALLINT,
	 home_1st_total_shots SMALLINT,
	 home_1st_yellow_cards SMALLINT,
	 home_2nd_accurate_passes SMALLINT,
	 home_2nd_aerials_won SMALLINT,
	 home_2nd_ball_possession SMALLINT,
	 home_2nd_big_chances SMALLINT,
	 home_2nd_big_chances_missed SMALLINT,
	 home_2nd_blocked_shots SMALLINT,
	 home_2nd_clearances SMALLINT,
	 home_2nd_corner_kicks SMALLINT,
	 home_2nd_counter_attacks SMALLINT,
	 home_2nd_crosses SMALLINT,
	 home_2nd_dribbles SMALLINT,
	 home_2nd_duels_won SMALLINT,
	 home_2nd_goalkeeper_saves SMALLINT,
	 home_2nd_hit_woodwork SMALLINT,
	 home_2nd_interceptions SMALLINT,
	 home_2nd_long_balls SMALLINT,
	 home_2nd_offsides SMALLINT,
	 home_2nd_passes SMALLINT,
	 home_2nd_possession_lost SMALLINT,
	 home_2nd_red_cards SMALLINT,
	 home_2nd_shots_inside_box SMALLINT,
	 home_2nd_shots_off_target SMALLINT,
	 home_2nd_shots_on_target SMALLINT,
	 home_2nd_shots_outside_box SMALLINT,
	 home_2nd_tackles SMALLINT,
	 home_2nd_total_shots SMALLINT,
	 home_2nd_yellow_cards SMALLINT,
	 home_tot_accurate_passes SMALLINT,
	 home_tot_aerials_won SMALLINT,
	 home_tot_ball_possession SMALLINT,
	 home_tot_big_chances SMALLINT,
	 home_tot_big_chances_missed SMALLINT,
	 home_tot_blocked_shots SMALLINT,
	 home_tot_clearances SMALLINT,
	 home_tot_corner_kicks SMALLINT,
	 home_tot_counter_attacks SMALLINT,
	 home_tot_crosses SMALLINT,
	 home_tot_dribbles SMALLINT,
	 home_tot_duels_won SMALLINT,
	 home_tot_fouls SMALLINT,
	 home_tot_goalkeeper_saves SMALLINT,
	 home_tot_hit_woodwork SMALLINT,
	 home_tot_interceptions SMALLINT,
	 home_tot_long_balls SMALLINT,
	 home_tot_offsides SMALLINT,
	 home_tot_passes SMALLINT,
	 home_tot_possession_lost SMALLINT,
	 home_tot_red_cards SMALLINT,
	 home_tot_shots_inside_box SMALLINT,
	 home_tot_shots_off_target SMALLINT,
	 home_tot_shots_on_target SMALLINT,
	 home_tot_shots_outside_box SMALLINT,
	 home_tot_tackles SMALLINT,
	 home_tot_total_shots SMALLINT,
	 home_tot_yellow_cards SMALLINT,	
	primary key (match_stats_id),
    foreign key (match_id) references matches(match_id)
    on update cascade
    on delete cascade,
    foreign key (home_best_player_id) references player_team_season(player_team_season_id)
    on update cascade
    on delete cascade,
    foreign key (away_best_player_id) references player_team_season(player_team_season_id)
    on update cascade
    on delete cascade
    );