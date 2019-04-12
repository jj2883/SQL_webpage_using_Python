#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import psycopg2
from psycopg2.extensions import AsIs
from sqlalchemy_utils import database_exists, create_database
from flask.views import MethodView

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response



tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
#DATABASEURI = "postgresql://jad2267:jj2883@34.73.21.127/proj1part2"
DATABASEURI = "postgresql://jj2883:2360@34.73.21.127/proj1part2"



engine = create_engine(DATABASEURI,isolation_level="AUTOCOMMIT")

engine.execute(open("tables.sql", "r").read())
engine.execute(open("data.sql", "r").read())



@app.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):

  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():

  names = ['Team','Player', 'Game', 'Statline']
  context = dict(entities = names)


 
  return render_template("index.html", **context)



@app.errorhandler(500)
def page_not_found(e):
    return render_template('505.html'), 500

class List_Search(MethodView):


    def get(self, name):
        if request.method != 'POST':

            # Get table entries
            query = "SELECT * FROM %(table)s;"
            cursor = g.conn.execute(query, {"table": AsIs(name)})
          

            table = []
            for cells in cursor:
                table.append(cells)

            fields = cursor.keys()
            fields = [(f,) for f in fields]
           

            cursor.close()
           

            table = sorted(table)
            context = dict(t_name=str(name), table=table, fields=fields)
            if '_' not in name:
                return render_template("entities.html", **context)
            else:
                return render_template("relations.html", **context)

    def post(self, name):
        # print name
        search = request.form['search']
#        search_ph = search + '%%'
        search_ph = search 
        name = name.lower()
        # print search
        if name == 'player':
        	

#            cursor = g.conn.execute(query)
            if search == 'statline':

                query = "SELECT player_first_name, player_last_name, game_id, minutes_played, field_goals,field_goals_attempted,three_pointers, three_pointers_attempted,free_throws, free_throws_attempted,offensive_rebounds,defensive_rebounds,assists,steals,blocks,turnovers,personal_fouls,points FROM player p, (select * from statline) s where p.player_id = s.player_id;"
                cursor = g.conn.execute(query, (search_ph,))


            elif search == 'team':

                query = "SELECT p.player_first_name, p.player_last_name, t.team_name, t.region FROM player p, team t,  (select * from play_for_) pf where pf.player_id = p.player_id AND pf.team_id=t.team_id;"

                cursor = g.conn.execute(query, (search_ph,))

            else:

            	search=search.capitalize()
            	search="\'"+search+"\'"

            	query = "SELECT * FROM player p where p.player_last_name = {};".format(search)

            	cursor = g.conn.execute(query, (search_ph,))


        elif name == 'team':
        	

            if search == 'coach':

                query = "SELECT team_name, coach_first_name, coach_last_name  FROM coach c, team t,(select * from coaches_ ) co where co.team_id = t.team_id and co.coach_id=c.coach_id;"
                cursor = g.conn.execute(query, (search_ph,))


            elif search == 'player':

                query = "SELECT t.team_name, p.player_first_name, p.player_last_name FROM player p, team t,  (select * from play_for_) pf where pf.player_id = p.player_id AND pf.team_id=t.team_id;"

                cursor = g.conn.execute(query, (search_ph,))

            elif search == 'game':

            	query = "SELECT game_id, home_team_name, points_home_team, away_team_name, points_away_team FROM game g, (select * from play_) pl where pl.game_id = g.game_id;"

            	cursor = g.conn.execute(query, (search_ph,))

            else:
            	search=search.capitalize()
            	search="\'"+search+"\'"

            	query = "SELECT home_team_name, points_home_team, away_team_name, points_away_team FROM game g, (select * from play_) pl where g.game_id = pl.game_id and (pl.away_team_name={0} or pl.home_team_name={1});".format(search,search)

            	cursor = g.conn.execute(query, (search_ph,))



        elif name == 'statline':


            if search == 'player':

                query = "SELECT player_first_name, player_last_name, game_id, minutes_played, field_goals,field_goals_attempted,three_pointers, three_pointers_attempted,free_throws, free_throws_attempted,offensive_rebounds,defensive_rebounds,assists,steals,blocks,turnovers,personal_fouls,points FROM player p, (select * from statline) s where p.player_id = s.player_id;"
                cursor = g.conn.execute(query, (search_ph,))
            
            else:


            	query = "SELECT player_first_name, player_last_name, game_id, {} FROM player p, (select * from statline) s where p.player_id = s.player_id;".format(search)

            	cursor = g.conn.execute(query, (search_ph,))


        elif name == 'game':
        	

            if search == 'player':

##            	query = "SELECT p.player_first_name, p.player_last_name, s.game_id FROM player p, game g, (select * from statline) s where s.player_id = p.player_id and s.game_id=g.game_id;"
            	query = "SELECT p.player_first_name, p.player_last_name, s.game_id FROM player p, game g, (select * from statline) s where s.player_id = p.player_id and s.game_id=g.game_id;"

            	cursor = g.conn.execute(query, (search_ph,))

            elif search == 'team':

            	query = "SELECT home_team_name, points_home_team, away_team_name, points_away_team FROM game g, (select * from play_) pl where pl.game_id = g.game_id;"

            	cursor = g.conn.execute(query, (search_ph,))

            else:
            	search=search.capitalize()
            	search="\'"+search+"\'"

            	query = "SELECT game_id, home_team_name, points_home_team, away_team_name, points_away_team FROM game g, (select * from play_) pl where pl.game_id = g.game_id and (pl.away_team_name={0} or pl.home_team_name={1});".format(search,search)

            	cursor = g.conn.execute(query, (search_ph,))



        # Get fields
        _fields = cursor.keys()
     
        # print _fields

        fields = []
        for x in _fields:
            if x not in fields:
                fields.append(x)
        # print fields
        output = []
        for result in cursor:
            row = ()
            for f in fields:
                # print result[f]
                row += (result[f],)
            output.append(row)
        output = sorted(output)
        # Format fields correctly, but only after to prevent type issues
        fields = [(f,) for f in fields]
        cursor.close()
        context = dict(search=str(search), t_name=str(name).title(), table=output, fields=fields)
        return render_template("search.html", **context)


ListSearch_View = List_Search.as_view('List_Table')
# Can always use defaults={'search': None} as a arg if need be
app.add_url_rule('/<name>', view_func=ListSearch_View)
app.add_url_rule('/<name>/search', view_func=ListSearch_View)


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
      """
      This function handles command line parameters.
      Run the server using
          python server.py
      Show the help text using
          python server.py --help
      """

      HOST, PORT = host, port
      print "running on %s:%d" % (HOST, PORT)
      app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()