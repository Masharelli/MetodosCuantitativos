from flask import Flask
from flask import render_template, request, redirect, url_for
import project as backend
app = Flask(__name__)

#Array to store globally the teams selected
teams=[]
#Array to store the data to display on the results page
results=[]
#Data to use
data=[]
#Path to read and write data, working directory.
WORKING_PATH  = 'D:\\7mo semestre\\Metodos cuantitativos\\MetodosCuantitativos\\proyecto\\'
#Filename of the original data file.
FILE_NAME = 'data.json'
#Complete path of the original data file
PATH = FILE_NAME


@app.route('/')
def index():
   return render_template(
      "llaves.html",
      data =[{'team': 'Top Esports'}, {'team': 'G2 Esports'}, {'team': 'Damwon'}, {'team': 'Suning Gaming'}, {'team': 'DragonX'}, 
      {'team': 'JD Gaming'}, {'team': 'Fnatic'}, {'team': 'Gen G'}, {'team': 'Team Liquid'}, {'team': 'PSG Talon'},
      {'team': 'LGD Gaming'}, {'team': 'FlyQuest'}, {'team': 'Machi Esports'}, {'team': 'Rogue'}, {'team': 'TSM'},
      {'team': 'Unicorns of Love'}, ])

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
   global teams
   global data
   team1 = request.form.get('team1')
   team2 = request.form.get('team2')
   team3 = request.form.get('team3')
   team4 = request.form.get('team4')
   team5 = request.form.get('team5')
   team6 = request.form.get('team6')
   team7 = request.form.get('team7')
   team8 = request.form.get('team8')
   teams = [team1,team2,team3,team4,team5,team6,team7,team8]

   data = backend.loadData(PATH)
   backend.settingBuffs(data)
   data = backend.loadData(WORKING_PATH+"buffed_data.json")
   tournament=backend.getWinner(teams,data)

   #return render_template('resultado.html',  team1 = team1, team2 = team2, team3 = team3, team4 = team4, team5 = team5, 
   #team6 = team6, team7 = team7, team8 = team8 ) 
   return render_template('resultado.html', tournament=tournament)

if __name__=='__main__':
    app.run(debug=True)

