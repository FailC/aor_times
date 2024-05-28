#!/usr/bin/env python3

import argparse
import sys
import select

# takes txt file with stages, outputs total time
# for building unique list of different stages
# ignores the total time (--totaltime) output from rallydb.py
# only add the times at the end of the single stage lines:
# input file should look like
# finland         noormarku            groupa          the liftback         forward    dry       01:12.015
# finland         lamppi               groupa          the fujin            forward    dry       02:32.515
# ..

# reading in times that looks like this?
#arch :: code/pyrally/aor_times ‹testing*› » py rallydb.py -l finland -x -t -a
#----------   finland   ----------
#----------   6:09:06.173
#arch :: code/pyrally/aor_times ‹testing*› »


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def convert_race_time(ms: int) -> tuple[int,int,int,int]:
    #if ms >= 356400000:
    # need the rust Option type here..
        #raise TypeError
    total_seconds = ms // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = ms % 1000
    return (hours, minutes, seconds, milliseconds)

def main():
    filename: str = ""
    words: list[str] = []
    lines: list[str] = []
    total_min: int = 0
    total_sec: int = 0
    total_ms: int = 0
    milliseconds: int = 0
    parser = argparse.ArgumentParser(description="sum of best calculator :) ")
    parser.add_argument('-f','--filename', required=False,  help='takes output file from rallydb')
    args = parser.parse_args()

    # for piped input
    if not args.filename:
        if not sys.stdin.isatty():
            if select.select([sys.stdin], [], [], 0.1)[0]:
                lines = sys.stdin.readlines()
                if not lines:
                    eprint("ERROR: no data provided")
                    sys.exit(1)
            else:
                eprint("ERROR: no data provided, second one debug")
        else:
            eprint("ERROR: no input file. Use -f flag to specify filename")
            eprint("example: python3 times.py -f filename")
            eprint("or do:")
            eprint("cat file | python3 times.py")
            sys.exit(1)

    else:
        filename: str = args.filename.strip()
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
                eprint(f"File not found: {filename}")
                sys.exit(1)

    for line in lines:
        #ignore every ----- line from rallydb
        if line[0] == "-":
            continue
        words = line.split()
        times = words[-1]
        if times == "DNF":
            continue
        min = int(times[0:2])
        sec = int(times[3:5])
        ms = int(times[6::])
        total_min += min
        total_sec += sec
        total_ms += ms
        milliseconds += ms
        milliseconds += sec * 1000
        milliseconds += min * 60 * 1000
    h, m, s, ms = convert_race_time(milliseconds)
    if h >= 1:
        print(f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}")
    else:
        print(f"{m:02d}:{s:02d}.{ms:03d}")

if __name__ == "__main__":
    main()
