# The file "Leaderboards.txt" must be located in the same directory in which the script is executed.
#
# daily/weekly events are excluded
#
# made by FailX and MxCraven

import argparse

# not important, class is used to make the help message from -h a bit more readable - FailX (craven doesn't know what this does at all)
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

parser = argparse.ArgumentParser(description="Gives info of your leaderboard file",formatter_class=CustomFormatter)
parser.add_argument('-f','--file', action='store_const', const='file')
args = parser.parse_args()


def convert(milliseconds):
    seconds = milliseconds / 1000 
    minutes = seconds / 60
    hours = seconds / 3600
    days = hours / 24
    return seconds, minutes, hours, days

def convert_hour_min(milliseconds):
    # converts to hour:min format
     ms=int(milliseconds)%1000
     s=int(milliseconds/1000)%60
     m=int(milliseconds/(1000*60))%60
     h=int(milliseconds/(1000*60*60))%24
     d=int(milliseconds/(1000*60*60*24))
     return ms,s,m,h,d


output_array = ["_____________________"]

# init hashmap

group_total_time = 0
group_strings = []

country_total_time = 0
country_strings = []

country_total = 0
group_total = 0

rainSetting = "all"

def get_settings():
    global country_strings
    global group_strings
    global country_total
    global group_total
    global rainSetting

    isAus = input("Do you want to include Australia? No/Yes ").lower()
    #print(f"is aus: {isAus}")

    if isAus == "no" or isAus == "n":
        #print("yes")
        country_strings = ["Finland", "Sardinia", "Japan", "Norway", "Germany", "Kenya", "Indonesia"]
        country_total = 168
    else:
        #print("no")
        country_strings = ["Finland", "Sardinia", "Japan", "Norway", "Germany", "Kenya", "Indonesia", "Australia"]
        country_total = 192

    isBonus = input("Do you want bonus vehicles? No/Only/All ").lower()
    #print(f"is bonus: {isBonus}")

    if isBonus == "no" or isBonus == "n":
        #print("no")
        group_strings = ["60s","70s","80s","GroupB","GroupS","GroupA"]
        group_total = 6
    elif isBonus == "only" or isBonus == "o":
        #print("only")
        group_strings = ["Logging","Vans","Dakar","Monkey"]
        group_total = 4
    else:
        #print("all")
        group_strings = ["60s","70s","80s","GroupB","GroupS","GroupA","Logging","Vans","Dakar","Monkey"]
        group_total = 10


    isRain = input("Do you want to include rain stages? Dry/Wet/Both ").lower()

    if isRain == "dry" or isRain == "d":
        rainSetting = "dry"
        country_total = country_total / 2
    elif isRain == "wet" or isRain == "w":
        rainSetting = "wet"
        country_total = country_total / 2
    else:
        rainSetting = "all"

get_settings()

group_counts = {string: 0 for string in group_strings}
group_stages = {string: 0 for string in group_strings}

country_counts = {string: 0 for string in country_strings}
country_stages = {string: 0 for string in country_strings}

dnf_count = 0


# print()
output_array.append("")
try:
    with open("Leaderboards.txt", "r") as file:
        for line in file:
            parts = line.split(":")
            if len(parts) >= 3: # kind off pointless if the file hasn't changed
                #Groups
                for group in group_strings:
                    if group in parts[0]:
                       time = int(parts[1].strip())
                       if time >= 356400000:
                            dnf_count += 1
                            break
                       for country in country_strings:
                           if country in parts[0]:
                                if rainSetting == "dry":
                                    if "Dry" in parts[0]:
                                        group_total_time += time
                                        group_counts[group] += time
                                        group_stages[group] += 1
                                elif rainSetting == "wet":
                                    if "Wet" in parts[0]:
                                        group_total_time += time
                                        group_counts[group] += time
                                        group_stages[group] += 1
                                else:
                                    group_total_time += time
                                    group_counts[group] += time
                                    group_stages[group] += 1


                #Countries
                for country in country_strings:
                    if country in parts[0]:
                        time = int(parts[1].strip())
                        if time >= 356400000:
                            #print("DNF")
                            break
                        for group in group_strings:
                            if group in parts[0]:
                                if rainSetting == "dry":
                                    if "Dry" in parts[0]:
                                        #print(f"dry {group} {country}")
                                        country_total_time += time
                                        country_counts[country] += time
                                        country_stages[country] += 1
                                elif rainSetting == "wet":
                                    if "Wet" in parts[0]:
                                        #print(f"wet {group} {country}")
                                        country_total_time += time
                                        country_counts[country] += time
                                        country_stages[country] += 1
                                else:
                                    country_total_time += time
                                    country_counts[country] += time
                                    country_stages[country] += 1



except FileNotFoundError:
    print("ERROR: File not found")
    print("Leaderboards.txt needs to be in same directory as this script")
    exit()

#Group times
# print("Times Groups:")
output_array.append("Times Groups:")
for group, count in group_counts.items():
    milliseconds,seconds,minutes,hours,d = convert_hour_min(count)
    #print(f"{group:<8}\t {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
    output_array.append(f"{group:<8}\t {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
# print()
output_array.append("")

# print("Times Countries:")
output_array.append("Times Countries:")
for country, count in country_counts.items():
    milliseconds,seconds,minutes,hours,d = convert_hour_min(count)
    # print(f"{country:<8}\t {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
    output_array.append(f"{country:<8}\t {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
# print()
output_array.append("")

#Total stages
# print("Stages Groups:")
output_array.append("Stages Groups:")
stage_counter = 0
for group, count in group_stages.items():
    stage_counter += count
    # print(f"{group:<8}\t {count}")
    output_array.append(f"{group:<8}\t {count}")
# print()
output_array.append("")

# print("Stages Countries:")
output_array.append("Stages Countries:")
for country, count in country_stages.items():
    # print(f"{country:<8}\t {count}")
    output_array.append(f"{country:<8}\t {count}")
# print()
output_array.append("")

seconds, minutes, hours, days = convert(group_total_time)
ms,s,m,h,d = convert_hour_min(group_total_time)
# print("total time:")
# print(f"{d}:{h:02d}:{m:02d}:{s:02d}.{ms:03d}")
# print(f"{group_total_time} ms")
# print(f"{seconds:.2f} sec")
# print(f"{minutes:.2f} min")
# print(f"{hours:.2f} h")
# print(f"{days:.2f} days")
output_array.append("total time:")
output_array.append(f"{d}:{h:02d}:{m:02d}:{s:02d}.{ms:03d}")
output_array.append(f"{group_total_time} ms")
output_array.append(f"{seconds:.2f} sec")
output_array.append(f"{minutes:.2f} min")
output_array.append(f"{hours:.2f} h")
output_array.append(f"{days:.2f} days")
# print()
output_array.append("")
# print(f"DNFs: {dnf_count}")
output_array.append(f"DNFs: {dnf_count}")
max_stages = country_total * group_total
# print(f"total stages: {stage_counter} / {max_stages:.0f}")
output_array.append(f"total stages: {stage_counter} / {max_stages:.0f}")


if args.file:
    #Output to file
    with open("lb_output.txt", "a") as file:
        for line in output_array:
            print(line)
            file.write(f"{line}\n")
        
    print("File written")
    
else:
    #Print out all lines in output_array. In future convert this to use the options
    for line in output_array:
        print(line)

    
    

