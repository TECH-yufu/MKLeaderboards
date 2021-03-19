# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 15:16:06 2021

@author: Yucheng
"""
import os
path = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
os.chdir(path)
import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class MKLeaderboard():
    def __init__(self, category, track='none'):
        self.category = category.lower()

        if self.category == 'no-sc' or self.category == 'unrestricted':
            cup_ids = np.arange(12,20)
        
            if self.category == 'no-sc':
                api_url = 'https://www.mkleaderboards.com/api/charts/mkw_nonsc_world/{num}'
                
                
            elif self.category == 'unrestricted':
                api_url = 'https://www.mkleaderboards.com/api/charts/mkw_combined_world/{num}'
                
            
            self.mkwii_data = [requests.get(api_url.format(num=i*4+j)).json() for i in cup_ids for j in np.arange(1,5)]
            
            self.track_names = [self.mkwii_data[i]['track_name'].upper() for i in np.arange(0,32)]
            self.player_names = self.get_playerNames(self.mkwii_data, self.track_names)
            self.country_names = self.get_countryNames(self.mkwii_data, self.track_names)
        
        elif self.category == 'alt-sc':
            cup_ids = np.array([60,75])
            api_url = 'https://www.mkleaderboards.com/api/charts/mkw_altsc_world/{num}'
            
            
        
            
            self.mkwii_data = [requests.get(api_url.format(num=i)).json() for i in cup_ids]
            
            self.track_names = [self.mkwii_data[i]['track_name'].upper() for i in np.arange(0,2)]
            self.player_names = self.get_playerNames(self.mkwii_data, self.track_names)
            self.country_names = self.get_countryNames(self.mkwii_data, self.track_names)
      
            
        if track.upper() in self.track_names:
            self.track = track.upper()
        else:
            self.track = None
        
    def player_leaderboards(self):
        self.WW_tops_by_player(self.category, self.player_names)
        
    def country_leaderboards(self):
        self.WW_tops_by_country(self.category, self.country_names)
        
    def wr(self):
        if self.track == None:
            return "Please select a valid track name."
        else:
            wr_dict = {}
            for i in range(len(self.track_names)):
                wr_dict[self.track_names[i]] = self.mkwii_data[i]['data']
            
            wr = wr_dict[self.track][0]
            
            l1 = 'The world record on {track} ({cat})'.format(track=self.track, cat=self.category)
            l2 = 'is set by {player} with a time of {time}.'.format(player=wr['name'],time=wr['score_formatted'])
            l3 = 'Congratulations to {player}!'.format(player=wr['name'])  

            wr_display = self.wr_table(l1,l2,l3)

        return wr_display

    
    def get_playerNames(self, mkwii_data, track_names):
        player_names = {}        
        
        for track,i in zip(track_names, np.arange(0,32)):
            player_names[track] = [mkwii_data[i]['data'][j]['name'] for j in np.arange(0,10)]
            
        return player_names
    
    def get_countryNames(self, mkwii_data, track_names):
        country_names = {}
        
        for track,i in zip(track_names, np.arange(0,32)):
            country_names[track] = [mkwii_data[i]['data'][j]['country'] for j in np.arange(0,10)]
            
        return country_names    
    
    def get_trackNames(self):
        return self.track_names
    
    def wr_table(self, l1, l2,l3):
        len_standard = 52 + 6
        dif1 = len_standard - len(l1)
        dif2 = len_standard - len(l2)
        dif3 = len_standard - len(l3)
        
        # I know this is ugly but whatever
        dif11 = dif1//2 
        dif12 = dif1 - dif11
        dif21 = dif2//2
        dif22 = dif2 - dif21
        dif31 = dif3//2
        dif32 = dif3 - dif31
        
        header = '╔' + len_standard*'═' + '╗\n'
        space1 = '║' + len_standard*' ' + '║\n'
        l1 = '║' + dif11*' ' + l1 + dif12*' ' + '║\n'
        l2 = '║' + dif21*' ' + l2 + dif22*' ' + '║\n'
        l3 = '║' + dif31*' ' + l3 + dif32*' ' + '║\n'
        space2 = '║' + len_standard*' ' + '║\n'
        footer = '╚' + len_standard*'═' + '╝\n'
            
        table = header+space1+l1+l2+l3+space2+footer
        return table 
        
    def WW_tops_by_player(self,category, player_names):
        player_list = []
        
        for key in player_names.keys():
            player_list.extend(player_names[key])
            
        player_dict = Counter(player_list)
        WW_tops_players = sorted(player_dict, key=player_dict.get, reverse=True)
        WW_tops = [player_dict[player] for player in WW_tops_players]
        
        plt.bar(WW_tops_players[0:10],WW_tops[0:10], color='green')
        plt.ylim(0,max(WW_tops)+2)
        plt.xticks(WW_tops_players[0:10], rotation=60)
        plt.yticks(np.arange(0,max(WW_tops)+2))
        plt.xlabel('Player')
        plt.ylabel('Number of WW tops')
        plt.title('{} WW tops (by player)'.format(category))
        plt.show()

    def WW_tops_by_country(self,category, country_names):
        country_list = []
        
        for key in country_names.keys():
            country_list.extend(country_names[key])
            
        country_dict = Counter(country_list)
        WW_tops_countries = sorted(country_dict, key=country_dict.get, reverse=True)
        WW_tops_CT = [country_dict[country] for country in WW_tops_countries]
        
        plt.bar(WW_tops_countries[0:10],WW_tops_CT[0:10],color='red')
        plt.ylim(0,max(WW_tops_CT)+10)
        plt.xticks(WW_tops_countries[0:10], rotation=60)
        plt.xlabel('Country')
        plt.ylabel('Number of WW tops')
        plt.title('{} WW tops (by country)'.format(category))
        plt.show()
    


if __name__ == '__main__':
    wii = MKLeaderboard(category='alt-sc', track='grumble volcano')
    wii.player_leaderboards()
    print(wii.wr())
    
track_names = np.load("track_names.npy")