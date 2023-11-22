
from app import app
from unittest import TestCase
from flask import session
from boggle import boggle_test_board
import json

class BoggleTestCase(TestCase):

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code,200)
            self.assertIn('<button type="submit">Play Game</button>', html)

    def test_boggle_page(self):
        with app.test_client() as client:
            res = client.post('/boggle/')
            html = res.get_data(as_text=True)
            # print('session: ', session)
            self.assertEqual(res.status_code,200)
            self.assertIn('Time Remaining', html)
            self.assertEqual(len(session['boggle_game']['board']),5)
    
    def test_check_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                 change_session['boggle_game'] = {'board': boggle_test_board}
            res = client.get('/boggle/check-word/?word=indian')
            self.assertEqual(res.get_data(as_text=True), "ok")
            res = client.get('/boggle/check-word/?word=lamppost')
            self.assertEqual(res.get_data(as_text=True), "not-on-board")
            res = client.get('/boggle/check-word/?word=xxxyyyzzz')
            self.assertEqual(res.get_data(as_text=True), "not-word")

    def test_get_game_stats(self):
        with app.test_client() as client:
            res = client.post('/boggle/')
            res = client.get('/boggle/get-game-stats/')
            self.assertIn('high_score', res.get_data(as_text=True))
            
    def test_post_game_stats(self):
        with app.test_client() as client:
            res = client.post('/boggle/')
            res = client.post('/boggle/post-game-stats/')
