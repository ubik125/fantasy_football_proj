# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 10:36:46 2020

@author: Alessandro
"""

import json
import requests
import time
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

JSON_SEASON_URL = 'https://www.sofascore.com/u-tournament/23/season/17932/matches/round/'
EVENT_URL = 'https://www.sofascore.com/event/'
MATCH_JSON_URL = '/json?_=157878006'
PLAYERS_JSON_URL = '/statistics/players/json?_=157878006'
BAD_CHARS = ["'", "%", "(",")", "/", "[", "]", "`",",", " ","-","–"]
PLAYER_MATCH_STATS_COLS = ['player_team_season_id', 'match_id', 'goals',
       'goal_assist', 'total_tackle', 'total_pass', 'total_duels', 'ground_duels',
       'aerial_duels', 'minutes_played', 'position', 'rating', 'shots_on_target',
       'shots_off_target', 'shots_blocked', 'total_contest', 'total_clearance',
       'outfielder_block', 'interception_won', 'challenge_lost', 'touches',
       'accurate_pass', 'key_pass', 'total_cross', 'total_longballs',
       'possession_lost', 'fouls', 'fouls_suffered', 'saves', 'punches', 'runs_out',
       'good_high_claim']

def fetch_round_data(round_url):
    response_round = requests.get(round_url)
    round_data = json.loads(response_round.text)
    return round_data

def fill_match_list(round_dict, matches_list):
    for event in round_dict:
        if event['id'] not in matches_list:
            matches_list.append(event['id'])
    return matches_list

def fetch_season_data(season_url):
    match_list = []
    for roundn in range(1, 39):
        round_url = f'{season_url}' + f'{roundn}'
        round_data = fetch_round_data(round_url)
        match_list = fill_match_list(round_data['roundMatches']['tournaments'][0]['events'], match_list)
        time.sleep(1)
    return match_list

def fetch_match_data(match_url):
    response_match = requests.get(match_url)
    match_data = json.loads(response_match.text)
    return match_data

def fetch_players_data(players_url):
    response_players = requests.get(players_url)
    players_data = json.loads(response_players.text)
    return players_data

def extract_player(players_data):
    player_list = []
    for player in players_data['players']:
        player_list.append({'player_id':player['player']['id'],
                            'player_name':player['player']['name'] })
    return player_list

def extract_season(match_data):
    season_dic = {'season_id':match_data['event']['season']['id'],
                  'season_name':match_data['event']['season']['year']}
    return season_dic

def extract_tournament(match_data):
    tournament_dic = {'tournament_id':match_data['event']['tournament']['id'],
                      'tournament_name':match_data['event']['tournament']['name']}
    return tournament_dic

def extract_team(match_data):
    teams_list = []
    keys = ["id", "name", "slug", "gender"]
    def fill(home_away):
        names = []
        values = []
        for name in list(match_data["event"][home_away +'Team'].keys()):
            if name in keys:
                values.append(match_data["event"][home_away +'Team'][name])
                names.append('team_'+ f'{name}')
        values.append(match_data["event"][home_away +'Team']['national'])
        names.append('is_national')
        ha_dict = dict(zip(names, values))
        return ha_dict
    home = fill('home')
    away = fill('away')
    teams_list.append(home)
    teams_list.append(away)
    return teams_list

def create_season_tournament(match_data):
    season_tournament_dic = {'season_id': match_data['event']['season']['id'],
                             'tournament_id':match_data['event']['tournament']['id']}
    return season_tournament_dic

def create_team_season(match_data):
    team_season_list = [{'team_id': match_data["event"]["homeTeam"]['id'],
                         'season_id': match_data['event']['season']['id']},
                        {'team_id': match_data["event"]["awayTeam"]['id'],
                         'season_id': match_data['event']['season']['id']}]                 
    return team_season_list

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
            
def create_player_team_season(match_data, players_data):
    home_id = match_data["event"]["homeTeam"]['id']
    away_id = match_data["event"]["awayTeam"]['id']
    seas_id = match_data['event']['season']['id']
    with session_scope() as session:
        hts_id = session.query(Team_season.team_season_id).filter(Team_season.team_id==home_id,
                                                                  Team_season.season_id==seas_id).scalar()
        ats_id = session.query(Team_season.team_season_id).filter(Team_season.team_id==away_id,
                                                                  Team_season.season_id==seas_id).scalar()
    pts_list = []
    for player in players_data['players']:
        if player['team']['id'] == home_id:
            pts_list.append({'player_id': player['player']['id'],
                             'team_season_id': hts_id,
                             'is_active': True})
        elif player['team']['id'] == away_id:
            pts_list.append({'player_id': player['player']['id'],
                             'team_season_id': ats_id,
                             'is_active': True})
    return pts_list

def create_matches(match_data):
    home_id = match_data["event"]["homeTeam"]['id']
    away_id = match_data["event"]["awayTeam"]['id']
    with session_scope() as session:
        hts_id = session.query(Team_season.team_season_id).filter(Team_season.team_id==home_id).scalar()
        ats_id = session.query(Team_season.team_season_id).filter(Team_season.team_id==away_id).scalar()
    seas_id = match_data['event']['season']['id']
    tourn_id = match_data['event']['tournament']['id']
    with session_scope() as session:
        st_id = session.query(Season_tournament.season_tourn_id).filter(Season_tournament.season_id==seas_id,
                                                                    Season_tournament.tournament_id==tourn_id).scalar()
    matches_dic = {'match_id': match_data['event']['id'],
                     'match_name': match_data['event']['name'],
                     'season_tourn_id': st_id,
                     'home_team_season_id': hts_id,
                     'away_team_season_id': ats_id,
                     'start_hour': match_data['event']['startTime'],
                     'match_date': match_data['event']['formatedStartDate'],
                     'stadium': match_data['event']['venue']['stadium']['name'],
                     'country': match_data['event']['venue']['country']['name']}
    return matches_dic

def fill_stat_list(match_data, period, what):
    listfill = []
    for groups in match_data["statistics"]["periods"][period]["groups"]:
        for items in groups["statisticsItems"]:
            listfill.append(items[what])
    return listfill

def create_match_stats(match_data):
    home_form = ''
    away_form = ''
    if match_data['teamsForm'] is not None:
        for let1 in match_data['teamsForm']['homeTeam']['form']:
            home_form += str(let1)
        for let2 in match_data['teamsForm']['awayTeam']['form']:
            away_form += str(let2)
    else:
        home_form = None
        away_form = None
    home_pid = match_data['event']['bestHomeTeamPlayer']['player']['id']
    away_pid = match_data['event']['bestAwayTeamPlayer']['player']['id']
    with session_scope() as session:
        hbpid = session.query(Player_team_season.player_team_season_id)\
            .filter(Player_team_season.player_id==home_pid, Player_team_season.is_active==1).scalar()
        abpid = session.query(Player_team_season.player_team_season_id)\
            .filter(Player_team_season.player_id==away_pid, Player_team_season.is_active==1).scalar()
    ms_dic = {'match_id': match_data['event']['id'],
                'home_score': match_data['event']['homeScore']['current'],
                'away_score': match_data['event']['awayScore']['current'],
                'home_best_player_id': hbpid,
                'away_best_player_id': abpid,
                'home_formation': home_form,
                'away_formation': away_form}
    tot_names = fill_stat_list(match_data, 0, 'name')
    first_names = fill_stat_list(match_data, 1, 'name')    
    scnd_names = fill_stat_list(match_data, 2, 'name')
    away_1st_names = ['away_1st_' +  f'{item}'.replace(' ','_').lower() for item in first_names]
    away_1st_values = fill_stat_list(match_data, 1, 'away')
    away_2nd_names = ['away_2nd_' + f'{item}'.replace(' ','_').lower() for item in scnd_names]    
    away_2nd_values = fill_stat_list(match_data, 2, 'away')
    away_tot_names = ['away_tot_' + f'{item}'.replace(' ','_').lower() for item in tot_names]
    away_tot_values = fill_stat_list(match_data, 0, 'away')
    home_1st_names = ['home_1st_' +  f'{item}'.replace(' ','_').lower() for item in first_names]
    home_1st_values = fill_stat_list(match_data, 1, 'home')
    home_2nd_names = ['home_2nd_' + f'{item}'.replace(' ','_').lower() for item in scnd_names]    
    home_2nd_values = fill_stat_list(match_data, 2, 'home')
    home_tot_names = ['home_tot_' + f'{item}'.replace(' ','_').lower() for item in tot_names]
    home_tot_values = fill_stat_list(match_data, 0, 'home')
    names = away_1st_names+away_2nd_names+away_tot_names+home_1st_names+home_2nd_names+home_tot_names
    values = away_1st_values+away_2nd_values+away_tot_values+home_1st_values+home_2nd_values+home_tot_values
    
    for val in range(len(values)):
        for char in BAD_CHARS:
            values[val] = str(values[val]).replace(char, '')
            if len(values[val]) > 3:
                values[val] = str(values[val])[0:3]
        values[val] = int(values[val])
                
    nv = dict(zip(names, values))
    ms_dic.update(nv)
    return ms_dic

def create_player_match_stats(match_data, players_data):    
    names = []
    
    for player in players_data['players']:
        for group in player['groups'].keys():
            if player['groups'][group] is not None:
                for key in player['groups'][group]['items'].keys():
                    if key not in names and key != 'notes':
                        names.append(key)
  
    pms_list = []
    match_id = match_data['event']['id']
  
    for player in players_data['players']:
        with session_scope() as session:
            pts_id = session.query(Player_team_season.player_team_season_id)\
                .filter(Player_team_season.player_id==player['player']['id'], Player_team_season.is_active==1).scalar()
        stats = [pts_id, match_id] + [None] * len(names)
        stat_val = {}
        for group in player['groups'].keys():
            if player['groups'][group] is not None:
                for key in player['groups'][group]['items'].keys():
                    for nom in range(len(names)):
                        if key == names[nom]:
                            stats[nom+2] = player['groups'][group]['items'][key]['value']
        stat_val = dict(zip(PLAYER_MATCH_STATS_COLS, stats))
        for val in stat_val.keys():
            if val not in ['player_team_season_id', 'match_id']:
                for char in BAD_CHARS:
                    if stat_val[val] is not None:
                        stat_val[val] = str(stat_val[val]).replace(char, '')
                if stat_val[val] is not None:
                    if len(stat_val[val]) > 3:
                        stat_val[val] = str(stat_val[val])[0:3]
                    if stat_val[val] == '':
                        stat_val[val] = 0
                    if val not in ['position', 'rating']:
                        stat_val[val] = int(stat_val[val])
                    if val == 'rating':
                        stat_val[val] = float(stat_val[val])
        pms_list.append(stat_val)       
    return pms_list

def check_insert(attr_num, insertion, table, table_column1, attribute1, table_column2=None, attribute2=None):
    with session_scope() as session:
        if attr_num == 1:
            ids_onDb = session.query(table_column1).all()
            ids_onDb = [ids[0] for ids in ids_onDb]
            if isinstance(insertion, list):
                new_list = []
                for item in insertion:
                    if item[attribute1] not in ids_onDb:
                        new_list.append(item)
                session.bulk_insert_mappings(table, new_list)
            elif isinstance(insertion, dict):
                if insertion[attribute1] not in ids_onDb:
                    instance = table(**insertion)
                    session.add(instance)
        elif attr_num == 2:
            if isinstance(insertion, list):
                new_list = []
                for item in insertion:
                    ids_onDb = session.query(table_column1, table_column2).filter(table_column1==item[attribute1],
                                                                                  table_column2==item[attribute2]).first()
                    if not ids_onDb:
                        new_list.append(item)
                session.bulk_insert_mappings(table, new_list)
            elif isinstance(insertion, dict):
                ids_onDb = session.query(table_column1, table_column2).filter(table_column1==insertion[attribute1],
                                                                              table_column2==insertion[attribute2]).first()
                if not ids_onDb:
                    instance = table(**insertion)
                    session.add(instance)
    return print(f'{table} complete')  

def set_inactive_player():
    with session_scope() as session:
        replica = session.query(Player_team_season.player_id).filter(Player_team_season.is_active==1).group_by(Player_team_season.player_id)\
                        .having(func.count(Player_team_season.player_id) > 1).all()
        if len(replica) != 0:
            for player in range(len(replica)):
                rep_pl = session.query(Player_team_season.player_team_season_id).filter(Player_team_season.player_id==replica[player][0]).all()
                session.query(Player_team_season).filter(Player_team_season.player_team_season_id==rep_pl[0][0])\
                    .update({'is_active':0}, synchronize_session=False)
    return
          
def fetch_match_players_data(match_list):
    problematic_matches = []
    for matchid in match_list:
        print(matchid)
        try:
            match_url = f'{EVENT_URL}' + f'{matchid}' + f'{MATCH_JSON_URL}'
            players_url = f'{EVENT_URL}' + f'{matchid}' + f'{PLAYERS_JSON_URL}'
            match_data = fetch_match_data(match_url)
            players_data = fetch_players_data(players_url)
            players_list = extract_player(players_data)
            check_insert(1, players_list, Player, Player.player_id, 'player_id')
            season_dict = extract_season(match_data)
            check_insert(1, season_dict, Season, Season.season_id, 'season_id')
            tournament_dict = extract_tournament(match_data)
            check_insert(1, tournament_dict, Tournament, Tournament.tournament_id, 'tournament_id')
            team_list = extract_team(match_data)
            check_insert(1, team_list, Team, Team.team_id, 'team_id')
            st_dict = create_season_tournament(match_data)
            check_insert(2, st_dict, Season_tournament, Season_tournament.season_id, 'season_id',
                         Season_tournament.tournament_id, 'tournament_id')
            ts_list = create_team_season(match_data)
            check_insert(2, ts_list, Team_season, Team_season.team_id, 'team_id',
                         Team_season.season_id, 'season_id')
            pts_list = create_player_team_season(match_data, players_data)
            check_insert(2, pts_list, Player_team_season, Player_team_season.player_id, 'player_id',
                         Player_team_season.team_season_id, 'team_season_id')
            set_inactive_player()
            matches_dict = create_matches(match_data)
            check_insert(1, matches_dict,Match, Match.match_id, 'match_id')
            ms_dict = create_match_stats(match_data)
            check_insert(1, ms_dict, Match_stats, Match_stats.match_id, 'match_id')
            pms_list = create_player_match_stats(match_data, players_data)
            check_insert(2, pms_list, Player_match_stats, Player_match_stats.player_team_season_id,
                         'player_team_season_id', Player_match_stats.match_id, 'match_id')
        except KeyError:
            print(f'Key error in match {matchid}')
            problematic_matches.append(matchid)
        finally:
            time.sleep(1)
    return  print(problematic_matches)

if __name__ == '__main__':
    engine = create_engine('mysql://alex:a1234567!@localhost/fantasy_football?charset=utf8mb4',
                           echo = True)
    Base = automap_base()
    Base.prepare(engine, reflect = True)
    Player = Base.classes.player
    Team = Base.classes.team
    Season = Base.classes.season
    Tournament = Base.classes.tournament
    Team_season = Base.classes.team_season
    Season_tournament = Base.classes.season_tournament
    Player_team_season = Base.classes.player_team_season
    Match = Base.classes.matches
    Match_stats = Base.classes.match_stats
    Player_match_stats = Base.classes.player_match_stats
    Session = sessionmaker(bind=engine)
    match_list = fetch_season_data(JSON_SEASON_URL)
    fetch_match_players_data(match_list)
    