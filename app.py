
from boggle import Boggle
from flask import Flask, request, render_template, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "42"

@app.route('/')
def home_page():
    return(render_template('home.html'))

@app.route('/boggle/', methods=['POST'])
def boggle_page():
  boggle_game = Boggle()
  boggle_game.board = boggle_game.make_board()
  # set up session & store board
  if (not session.get('boggle_game')):
     session['boggle_game'] = {}
  game_copy = session['boggle_game']
  game_copy['board']= boggle_game.board
  session['boggle_game'] = game_copy
  return(render_template('boggle.html', board=boggle_game.board))

@app.route('/boggle/check-word/', methods=['GET'])
def check_word():
   """ call server to see if word is valid & can be found on board """
   boggle_game = Boggle()
   boggle_game.board = session['boggle_game']['board']
   word = request.args.get('word').upper()
   # print(boggle_game.board)
   check_valid = boggle_game.check_valid_word(boggle_game.board, word)
   return(check_valid)

@app.route('/boggle/get-game-stats/', methods=['GET'])
def get_game_stats():
   """ call server to see boggle game history stats """
   high_score = session['boggle_game'].get('high_score',0)
   num_games = session['boggle_game'].get('num_games',0)
   return({'high_score': high_score, 'num_games': num_games})

@app.route('/boggle/post-game-stats/', methods=['POST'])
def post_game_stats():
   """ called to post game score & augment stats """
   score = request.json['score']
   high_score = session['boggle_game'].get('high_score',0)
   if (score > high_score):
      # print('new high score: ', score)
      session['boggle_game']['high_score'] = score
   num_games = session['boggle_game'].get('num_games', 0)
   num_games += 1
   game_copy = session['boggle_game']
   game_copy['num_games'] = num_games
   session['boggle_game'] = game_copy
   return('ok')