import requests
from datetime import datetime
from requests.structures import CaseInsensitiveDict
import sys
from math import floor
headers = CaseInsensitiveDict()
keyyyy = "mxUMAvCXOvVNReOejG6LdToqTX8FvKb4ftsD7Lo2S6ACLTJ1PoEhZm0Sse7HZUK0\t"
headers["accept"] = "application/json"
headers["X-TBA-Auth-Key"] = keyyyy
class Team():
    def __init__(self, name):
        self.name = name
        self.matchScores = []
        self.rankingScore = 0
        self.avgMatch = 0
        self.totalRPs = 0
    def matchResults(self, score, rp):
        self.matchScores.append(score)
        self.totalRPs+=rp
        self.rankingScore = self.totalRPs/len(self.matchScores)
        self.avgMatch = sum(self.matchScores)/len(self.matchScores)
    def __lt__(self, other):
        if self.rankingScore == other.rankingScore:
            return self.avgMatch < other.avgMatch
        else:
            return self.rankingScore < other.rankingScore
    def __repr__(self):
        return self.name

def getInput(message, type):
    cast = getattr(__builtins__, type)
    while(1):
        try:
            output = input(message)
            return cast(output) 
        except ValueError:
            print(f"Input must be of type {type}, Please try again!")
if __name__ == "__main__":
    matchNum = getInput("Please Enter Match Number to view rankings at: ", "int")
    eventKey = input("Please Input event key:")
    year = str(datetime.now().year)
    event = year + eventKey.lower()
    matchURL = "https://www.thebluealliance.com/api/v3/event/{event}/matches".format(
    event=event)
    teamURl = "https://www.thebluealliance.com/api/v3/event/{event}/teams/keys".format(
    event=event)
    try:
        resp = requests.get(teamURl, headers=headers)
    except requests.exceptions.ConnectionError:
        print("Server Can't Be reached")
        sys.exit()
    if resp.status_code == 404:
        print(resp.text())
        sys.exit()
    matchResp = requests.get(matchURL, headers=headers) 
    matchList = matchResp.json()
    matchList = [x for x in matchList if x['comp_level'] in ['qm']]
    matchList=sorted(matchList, key=lambda x:x['actual_time'])[:matchNum]
    print(f"Rankings After Match {matchNum} at Event {event}")
    teamDict = {}   
    for team in resp.json():
        teamDict[team]=(Team(team))
    for match in matchList:
      for color in ('red', 'blue'):
        teams = match["alliances"][color]["team_keys"]
        stats = match["score_breakdown"][color]
        for team in teams:
         if team in match['alliances'][color]['dq_team_keys']:
             teamDict[team].matchResults(0,0)
         else:
             teamDict[team].matchResults(stats['totalPoints'], stats['rp'])

    for rank, team in enumerate(sorted(teamDict.values())[::-1]):
        print(f'{rank+1}. {str(team)[3:]} with a ranking score of {str(team.rankingScore)[:3]} and an average match of {floor(team.avgMatch)}')
