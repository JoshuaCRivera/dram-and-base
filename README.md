# dram-and-base

## Our story
We are interested in

## Collecting the data
* We use DraCor, a corpus of dramas
* German DraCor includes 621 dramas ranging from 1549 - 1947
* The dramas are available at dracor.org as TEI-encoded XML files
* ...

## Preparing the data
* We used XPath-queries ...
* ...
* We put the information into an SQLite database with two tables: one for the dramas and one for the characters
* The columns store information like ...

## Accessing the data
* You can query the database for basic information and some statistics about the dramas and characters.
* You can query the database for emotion information.
* You can calculate the similarity between two dramas.
* You can calculate the similarity between a drama and a group of dramas, or two groups of dramas. These groups can be flexibly defined by an SQL condition.
* You can take a look at the nice graphs and visualizations we generated using our extension.
