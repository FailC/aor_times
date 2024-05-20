# art of rally or as i've recently taken to calling it, art plus rally
#
# early access version
#

import sys
import argparse
import difflib

# not important, class is used to make the help message from -h a bit more readable
# well still kinda ugly
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
    def __init__(self, ms):
        self.dnf: bool = False
        try:
            hours, minutes, seconds, milliseconds = self.convert_race_time(int(ms))
            self.hours = hours
            self.minutes = minutes
            self.seconds = seconds
            self.milliseconds = milliseconds
        except TypeError:
            self.dnf = True

    @staticmethod
    def convert_race_time(ms: int) -> tuple[int,int,int,int]:
        if ms >= 356400000:
            # need the rust Option type here
            raise TypeError
        # Convert milliseconds to seconds
        total_seconds = ms // 1000
        # Extract hours, minutes, and remaining seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        # Extract remaining milliseconds
        milliseconds = ms % 1000
        return (hours, minutes, seconds, milliseconds)
    def print_time(self, hours=False):
        if self.dnf:
            print("DNF")
            return
        if hours == True:
            print(f"{self.hours}:{self.minutes:02d}:{self.seconds:02d}.{self.milliseconds:03d}")
            return
        print(f"{self.minutes:02d}:{self.seconds:02d}.{self.milliseconds:03d}")

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
    # add bonus cars
    # todo check if the integers are the right cars
    # car integer starts at 0
    car_names = {
        "60s": ["the esky v1", "the meanie", "la montaine", "das 220", "das 119i", "le gorde", "la regina", "the rotary kei"],
        "70s": ["the esky v2", "il nonno 313", "the rotary 3", "la wedge", "il cavallo 803", "das 119e", "la hepta", "the pepple v1", "the pepple v2", "the zetto"],
        "80s": ["le cinq", "das whip", "turbo brick", "das uberwhip", "the cozzie sr5", "the original", "la super montaine", "la longana", "the gazelle", "das scholar"],
        "groupb": ["the 4r6","le 502","das hammer v2","il gorilla 4s","the cozzie sr2","the cozzie sr71","the rotary b7","das hammer v3","il monster","il cavallo 882","le cinq b","das uberspeedvan", "the king of africa", "das 559", "the hyena", "das maestro"],
        "groups": ["das eibenhammer","the rotary s7","the umibozu","il gorilla e1","le 504","il gorilla e2","das superbaus","the t22"],
        "groupa": ["il gorillona","the fujin","the liftback","the max attack","the cozzie 90","the kingpin"],
        # todo add bonus car names
        "logging": ["logging truck"],
        "vans": ["van", "van", "van", "van", "van"],
        "dakar": ["dakar", "dakar", "dakar", "dakar"],
        "monkey": ["monkey","monkey","monkey","monkey"]
    }

    debug_stage_count = 0
    def __init__(self,line):
        parts = line.split(":")
        stage = parts[0].split("_")
        self.location: str = stage[0].lower()
        self.stage: str = self.get_stage_name(int(stage[2]))
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

# maybe there is a shorter way, don't need the location
# add this to a class? who needs OOP am i right..
all_stages = {stage: location for location, stages in Stage.location_stage_names.items() for stage in stages}
def find_stage(stage_name: str) -> str:
    if stage_name in all_stages:
        return stage_name
    else:
        suggestions = difflib.get_close_matches(stage_name, all_stages)
        if suggestions:
            eprint(f"Stage '{stage_name}' not found. Did you mean: {', '.join(suggestions)}?")
            return suggestions[0]
        else:
            eprint(f"Stage '{stage_name}' not found")
            exit()

# for printing to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    week_counter = 0
    with open("newLeaderboards.txt", "r") as file:
        for line in file:
            if "daily" in line or "weekly" in line:
                week_counter += 1
                continue
            Stage.stage_vec.append(Stage(line))

    parser = argparse.ArgumentParser(description="rally car goes vrooaaam",formatter_class=CustomFormatter)

    # for counting lines just use wc -l (no bloat..), doesnt work anymore with printing headline, works again with extra --argprint
    # add types in the argument, instead in the class? not really necessary i think
    # exclude groups or locations?
    # add daily weekly filter
    # add path option for changed name for leaderboards.txt file
    # add option to print the headline containing all the chosen option?
    parser.add_argument( '-l','--location', choices=["finland", "japan" ,"sardinia" ,"norway", "germany", "kenya", "indonesia", "australia"], default=["finland", "japan" ,"sardinia" ,"norway", "germany", "kenya", "indonesia", "australia"], help='specify a location')
    parser.add_argument( '-g','--group', choices=["60s", "70s", "80s", "groupb", "groups", "groupa", "vans", "monkey", "dakar", "logging"], default=["60s", "70s", "80s", "groupb", "groups", "groupa", "vans", "dakar", "monkey", "logging"], help='specify a group')
    parser.add_argument('-c', '--car', action='store_true', help='print out the used car')
    # should stage take the number of the stage too?
    parser.add_argument('-s', '--stage', default=None, help="search for stage name. Doesn't need the location argument")
    parser.add_argument( '-d','--direction', choices=["forward", "reverse"], default=["forward", "reverse"])
    parser.add_argument( '-w','--weather', choices=["dry", "wet"], default=["dry", "wet"])
    parser.add_argument('-t', '--total_time', action='store_true', help='print total time of all selected stages')
    parser.add_argument('-x', '--only_time', action='store_true', help='only print the total time of selected stages')
    parser.add_argument('-a', '--argprint', action='store_true', help='print headlines containing provided arguments, for easy overview')
    args = parser.parse_args()

    # getting the user only provided arguments
    # if stage name is provided, it's printing the "wrong" name
    if args.argprint:
        # need to exclude some options like --headline or --car doesn't make sense
        defaults = parser.parse_args([])
        user_provided_args = {k: v for k, v in vars(args).items() if vars(args)[k] != vars(defaults)[k]}
        print(f"-----------  ", end='')
        for arg, value in user_provided_args.items():
            print(f'{arg}: {value}     ', end='')
        print(f"-----------  ")

    total_time = 0
    if args.stage:
        args.stage = find_stage(args.stage)

    #todo getting BrokenPipeError lol
    for stage in Stage.stage_vec:
        if stage.location in args.location and stage.group in args.group and stage.direction in args.direction and stage.weather in args.weather and (not args.stage or stage.stage in args.stage):
            if not args.only_time:
                # kinda shit but oh well
                if args.car:
                    print(f"{stage.location:<15} {stage.stage:<20} {stage.group:<15} {stage.car_name:<20} {stage.direction:<10} {stage.weather:<10}", end='')
                else:
                    print(f"{stage.location:<15} {stage.stage:<20} {stage.group:<15} {stage.direction:<10} {stage.weather:<10}", end='')
                stage.time.print_time()
            total_time += stage.time_ms

    if args.total_time:
        new = Time(total_time)
        #print("total time:  ", end='')
        new.print_time(hours=True)



if __name__ == "__main__":
    main()
