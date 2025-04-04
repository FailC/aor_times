#!/usr/bin/env python3
# art of rally or as i've recently taken to calling it, art + rally
#
# early access version
#
# CHANGELOG: add stage_number
#
# TODO:
# change time function to use divmod()
# exclude groups or locations? -> better: --groups and --location should take multiple arguemnts
# add daily weekly filter - seperate program?
#
# --stage should take the number of the stage too (takes only the name)
# bit shitty to implement, needs --location to find the stage name
#
# ???
# getting BrokenPipeError when piping into | less
# BrokenPipeError: [Errno 32] Broken pipe
#

import sys
import argparse
import difflib
# for printing to stderr, doesn't get written to a file with >>
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# not important, class is used to make the help message from -h a bit more readable
class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            # "metavar"
            metavar = action.dest.upper()
            return metavar
        else:
            parts = []
            # if the Optional doesn't take a value, format is "-s" or "--long"
            if action.nargs == 0:
                parts.extend(action.option_strings)
            # if the Optional takes a value, format is "-s ARGS" or "--long ARGS"
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                parts.extend(action.option_strings)
                parts[-1] += ' ' + args_string

            return ', '.join(parts)


class Time:
    def __init__(self, ms: int):
        # ms = milliseconds
        self.is_dnf: bool = False
        try:
            hours, minutes, seconds, milliseconds = self.convert_race_time(int(ms))
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds
            self.milliseconds = milliseconds
        except TypeError:
            self.is_dnf = True

    @staticmethod
    def convert_race_time(ms: int) -> tuple[int,int,int,int]:
        if ms >= 356400000:
            # need the rust Option type here..
            raise TypeError
        total_seconds = ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = ms % 1000
        return (hours, minutes, seconds, milliseconds)
    def print_time(self, hours=False) -> str :
        if self.is_dnf:
            return "NF"
        if hours == True:
            return f"{self.hours}:{self.minutes:02d}:{self.seconds:02d}.{self.milliseconds:03d}"
        return f"{self.minutes:02d}:{self.seconds:02d}.{self.milliseconds:03d}"

    def get_time(self, hours=False) -> str:
        string: str = ""
        if self.is_dnf:
             return "DNF"
        if hours == True:
             string = f"{self.hours}:{self.minutes:02d}:{self.seconds:02d}.{self.milliseconds:03d}"
             return string
        return f"{self.minutes:02d}:{self.seconds:02d}.{self.milliseconds:03d}"


class Stage:
    stage_vec = []
    location_stage_names = {
        "finland": ["noormarku", "lamppi", "palus", "lassila", "kairila", "haaparjarvi"],
        "sardinia": ["villacidro", "san gavino monreale", "san benedetto", "gennamari", "portu maga", "montevecchio"],
        "japan": ["nasu highland", "mount asama", "mount akagi", "nikko", "tsumagoi", "mount haruna"],
        "norway": ["laupstad", "vestpollen", "stronstad", "kvannkjosen", "grunnfor", "lake rostavatn"],
        "germany": ["hockweiler", "franzenheim", "holzerath", "farschweiler", "mertesdorf", "gonnesweiler"],
        "kenya": ["mount kenya", "karura", "homa bay", "ndere island", "lake baringo", "lake nakuru"],
        "indonesia": ["mount kawi", "semangka island", "satonda island", "oreng valley", "sangeang island", "kalabakan island"],
        "australia": ["gum scrub", "toorooka", "nulla nulla", "comara canyon", "lake lucernia", "wombamurra"]
    }
    car_names = {
        "60s": ["the esky v1", "the meanie", "la montaine", "das 220", "das 119i", "le gorde", "la regina", "the rotary kei"],
        "70s": ["the esky v2", "il nonno 313", "the rotary 3", "la wedge", "il cavallo 803", "das 119e", "la hepta", "the pepple v1", "the pepple v2", "the zetto"],
        "80s": ["le cinq", "das whip", "turbo brick", "das uberwhip", "the cozzie sr5", "the original", "la super montaine", "la longana", "the gazelle", "das scholar"],
        "groupb": ["the 4r6", "le 502", "das hammer v2", "il gorilla 4s", "the cozzie sr2", "the cozzie sr71", "the rotary b7", "das hammer v1", "das hammer v3", "il monster", "il cavallo 882", "le cinq b", "das uberspeedvan", "the king of africa", "das 559", "the hyena", "das maestro"],
        "groups": ["das eibenhammer","the rotary s7","the umibozu","il gorilla e1","le 504","il gorilla e2","das superbaus","the t22"],
        "groupa": ["il gorillona", "the fujin", "the liftback", "the max attack", "the cozzie 90", "the kingpin"],
        "vans": ["das speedvan", "das hi-speedvan", "das cube van", "funselector's van"],
        "monkey": ["monkey"],
        "dakar": ["dakar"],
        "logging": ["logging truck"]
    }
    debug_stage_count = 0
    def __init__(self,line):
        parts = line.split(":")
        stage = parts[0].split("_")
        self.location: str = stage[0].lower()
        self.stage_number: int = int(stage[2])
        self.stage: str = self.get_stage_name(self.stage_number)
        self.direction: str = stage[3].lower()
        self.weather: str = stage[4].lower()
        self.group: str = stage[5].lower()
        if self.group == "bonus":
            self.group: str = stage[6].lower()
        self.car_number: int = int(parts[2])
        self.car_name: str = self.get_car_name()
        self.time_ms: int = int(parts[1])
        self.time: Time = Time(parts[1])
        Stage.debug_stage_count += 1

    def get_stage_name(self, number: int) -> str:
        # aor stages start at 1
        return Stage.location_stage_names[self.location][number-1]

    def get_car_name(self) -> str:
        return Stage.car_names[self.group][self.car_number]


