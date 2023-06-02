from flask import Flask, render_template
from flask_frozen import Freezer
import pandas as pd
import random as rd

app = Flask(__name__)


@app.route('/')
def index():
    energy_data = [
        {'year': 2010, 'energy': 1000},
        {'year': 2011, 'energy': 1200},
        {'year': 2012, 'energy': 1350},
        {'year': 2013, 'energy': 1100},
        {'year': 2014, 'energy': 1250},
        # Add more data points as needed
    ]

    funFact_df = pd.read_csv('static/FunFactz.csv')
    funFact_dict = funFact_df.to_dict()
    x = rd.randint(1, 5)
    random_number = rd.randint(0, 57)
    random_fact = ''

    if x == 1:
        random_fact = funFact_dict['Fact1'][random_number]
    elif x == 2:
        random_fact = funFact_dict['Fact2'][random_number]
    elif x == 3:
        random_fact = funFact_dict['Fact3'][random_number]
    elif x == 4:
        random_fact = funFact_dict['Fact4'][random_number]
    elif x == 5:
        random_fact = funFact_dict['Fact5'][random_number]

    years = [data['year'] for data in energy_data]
    energy_values = [data['energy'] for data in energy_data]

    return render_template('index.html', years=years, energy_values=energy_values, random_fact=random_fact)


@app.route('/counties')
def count_yolo():
    counties_df = pd.read_csv('ImageCSV.csv')
    counties = counties_df.to_dict(orient='records')

    return render_template('counties.html', counties=counties)



@app.route('/counties/<county_name>')
def county_page(county_name):
    counties_df = pd.read_csv('ImageCSV.csv')
    county_data = counties_df.loc[counties_df['County'] == county_name].to_dict(orient='records')[0]

    # Load the CSV file
    counties_data_df = pd.read_csv('output.csv', index_col=0)

    # Initialize empty lists
    energies = []
    populations = []

    # Iterate through DataFrame rows
    for index, row in counties_data_df.iterrows():
        for col in row:
            # Check if the cell is not empty or NaN
            if pd.notnull(col):
                # Convert string to tuple
                population, energy = eval(col)
                energies.append(energy)
                populations.append(population)

    filtered_rows = counties_df[counties_df['County'] == county_name]

    county_index = filtered_rows.index.tolist()[0]

    energy_data = []
    population_data = []

    for i in range(county_index * 61, county_index * 61 + 61):
        energy_data.append(energies[i])
        population_data.append(populations[i])


    return render_template('county.html', county=county_data, energy_data=energy_data, populations_data=population_data)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/machinelearning')
def MachineLearning():
    return render_template('MachineLearning.html')

if __name__ == '__main__':
    freezer.freeze()