# Example queries

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