# don't need the location for now
# add this to a class? who needs OOP am i right..
# I HECKING LOVE LIST COMPREHENSIONS
all_stages: dict[str, str] = {stage: location for location, stages in Stage.location_stage_names.items() for stage in stages}
def find_stage(stage_name: list[str]) -> list[str]:
    stage_list: list[str] = []
    for name in stage_name:
       if name in all_stages:
           stage_list.append(name)
       else:
           suggestions = difflib.get_close_matches(name, all_stages)
           if suggestions:
               eprint(f"Warning: Stage '{name}' not found -> using {suggestions[0]}")
               stage_list.append(suggestions[0])
           else:
               eprint(f"ERROR: Stage '{stage_name}' not found")
               raise SystemError
               #exit()
    return stage_list


def print_ascii():
    print(r"""
        _ _           _ _
_ __ __ _| | |_   _  __| | |__
| '__/ _` | | | | | |/ _` | '_ \
| | | (_| | | | |_| | (_| | |_) |
|_|  \__,_|_|_|\__, |\__,_|_.__/
            |___/
    """)


def main() -> None:
    total_time: int  = 0
    debug_week_counter: int = 0
    filename: str = ""
    parser = argparse.ArgumentParser(description="rally car goes vrooaaam",formatter_class=CustomFormatter)
    parser.add_argument( '-l','--location', nargs='+', choices=["finland", "japan" ,"sardinia" ,"norway", "germany", "kenya", "indonesia", "australia"], default=["finland", "japan" ,"sardinia" ,"norway", "germany", "kenya", "indonesia", "australia"])
    parser.add_argument( '-g','--group', nargs='+', choices=["60s", "70s", "80s", "groupb", "groups", "groupa", "vans", "monkey", "dakar", "logging"], default=["60s", "70s", "80s", "groupb", "groups", "groupa", "vans", "dakar", "monkey", "logging"])
    parser.add_argument('-c', '--car', action='store_true', help='print out the used car')
    parser.add_argument('-s', '--stage', nargs='+', default=None, help='search for stage name, will provide the best match, enclose long names in quotation marks: "nulla nulla"')
    parser.add_argument( '-d','--direction', choices=["forward", "reverse"], default=["forward", "reverse"])
    parser.add_argument( '-w','--weather', choices=["dry", "wet"], default=["dry", "wet"])
    parser.add_argument('-t', '--totaltime', action='store_true', help='print total time of all selected stages')
    parser.add_argument('-x', '--onlytime', action='store_true', help='only print the total time of selected stages')
    parser.add_argument('-a', '--argprint', action='store_true', help='print headlines containing provided arguments, for easy overview')
    parser.add_argument('-f', '--filename', default="Leaderboards.txt",help='provide custom file name')
    parser.add_argument('-r', '--rally', action='store_true', help="print cool ascii art")
    args = parser.parse_args()

    # add arguments to ignore with --argprint:
    ignore_user_args = ["onlytime", "argprint", "totaltime", "car"]

    if args.rally:
        print_ascii()
        sys.exit()

    if args.filename:
        filename = args.filename
    try:
        with open(filename, "r") as file:
            for i, line in enumerate(file):
                if "daily" in line or "weekly" in line:
                    debug_week_counter += 1
                    continue
                if "Custom" in line:
                    continue
                try:
                    Stage.stage_vec.append(Stage(line))
                except:
                    print(f"ERROR: can't read line {i} of file {filename}:")
                    print(line)
                    sys.exit()
    except FileNotFoundError:
        eprint(f"ERROR:  {args.filename}  file not found")
        eprint("try: ", end='')
        eprint("file needs to be in the same directory as rallydb.py")
        sys.exit()

    if args.stage:
        try:
            args.stage = find_stage(args.stage)
        except SystemError:
            sys.exit()

    output = []

    # getting the user provided arguments
    if args.argprint:
        defaults = parser.parse_args([])
        # I HECKING LOVE LIST COMPREHENSIONS
        user_provided_args = {k: v for k, v in vars(args).items() if vars(args)[k] != vars(defaults)[k]}
        # print(f"----------   ", end='')
        output.append(f"----------   ")
        for arg, value in user_provided_args.items():
            if arg in ignore_user_args:
                continue
            output.append(f'{value}   ')
        output.append(f"----------   \n")

    for stage in Stage.stage_vec:
        if (
            stage.location in args.location and
            stage.group in args.group and
            stage.direction in args.direction and
            stage.weather in args.weather and
            (not args.stage or stage.stage in args.stage)
        ):
            time = stage.time.print_time()
            if not args.onlytime:
                if args.car:
                    output.append(f"{stage.location:<15} {stage.stage:<20} {stage.group:<15} {stage.car_name:<20} {stage.direction:<10} {stage.weather:<10} {time}")
                else:
                    output.append(f"{stage.location:<15} {stage.stage:<20} {stage.group:<15} {stage.direction:<10} {stage.weather:<10} {time}")
                # stage.time.print_time()
                # output.append(stage.time.print_time())
            if not stage.time.is_dnf:
                total_time += stage.time_ms

    if args.totaltime:
        new = Time(total_time)
        output.append(f"----------   ")
        # print(new.get_time())
        output.append(new.get_time())
        #new.print_time(hours=True)

    for line in output:
        print(line)


if __name__ == "__main__":
    main()
