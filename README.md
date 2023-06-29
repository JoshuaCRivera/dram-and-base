# dram-and-base

This is our README documentation, our query file is query.txt.

## Our story
We are interested in dramas spanning different times, genres and languages. We are looking at structural and statistical information rather than deep linguistic or literary annotations.
We are interested in questions like:
* How did dramas change over time in their structure?
* Can we find a measure of similarity between plays?
* Can we assign meaningful emotion scores to dramas?
* How do we best visualize such findings?


## Collecting the data
* We use DraCor, a corpus of dramas
* German DraCor includes 621 dramas ranging from 1549 - 1947
* The dramas are available at dracor.org as TEI-encoded XML files
* Present annotations: Info about the play (title, subtitle, author,  year, ...) as well as characters, relations, scenes, speakers, lines/paragraphs
* You can download the files at their [Github](https://github.com/dracor-org/gerdracor)

## Preparing the data
* We used XPath-queries to extract information about the plays as well as calculating statistics about them
* Same for the characters
* We infer genre from keywords in the subtitle
* We used an emotion classification system to assign emotions to lines and aggregated those over plays (by percentage of lines assigned to each emotion category)
- Relevant files: drama_stats.py, character_data.py, count_emotion.py, german_drama_emotion_classifier.py, data_extractor.py
* We put the information into an SQLite database with two tables: one for the dramas and one for the characters
* The columns in the dramas table store information like the number of characters, number of scenes, length of the play in lines, longest dialogue turn... as well as scores for our seven emotions
* The columns in the dramas table store information like their name, which drama they are from, their gender, the number of lines they speak and scenes they appear in, ...
- Relevant files: db_handling.py, drama_base.db

## Accessing the data
* Queries go in main.py
* You can query the database for basic information and some statistics about the dramas and characters.
* You can query the database for emotion information.
* You can calculate the similarity between two dramas.
* You can calculate the similarity between a drama and a group of dramas, or two groups of dramas. These groups can be flexibly defined by an SQL condition.
* You can take a look at the nice graphs and visualizations we generated using our extension.
* See different examples of queries in our queries.txt file.

- Relevant files: db_handling.py
