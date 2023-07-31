# Example queries

## Plays without male characters

```sql
SELECT d.title, d.id 
FROM dramas AS d 
WHERE d.id NOT IN (
    SELECT c.drama_id 
    FROM characters AS c 
    WHERE c.gender = 'MALE') 
    AND d.id NOT LIKE 'min' AND d.id NOT LIKE 'max'
```

```
(3, [('Proserpina', 'goethe-proserpina'), 
('Die von der Weisheit wider die Unwissenheit beschützte Schauspielkunst', 'neuber-die-beschuetzte-schauspielkunst'), 
('Die Verehrung der Vollkommenheit durch die gebesserten deutschen Schauspiele', 'neuber-die-verehrung-der-vollkommenheit')])
```

## Plays about Faust
How many dramas are there where the character with the most lines is called some variant of "Faust"?
```sql
SELECT COUNT(*)
FROM dramas AS d
JOIN characters AS c ON d.id = c.drama_id
WHERE c.name LIKE '%Faust%' AND c.num_lines = (SELECT max(ch.num_lines) FROM characters AS ch WHERE c.drama_id = ch.drama_id)
```
```
16 (Note that there are 25 dramas with a "Faust" character overall)
```

## Average number of lines per gender

```sql
SELECT gender, avg(num_lines) AS avg_lines
FROM characters
GROUP BY gender;
```

```
gender	avg_lines
FEMALE	40.15990613476366
MALE	28.73341737781226
UNKNOWN	4.53484602917342
unknown	2
```

## Gender distribution in Goethe plays

```sql
SELECT characters.gender, count(characters.gender)
FROM characters, dramas
 WHERE dramas.id = characters.drama_id
 AND dramas.author LIKE '%Goethe%'
GROUP BY gender;
```

```
gender	count(characters.gender)
FEMALE	160
MALE	388
UNKNOWN	84
```

## Dead parents
Main characters whose parents die onstage
```sql
SELECT c.name AS child, p.name AS parent
FROM characters AS c 
JOIN characters AS p ON c.drama_id = p.drama_id
WHERE c.main_char = 'Yes' AND p.dead = 'Yes' AND p.relations LIKE '%parent_of to ' || replace(c.id, rtrim(c.id, replace(c.id, '-', '')), '') || ')%'
```
```
child       parent
Franz	    Ferner
Angelo	    Maria
Faust	    Faustens Vater
Faust	    Diether
Prinzessin Alma	König Nicolo
Karl	    Kaiser Ludwig
```

## Looking at emotions
Get the play with the highest love score
```sql
SELECT d1.title, d1.genre
FROM dramas as d1, dramas as d2
WHERE d1.Liebe = d2.Liebe and d2.id = 'max' and d1.id <> 'max'
```

```
(1, [('Die zärtlichen Schwestern', 'comedy')])
```

Get the saddest play
```sql
SELECT d1.title, d1.genre
FROM dramas as d1, dramas as d2
WHERE d1.Leid = d2.Leid and d2.id = 'max' and d1.id <> 'max'
```

```
(1, [('Cili Cohrs', 'unknown')])
```
--> not annotated as comedy or tragedy, but we would suspect it from the score (and indeed it is described as "Irnsthaftig Spill" in the subtitle)

## Comedies with less than 10 scenes


```sql
SELECT title FROM dramas WHERE genre = 'comedy' AND num_scenes < 3;
```

```
title
Gute Freunde
Der Antiquar
Berengar
Das Gift
Der Herr vom Jenseits
Die Urgrossmutter
Komtesse Mizzi oder Der Familientag
Literatur
Die Dorfschule
```

## Similarity sanity check
We expect that plays by the same author have high similarity, higher than that to other plays of the same time.
We also expect plays from the same epoch to have higher similarity than plays from different epochs.
(We use the ID here, since there ar etwo plays called "Medea")

We can see that the similarity measures behave as expected.

```python
similarity('grillparzer-medea', 'Sappho')
similarity("grillparzer-medea', 'year = '1821'")
similarity('grillparzer-medea', "year = '1921'")
```

```
0.870
0.842
0.793
```


## What is a melodrama?
The drama "Ino" is described as a "melodrama". We want to know whether it has more similarity with a comedy or a tragedy. We see that the similarity is higher to tragedies than to comedies.

```python
similarity('Ino', "genre = 'comedy'")
similarity('Ino', "genre = 'tragedy'")
```

```
0.621
0.694
```

