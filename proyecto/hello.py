from flask import Flask
from flask import render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
   return render_template(
      "llaves.html",
      data =[{'team': 'Top esports'}, {'team': 'G2 Esports'}, {'team': 'Damwon'}, {'team': 'Suning'}, {'team': 'DRX'}, 
      {'team': 'JD Gaming'}, {'team': 'Fnatic'}, {'team': 'Gen G'}, {'team': 'Team Liquid'}, {'team': 'PSG Talon'},
      {'team': 'LGD Gaming'}, {'team': 'FlyQuest'}, {'team': 'Machi Esport'}, {'team': 'Rogue'}, {'team': 'TSM'},
      {'team': 'Unicorns Of Love'}, ])

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
   team1 = request.form.get('team1')
   team2 = request.form.get('team2')
   team3 = request.form.get('team3')
   team4 = request.form.get('team4')
   team5 = request.form.get('team5')
   team6 = request.form.get('team6')
   team7 = request.form.get('team7')
   team8 = request.form.get('team8')
   arrayTeam = [team1,team2,team3,team4,team5,team6,team7,team8]
   return render_template('resultado.html',  team1 = team1, team2 = team2, team3 = team3, team4 = team4, team5 = team5, 
   team6 = team6, team7 = team7, team8 = team8 ) 

if __name__=='__main__':
    app.run(debug=True)