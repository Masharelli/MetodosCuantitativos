import json
import random as rnd

#Path to read and write data, working directory.
WORKING_PATH  = 'D:\\7mo semestre\\Metodos cuantitativos\\MetodosCuantitativos\\proyecto\\'
#Filename of the original data file.
FILE_NAME = 'data.json'
#Complete path of the original data file
PATH = FILE_NAME

#Set the data with buffs and debuffs according
#to the region of the team
def settingBuffs(data):
    buffs={"LPL":1,"LEC":0.95,"LCK":0.95,"LCS":0.90,"PCS":0.85,"LCL":0.55}
    buffed_data=data
    for team in data:
        mult = buffs[data[team]["region"]]
        for stat in data[team]:
            if stat=="region" or stat=="goldpm":
                continue
            elif stat=="members":
                for member in data[team][stat]:
                    new_stat = round(data[team][stat][member]["killparticipation"]*mult,2)
                    buffed_data[team][stat][member]["killparticipation"]=new_stat
            else:
                new_stat = round(data[team][stat]*mult,2)
                buffed_data[team][stat]=new_stat

    #Write the new buffed data on a json file
    with open(WORKING_PATH+'buffed_data.json','w') as outfile:
        json_object= json.dumps(buffed_data, indent=4)
        outfile.write(json_object)
        print("Buffed data file created succesfully")
    
#Returns the dictionary load from a json file.
def loadData(path):
    with open(path,'r') as f:
	    data = json.load(f)
    return data

#Receives 2 porcentages and returns which is the winner.
#The porcentages can sum over 100%, this function translate
#them to a 100% basis. This method is a Markov chain of only 2
#posible outcomes. Returns 1 or 2, depending of the winner
def markov(teamA_ptge, teamB_ptge):
    sum_ptges=teamA_ptge+teamB_ptge
    teamA_ptge/=sum_ptges
    teamB_ptge/=sum_ptges
    w=[teamA_ptge,teamB_ptge]
    return rnd.choices([1,2],weights=tuple(w), k=1)[0]

#Testing the model
def testMatch(teamA,teamB,data):
    value_ingame={
        "winrate": 25,
        "firstblood": 15,
        "firsttower": 7,
        "1dragon": 3,
        "2dragon": 5,
        "3dragon": 10,
        "4dragon": 20,
        "elderdragon": 25,
        "heraldpg": 7,
        "nashorpg": 22,
        "top": 3,
        "jg": 5,
        "mid": 4,
        "adc": 4,
        "supp": 3
    }

    teamA_cont=0
    teamB_cont=0

    #winrate
    add = data[teamA["name"]]["winrate"]+data[teamB["name"]]["winrate"]
    teamA_cont+=(data[teamA["name"]]["winrate"]/add)*value_ingame["winrate"]
    teamB_cont+=(data[teamB["name"]]["winrate"]/add)*value_ingame["winrate"]

    for stat in value_ingame:
        if stat!="winrate":
            if teamA[stat]==True:
                teamA_cont+=value_ingame[stat]
            elif teamB[stat]==True:
                teamB_cont+=value_ingame[stat]
    
    sum_results=teamA_cont+teamB_cont
    teamA_ptge=teamA_cont/sum_results
    teamB_ptge=teamB_cont/sum_results
    if markov(teamA_ptge,teamB_ptge)==1:
        winner=teamA["name"]
    else:
        winner=teamB["name"]

    print("Testing: \n"+winner+" "+str(teamA_ptge)+" " +str(teamB_ptge))


