
from app import app
from unittest import TestCase
from flask import session
from boggle import boggle_test_board

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
            self.assertEqual(res.status_code,200)
            self.assertIn('Time Remaining', html)
            self.assertEqual(len(session['boggle_game']['board']),5)
            with client.session_transaction() as change_session:
                change_session['boggle_game'] = {'board': boggle_test_board}
                change_session.modified = True
            print(boggle_test_board)
            print(session['boggle_game']['board'])
            self.assertEqual(len(session['boggle_game']['board']),5)
            self.assertEqual(session['boggle_game']['board'][0][1],'H')


#            res = client.post('/boggle/', data={'color': 'blue'})
