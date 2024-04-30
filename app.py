from flask import Flask, render_template, request
import pandas as pd
from journal import Journals
import urllib


# Initialize Flask app
app = Flask(__name__)

# Read CSV, preprocess data, and create network
jorn = pd.read_csv('journal2022.csv').head(100)
my_journals = Journals(jorn)
my_journals.preprocess()
G = my_journals.network()


# Get the title and categories data
title_info = my_journals.journal_info['Title']
categories_data = my_journals.journal_info['Categories']

# categories is each uniqu category in the column 'Categories' of the dataframe after preprocessing
#sort alphabetically
categories = sorted(list(set([item for sublist in categories_data for item in sublist])))

@app.route('/')
def site():
    return render_template('site.html', categories=categories)

@app.route('/category', methods=['POST'])
def category():
    # Retrieve the selected categories from the form.
    selected_category1 = request.form.get('category1')
    selected_category2 = request.form.get('category2')

    if not selected_category1 or not selected_category2:
        return render_template('site.html', categories=categories, error="Please select two categories.")
    
    both_categories = []
    only_category1 = []
    only_category2 = []

    # Separate journals into respective lists based on category selection
    for title, cats in zip(title_info, categories_data):
        if selected_category1 in cats and selected_category2 in cats:
            both_categories.append(title)
        elif selected_category1 in cats:
            only_category1.append(title)
        elif selected_category2 in cats:
            only_category2.append(title)
    
    return render_template(
        'category.html',
        both_categories=both_categories,
        only_category1=only_category1,
        only_category2=only_category2,
        selected_categories=[selected_category1, selected_category2]
    )
@app.route('/journal')
def journal():
    title = request.args.get('title')
    if not title:
        return render_template('site.html', categories=categories, error="Please select a journal.")

    title = urllib.parse.unquote(title)
    
    journal_details = my_journals.journal_info[my_journals.journal_info['Title'] == title]
    
    if journal_details.empty:
        return render_template('404.html', title=title)

    journal_details = journal_details.iloc[0].to_dict()
    
    # Check if the graph contains the node for this title
    if title in my_journals.G:  # Note that we reference the graph from the my_journals instance
        neighbors = list(my_journals.G.neighbors(title))  # Again, note the use of my_journals.G
        
        # Sort neighbors by edge weight, descending order
        neighbors_by_weight = sorted(neighbors, key=lambda x: my_journals.G[title][x]['weight'], reverse=True)
        
        related_articles = neighbors_by_weight[:3]
    else:
        related_articles = []

    return render_template('journal.html', journal=journal_details, related_articles=related_articles)


if __name__ == '__main__':
    app.run(debug=True, port='8000')
