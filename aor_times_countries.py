# The file "Leaderboards.txt" must be located in the same directory in which the script is executed.
#
# daily/weekly events are excluded
#
# made by FailX and MxCraven

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
     return ms,s,m,h
 
def convert_total_time(milliseconds):
    # converts to hour:min format
     ms=int(milliseconds)%1000
     s=int(milliseconds/1000)%60
     m=int(milliseconds/(1000*60))%60
     h=int(milliseconds/(1000*60*60))%24
     d=int(milliseconds/(1000*60*60*24))
     return ms,s,m,h,d


# init hashmap
group_total_time = 0
group_strings = ["60s","70s","80s","GroupB","GroupS","GroupA","Logging","Vans","Dakar","Monkey"]
group_counts = {string: 0 for string in group_strings}
group_stages = {string: 0 for string in group_strings}

country_total_time = 0
country_strings = ["Finland", "Sardinia", "Japan", "Norway", "Germany", "Kenya", "Indonesia", "Australia"]
country_counts = {string: 0 for string in country_strings}
country_stages = {string: 0 for string in country_strings}

try:
    with open("Leaderboards.txt", "r") as file:
        for line in file:
            parts = line.split(":")
            if len(parts) >= 3: # kind off pointless if the file hasn't changed
                #Groups
                for string in group_strings:
                    if string in parts[0]:
                       time = int(parts[1].strip())
                       if time >= 356400000:
                            #print("DNF")
                            break
                       group_total_time += time
                       group_counts[string] += time
                       group_stages[string] += 1 

                #Countries
                for string in country_strings:
                    if string in parts[0]:
                        time = int(parts[1].strip())
                        if time >= 356400000:
                            #print("DNF")
                            break
                        country_total_time += time
                        country_counts[string] += time
                        country_stages[string] += 1

except FileNotFoundError:
    print("ERROR: File not found")
    print("Leaderboards.txt needs to be in same directory as this script")
    exit()


#Group times
print("Times Groups:")
for group, count in group_counts.items():
    milliseconds,seconds,minutes,hours = convert_hour_min(count)
    print(f"{group:<8}\t {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
print()

print("Times Countries:")
for country, count in country_counts.items():
    milliseconds,seconds,minutes,hours = convert_hour_min(count)
    print(f"{country:<8}\t {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}")
print()

#Total stages
print("Stages Groups:")
counter = 0
for group, count in group_stages.items():
    counter += count
    print(f"{group:<8}\t {count}")
print()

print("Stages Countries:")
for country, count in country_stages.items():
    print(f"{country:<8}\t {count}")
print()

seconds, minutes, hours, days = convert(group_total_time)
ms,s,m,h,d = convert_total_time(group_total_time)
print("total time:")
print(f"{d}:{h:02d}:{m:02d}:{s:02d}.{ms:03d}")
print(f"{group_total_time} ms")
print(f"{seconds:.2f} sec")
print(f"{minutes:.2f} min")
print(f"{hours:.2f} h")
print(f"{days:.2f} days\n")
print(f"total stages: {counter}")
