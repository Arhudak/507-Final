# import pandas as pd
# import matplotlib.pyplot as plt
# import networkx as nx
# from flask import Flask, render_template, request, jsonify
# from itertools import chain

# #take a sample of the first 100 data to work with 100 make it consistent for all users to work with the same data
# journal = pd.read_csv('journal2022.csv').head(100)


# class Journals:
# 	def __init__(self, journal_df):
# 		self.journal = journal_df
# 		self.G = nx.Graph()
# 		self.title = self.journal['Title']
# 		self.categories = self.journal['Categories']

# 	def preprocess(self):
# 		#extract the desired columns for my analysis
# 		self.journal_info = self.journal[['Title', 'Type', 'Issn', 'SJR', 'SJR Best Quartile', 'H index', 'Total Docs. (2022)', 'Total Docs. (3years)', 'Total Refs.', 'Total Cites (3years)', 'Citable Docs. (3years)', 'Cites / Doc. (2years)', 'Ref. / Doc.', 'Country', 'Publisher', 'Categories', 'Areas']].copy()
# 		#determine if there are any missing values and drop these rows
# 		self.journal_info.dropna(inplace=True)
# 		#Process the categories column
# 		self.journal_info['Categories'] = self.journal_info['Categories'].apply(lambda x: x.split(';'))
# 		# drop (quater) from catergories. Example Clinical Psychology (Q4) = Clinical Psychology
# 		self.journal_info['Categories'] = self.journal_info['Categories'].apply(lambda x: [i.split(' (')[0] for i in x])
# 		#group the categories with the same name
# 		self.journal_info['Categories'] = self.journal_info['Categories'].apply(lambda x: list(set(x)))
# 		#sort the categories by most common
# 		self.journal_info['Categories'] = self.journal_info['Categories'].apply(lambda x: sorted(x, key=lambda y: self.journal_info['Categories'].apply(lambda z: y in z).sum(), reverse=True))


# 	def compute_co_occurrences(self):
# 		#provide a dictionary of co-occurrences of categories 
# 		#this means that if two categories appear together in the same journal, the count of the pair is increased by 1
# 			co_occurrences = {}
# 			for _, row in self.journal_info.iterrows():
# 				categories = row['Categories']
# 				for i in range(len(categories)):
# 					for j in range(i + 1, len(categories)):
# 						pair = tuple(sorted([categories[i], categories[j]]))
# 						co_occurrences[pair] = co_occurrences.get(pair, 0) + 1
# 			return co_occurrences

# 	def network(self):
# 		co_occurrence = self.compute_co_occurrences()
# 		for pair, weight in co_occurrence.items():
# 			if weight > 0:
# 				self.G.add_edge(pair[0], pair[1], weight=weight)
#             	# Assign categories to the nodes
# 				if pair[0] not in self.G.nodes:
# 					self.G.nodes[pair[0]]['category'] = pair[0]
# 				if pair[1] not in self.G.nodes:
# 					self.G.nodes[pair[1]]['category'] = pair[1]
# 		return self.G

# 	def visualize(self):
# 		plt.figure(figsize=(10, 8))
# 		pos = nx.spring_layout(self.G, k=0.1)
# 		nx.draw(self.G, pos, node_size=75, node_color='lightblue', font_size=10, font_weight='bold', width=1, edge_color='gray', edgecolors='darkgray')
# 		plt.title('Article Co-occurrence Network Based on Shared Categories')
# 		plt.show()

# def main():
# 	#run preprocess, network and visualize methods
# 	my_journals = Journals(journal)
# 	my_journals.preprocess()
# 	my_journals.network()
# 	my_journals.visualize()

# if __name__ == "__main__":
#     main()


import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from flask import Flask, render_template, request, jsonify
from itertools import chain

# Take a sample of the first 100 data to work with 100 make it consistent for all users to work with the same data
journal = pd.read_csv('journal2022.csv').head(100)


