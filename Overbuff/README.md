# Python Overbuff / Overwatch API

Usage:

Save overbuff.py in the same directory and then import it
```python
import overbuff
```

## Functions

```python
listHeroes()
listStats(battletag, hero)
getStat(battletag, stat, hero)
getHighestStat(battletag, stat)
getHeroRanking(battletag, hero, comp=False)
compareStats(battletag1, battletag2, stat, hero)
getLevel(battletag)
getSR(battletag)
```

Here's an example:

```python
print(getSR('User#1234'))
```
```
>>> 2700
```