#Simulates a match between 2 teams, considering all the statistics
#and solving each of them with markov chains. Receives 2 team
#names and the data. Returns a list with the name of the winner and the
#porcentages in order (teamA and then teamB).
def playMatch(teamA, teamB,data):

    #Here we have the values of each stat in game according
    #to our own model of probabilities. 
    value_ingame={
        "winrate": 25,
        "firstblood": 15,
        "firsttower": 7,
        "1dragon": 3,
        "2dragon": 5,
        "3dragon": 10,
        "4dragon": 20,
        "elderdragon": 25,
        "heraldpg": 7,
        "nashorpg": 22,
        "top": 3,
        "jg": 5,
        "mid": 4,
        "adc": 4,
        "supp": 3
    }

    #Here we will sum the stats that each team won
    teamA_sum=0
    teamB_sum=0

    for stat in data[teamA]:
        if stat=="region" or stat=="goldpm" or stat=="towerratio":
                #Irrelevant information in the database
                continue
        elif stat=="members":
            #Members stats
            for member in data[teamA][stat]:
                for member2 in data[teamB][stat]:
                    if data[teamA][stat][member]["position"]==data[teamB][stat][member2]["position"]:
                        if markov(data[teamA][stat][member]["killparticipation"],data[teamB][stat][member2]["killparticipation"])==1:
                            teamA_sum+=value_ingame[data[teamA][stat][member]["position"]]
                        else:
                            teamB_sum+=value_ingame[data[teamB][stat][member2]["position"]]
        elif stat=="dragonpg":
            teamA_dragons=0
            teamB_dragons=0
            #Normal dragons
            while teamA_dragons<4 and teamB_dragons<4:
                if markov(data[teamA][stat],data[teamB][stat])==1:
                    teamA_dragons+=1
                    teamA_sum+=value_ingame[str(teamA_dragons)+"dragon"]
                else:
                    teamB_dragons+=1
                    teamB_sum+=value_ingame[str(teamB_dragons)+"dragon"]
            
            #Elder dragon
            if markov(data[teamA][stat],data[teamB][stat])==1:
                teamA_sum+=value_ingame["elderdragon"]
            else:
                teamB_sum+=value_ingame["elderdragon"]
        elif stat=="winrate":
            teamA_cont=0
            teamB_cont=0
            add = data[teamA][stat]+data[teamB][stat]
            teamA_cont+=(data[teamA][stat]/add)*value_ingame[stat]
            teamB_cont+=(data[teamB][stat]/add)*value_ingame[stat]
        else:
            if markov(data[teamA][stat],data[teamB][stat])==1:
                teamA_sum+=value_ingame[stat]
            else:
                teamB_sum+=value_ingame[stat]
        #print(teamA_sum)
        #print(teamB_sum)

    #Markov chain with final porcentages. Determines the winner
    sum_results=teamA_sum+teamB_sum
    teamA_ptge=teamA_sum/sum_results
    teamB_ptge=teamB_sum/sum_results
    if markov(teamA_ptge,teamB_ptge)==1:
        winner=teamA
    else:
        winner=teamB

    return [winner,teamA_ptge, teamB_ptge]

#Receives 8 teams participating on the bracket and the
# data. Returns a winner depending on the Markov chains
#representing each match
def getWinner(teams,data):
    result={}
    winners=[]
    labels=["Quarterfinals","Semifinals","Final"]
    cont_label=0
    match_cont=0
    while len(teams)>1:
        print(labels[cont_label]+"\n--------------------\n")
        cont_label+=1
        for index in range(0,len(teams),2):
            match_cont+=1
            teamA_wins=0
            teamB_wins=0
            teamA_ptge=0
            teamB_ptge=0

            #Store all the information on a dictionary to send it to the frontend
            result["serie"+str(match_cont)]={"teamA":teams[index]}
            result["serie"+str(match_cont)]["teamB"]=teams[index+1]

            #Bo5
            while teamA_wins<3 and teamB_wins<3:
                print("Playing "+teams[index]+" vs "+teams[index+1])
                match_results=playMatch(teams[index],teams[index+1],data)
                print("Winner: "+match_results[0]+"\nPercentages: ")
                print(teams[index]+": "+str(round(match_results[1]*100,2))+"%")
                print(teams[index+1]+": "+str(round(match_results[2]*100,2))+"%")
                teamA_ptge+=round(match_results[1]*100,2)
                teamB_ptge+=round(match_results[2]*100,2)
                print("------------------------------\n")
                if match_results[0]==teams[index]:
                    teamA_wins+=1
                elif match_results[0]==teams[index+1]:
                    teamB_wins+=1
                print(teamB_wins+teamA_wins)
                if teamA_wins+teamB_wins==1:
                    result["serie"+str(match_cont)]["matches"]={"match"+str(teamA_wins+teamB_wins):{"winner":match_results[0]}}
                else:
                    result["serie"+str(match_cont)]["matches"]["match"+str(teamA_wins+teamB_wins)]={"winner":match_results[0]}
                result["serie"+str(match_cont)]["matches"]["match"+str(teamA_wins+teamB_wins)]["teamA_ptge"]=match_results[1]
                result["serie"+str(match_cont)]["matches"]["match"+str(teamA_wins+teamB_wins)]["teamB_ptge"]=match_results[2]
            if teamA_wins>=3:
                winner=teams[index]
            elif teamB_wins>=3:
                winner=teams[index+1]
            winners.append(winner)
            teamA_ptge/=(teamA_wins+teamB_wins)
            teamB_ptge/=(teamA_wins+teamB_wins)

            result["serie"+str(match_cont)]["winner"]=winner
            result["serie"+str(match_cont)]["teamA_ptge"]=teamA_ptge
            result["serie"+str(match_cont)]["teamB_ptge"]=teamB_ptge
            result["serie"+str(match_cont)]["teamA_score"]=teamA_wins
            result["serie"+str(match_cont)]["teamB_score"]=teamB_wins
        teams=winners
        winners=[]
    print("CAMPEON: "+teams[0])
    #print(result)
    return result
    


'''data = loadData(PATH)
settingBuffs(data)
data = loadData(WORKING_PATH+"buffed_data.json")
#Teams that will be received from the user
teams=["Damwon","DragonX","Gen G","G2 Esports","Top Esports","Fnatic","Suning Gaming","JD Gaming"]
getWinner(teams,data)'''