class Journals:
    def __init__(self, journal_df):
        self.journal = journal_df
        self.G = nx.Graph()
        self.title = self.journal['Title']
        self.categories = self.journal['Categories']

    def preprocess(self):
        self.journal_info = self.journal[
            ['Title', 'Type', 'Issn', 'SJR', 'SJR Best Quartile', 'H index', 'Total Docs. (2022)',
             'Total Docs. (3years)', 'Total Refs.', 'Total Cites (3years)', 'Citable Docs. (3years)',
             'Cites / Doc. (2years)', 'Ref. / Doc.', 'Country', 'Publisher', 'Categories', 'Areas']].copy()
        self.journal_info.dropna(inplace=True)
        self.journal_info['Categories'] = self.journal_info['Categories'].apply(lambda x: x.split(';'))
        self.journal_info['Categories'] = self.journal_info['Categories'].apply(
            lambda x: [i.split(' (')[0] for i in x])
        self.journal_info['Categories'] = self.journal_info['Categories'].apply(lambda x: list(set(x)))
        self.journal_info['Categories'] = self.journal_info['Categories'].apply(
            lambda x: sorted(x, key=lambda y: self.journal_info['Categories'].apply(lambda z: y in z).sum(),
                             reverse=True))
        
        self.network()

	
    def network(self):
        # Initialize a dictionary that maps categories to the titles they appear in
        category_to_titles = {}
        for _, row in self.journal_info.iterrows():
            title = row['Title']
            categories = row['Categories']
            for category in categories:
                if category in category_to_titles:
                    category_to_titles[category].append(title)
                else:
                    category_to_titles[category] = [title]

        # Now add the nodes, which are the titles
        for title in self.journal_info['Title']:
            self.G.add_node(title)
            
        # Add edges between all titles that share a category
        for titles in category_to_titles.values():
            for title1 in titles:
                for title2 in titles:
                    if title1 != title2:
                        # This checks if an edge already exists and increments the weight if it does
                        if self.G.has_edge(title1, title2):
                            self.G[title1][title2]['weight'] += 1
                        else:
                            self.G.add_edge(title1, title2, weight=1)
                            
    #     for index, row in self.journal_info.iterrows():
    #         for category in row['Categories']:
    #             self.G.add_node(row['Title'], categories=row['Categories'])
    #             for index2, other_row in self.journal_info.iterrows():
    #                 if other_row['Title'] != row['Title'] and any(cat in other_row['Categories'] for cat in
    #                                                               row['Categories']):
    #                     self.G.add_edge(row['Title'], other_row['Title'])


    def visualize(self):
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.G, k=0.1)
        nx.draw(self.G, pos, node_size=75, node_color='lightblue', font_size=10, font_weight='bold', width=1,
                edge_color='gray', edgecolors='darkgray')
        plt.title('Article Co-occurrence Network Based on Shared Categories')
        plt.show()

    # class CategoriesAnalysis:
    #     def __init__(self, journal_df):
    #         self.journal = journal_df
    #         self.G = nx.Graph()

    #     def compute_co_occurrences(self):
    #         co_occurrences = {}
    #         for _, row in self.journal.iterrows():
    #             categories = row['Categories']
    #             for i in range(len(categories)):
    #                 for j in range(i + 1, len(categories)):
    #                     pair = tuple(sorted([categories[i], categories[j]]))
    #                     co_occurrences[pair] = co_occurrences.get(pair, 0) + 1
    #         return co_occurrences

    #     def categoriesnetwork(self):
    #         co_occurrence = self.compute_co_occurrences()
    #         for pair, weight in co_occurrence.items():
    #             if weight > 0:
    #                 self.G.add_edge(pair[0], pair[1], weight=weight)
    #                 if pair[0] not in self.G.nodes:
    #                     self.G.nodes[pair[0]]['category'] = pair[0]
    #                 if pair[1] not in self.G.nodes:
    #                     self.G.nodes[pair[1]]['category'] = pair[1]
    #         return self.G

    #     def visualize(self):
    #         plt.figure(figsize=(10, 8))
    #         pos = nx.spring_layout(self.G, k=0.1)
    #         nx.draw(self.G, pos, node_size=75, node_color='lightblue', font_size=10, font_weight='bold', width=1,
    #                 edge_color='gray', edgecolors='darkgray')
    #         plt.title('Article Co-occurrence Network Based on Shared Categories')
    #         plt.show()

    # class TitleAnalysis:
    #     def __init__(self, journal_df):
    #         self.journal = journal_df
    #         self.G = nx.Graph()

    #     def add_nodes_and_edges(self, G):
    #         for index, row in self.journal.iterrows():
    #             for category in row['Categories']:
    #                 G.add_node(row['Title'], categories=row['Categories'])
    #                 for index2, other_row in self.journal.iterrows():
    #                     if other_row['Title'] != row['Title'] and any(cat in other_row['Categories'] for cat in
    #                                                                   row['Categories']):
    #                         G.add_edge(row['Title'], other_row['Title'])

    #     def visualize(self):
    #         plt.figure(figsize=(10, 8))
    #         pos = nx.spring_layout(self.G, k=0.1)
    #         nx.draw(self.G, pos, node_size=75, node_color='lightblue', font_size=10, font_weight='bold', width=1,
    #                 edge_color='gray', edgecolors='darkgray')
    #         plt.title('Article Co-occurrence Network Based on Shared Categories')
    #         plt.show()


def main():
    my_journals = Journals(journal)
    my_journals.preprocess()
    my_journals.visualize()


if __name__ == "__main__":
    main()
