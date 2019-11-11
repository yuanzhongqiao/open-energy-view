import os
import json
from datetime import datetime
from flask import Flask, render_template, request
from itertools import cycle
import sqlite3

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=f'{PROJECT_PATH}/data/energy_history.db',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route("/test-gui")
    def test_gui():
        return render_template('test-gui.html')

    @app.route("/test-espi-chart", methods=['GET'])
    def chart():
        start = request.args.get('start', default=0)
        end = request.args.get('end', default=9571569200)
        conn = sqlite3.connect(
            f'{PROJECT_PATH}/test/data/energy_history_test.db')

        cur = conn.cursor()
        cur.execute("""
                    SELECT watt_hours, start
                    FROM espi
                    ORDER BY start ASC;
                    """)
        data = []
        lookup = {}
        dates = []
        i = 0
        for values, starts in cur.fetchall():
            # JS needs epoch in ms; the offset is to position the bar correctly
            starts = starts * 1000 + 1800000
            data.append({'x': starts, 'y': values})
            dates.append(starts)
            lookup[starts] = i
            i += 1

        data = str(json.dumps(data))
        lookup = str(json.dumps(lookup))

        return render_template('date-chart.html', data=data, lookup=lookup, dates=dates)

    @app.route("/test-partitions-chart", methods=['GET'])
    def partitions_chart():
        conn = sqlite3.connect(
            f'{PROJECT_PATH}/test/data/energy_history_test.db')

        cur = conn.cursor()

        cur.execute("SELECT n_parts FROM info WHERE id=0;")
        n_parts = cur.fetchone()[0]

        part_names = []
        for i in range(1, n_parts + 1):
            cur.execute(f"""
                        SELECT part_{i}_name
                        FROM info;
                        """)
            part_names.append(cur.fetchall()[0][0])

        part_1_color = '#800080'
        part_2_color = '#add8e6'
        part_3_color = '#0000A0'

        colors_tuple = (part_1_color, part_2_color, part_3_color)

        part_value_lists = [None] * 5
        part_date_lists = [None] * 5

        for i in range(0, n_parts):
            cur.execute(f"""
                        SELECT part_{i+1}_avg, date
                        FROM partitions
                        WHERE part_{i+1}_avg != 'None';
                        """)
            part_value, part_date = zip(*cur.fetchall())
            part_value_lists[i] = (list(part_value))
            part_date_lists[i] = (list(part_date))

        part_values = list(zip(
            part_value_lists[0],
            part_value_lists[1],
            part_value_lists[2]))

        part_dates = list(zip(
            part_date_lists[0],
            part_date_lists[1],
            part_date_lists[2]))

        values = [v for i in part_values for v in i]
        labels = [l for i in part_dates for l in i]

        colors = []
        color_picker = cycle(colors_tuple)
        for foo in values:
            colors.append(next(color_picker))

        return render_template('partitions-chart.html', values=values, labels=labels, colors=colors)

    @app.route('/test-espi-list')
    def long_list():
        conn = sqlite3.connect(
            f'{PROJECT_PATH}/test/data/energy_history_test.db')
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("select * from espi")

        rows = cur.fetchall()
        return render_template("list.html", rows=rows)

    @app.route('/test-partitions-list')
    def long_partslist():
        conn = sqlite3.connect(
            f'{PROJECT_PATH}/test/data/energy_history_test.db')
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("select * from partitions")

        rows = cur.fetchall()
        return render_template("list-parts.html", rows=rows)
    
    @app.route('/test-info-list')
    def info_list():
        conn = sqlite3.connect(
            f'{PROJECT_PATH}/test/data/energy_history_test.db')
        conn.row_factory = sqlite3.Row

        cur = conn.cursor()
        cur.execute("select * from info")

        rows = cur.fetchall()
        return render_template("list-info.html", rows=rows)

    @app.route('/test-baseline')
    def baseline():
        conn = sqlite3.connect(
            f'{PROJECT_PATH}/test/data/energy_history_test.db')

        cur = conn.cursor()
        cur.execute("SELECT baseline, date FROM daily")

        values, labels = zip(*cur.fetchall())
        labels = [datetime.strptime(l, '%y/%m/%d').strftime('%b %d %Y') for l in labels]

        return render_template('line.html', values=values, labels=labels)

    return app
