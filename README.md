## Various Python scripts for the art of rally Leaderboards.txt file. For speedrunning, checking times or 100% completion of the game. 

- progress.py gives a simple overview over stage/groups completion

- rallydb.py lets you search for groups, locations or for individual stages.   

- rallyui.py is a simple graphical user interface for rallydb.py 

**The Leaderboards.txt file must be in the same working directory as the scripts**

- Linux: `$HOME/.config/unity3d/Funselektor Labs/Art of Rally/cloud/Leaderboards.txt`

- macOS: `$HOME/Library/Application Support/Funselektor Labs/Art of Rally/cloud/Leaderboards.txt`
- Windows: `C:\Users\USERNAME\AppData\LocalLow\Funselektor Labs\art of rally\cloud\Leaderboards.txt`

  - useful for proton steam version:
    ```
    find ~/ -name "Leaderboards.txt"
    ```

### rallydb.py

show help page with all options, every argument has a short and ""--long" version
```
python3 rallydb.py --help
```
filter search for  finland, Group A, only reverse stages
```
python3 rallydb.py -l finland -g groupa -d reverse
```
search for a single stage with -s (returns the closest match), print out the combined times with -t / --totaltime
```
python3 rallydb.py -g groupb -s haaparjarvi --weather dry --totaltime
```
you can override which file the script uses with the -f argument
```
python3 rallydb.py -f myleaderboard.txt
```

### rallyui.py
let's you easily search and add stages to calculate the sum of best / or just for checking your PB's 

start rallyui.py
```
python3 rallyui.py
```

<img width="1154" alt="rallyui" src="https://github.com/FailC/aor_times/assets/90941819/f226720b-0483-43b7-85e6-545668cd76f4">

some distributions may not have the tk package installed
```
sudo pacman -S tk
```

### times.py 
for the advanced command line rally pilot 

create custom list of rally stages and use times.py to calculate sum of best

for anything where rallydb.py can't just print out the total time with --totaltime

send single stages to a new file
```
python3 rallydb.py -s lampi -g 60s -d forward -w wet >> sumofbest.txt
python3 rallydb.py -s mertesdorf -g 60s -d reverse -w dry >> sumofbest.txt
```
pipe file into times.py 
```
cat sumofbest.txt | python3 times.py 
```
or use -f option 
```
python3 times.py -f sumofbest.txt
```
you can manually edit the file, times.py only takes the last string in the file and tries to add it to a total time






