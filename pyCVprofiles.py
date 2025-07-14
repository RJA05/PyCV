from pyCVdocx import *
##TODO THIS ENTIRE SCRIPT SHOULD BE REPLACED WITH BETTER CODE :)
## CHANGES SHOULD INCLUDE:
## JSON profile formatting instead of this made up nightmare since it would be easier to handle for other users and would elimnate the requierement of using custom file writing and reading functions which are kind of a mess rn
## create profiles as a class and dynamically add, remove and edit the section objects within that class to simplify profile data access instead of this indexing nightmare implemented with a dictionary which could be usefull for JSON formatting but nah id rather make a function to convert the profile class to a dict then save it as a JSON file

## This should make it easier to implement a GUI

def find_profiles()-> list:
    profiles:list[str]=[]
    with os.scandir() as entries:
        for entry in entries:
            if entry.is_file() and ".pyCV-profile" in entry.name:  # Check if it's a file
                profiles.append(entry.name)
    return profiles

def read_profile(filename:str)-> dict:#{"title": [ type,["content line 1", "content line 2", ...],{"set 1": [1,2,3], "set 2":"bla bla bla", ...}] }
    # the dict of the entire return has the following structure {"title": [ type,["content line 1", "content line 2", ...],{"set 1": [1,2,3], "set 2":"bla bla bla", ...}] }
    section_type:str=None
    section_title:str=None
    read_state:str=None
    profile:dict={}
    start_set:bool=False
    set_num=1
    with open(filename,"rt") as data_file:
        for line in data_file:
            if "$$" in line:
                read_state="title"
                section_type=line[3:-1]
            elif "title:" in line and read_state=="title":
                section_title=line[6:-1]
                profile[section_title]=[section_type]
                read_state="info"
            elif line=="\n":
                read_state=None
            elif "##" in line:
                read_state="sets"
                profile[section_title].append({})
            elif read_state=="sets":
                if "set:" in line:
                    set_num=line[-2]
                    profile[section_title][-1][set_num]=[]
                elif "{" in line:
                    start_set=True
                elif"}"in line:
                    start_set=False
                else:
                    profile[section_title][-1][set_num].append(line[:-1])
            elif read_state=="info" and "##"not in line:
                if ("title" not in line) and ("## SETS" not in line):
                    if len(profile[section_title])<2:
                        profile[section_title].append({})
                    data=line.split(":")
                    profile[section_title][1][data[0]]=data[1][:-1]
    return profile

def write_profile(profile:dict):
    sections=list(profile.keys())
    profile_name=profile["Profile"][1]["profile"]
    with open(profile_name+".pyCV-profile","w") as file:
        file.write("pyCV profile")
    with open(profile_name+".pyCV-profile", "a") as file:
        file.write(f"\n$$ PROFILE\ntitle:Profile\nprofile:{profile_name}\n")
        file.write(f"\n$$ NAME\ntitle:Name\nname:{profile["Name"][1]["name"]}\n")
        file.write("\n$$ CONTACT\ntitle:Contact\n")
        for i in profile["Contact"][1].keys():
            file.write(f"{i}:{profile["Contact"][1][i]}\n")
        file.write("\n")
        for section in sections[3:]:
            section_info_array=profile[section]
            section_type=section_info_array[0]
            if section_type != "WORK" and section_type!="EDUCATION":
                section_data=section_info_array[1]
                section_sets=section_info_array[2]
                file.write(f"$$ {section_type}\n")
                file.write(f"title:{section}\n")
                for i in section_data.keys():
                    file.write(f"{i}:{section_data[i]}\n")
                file.write("## SETS\n")
                for set_key in section_sets:
                    file.write(f"set:{set_key}\n")
                    file.write("{\n")
                    for item in section_sets[set_key]:
                        file.write(f"{item}\n")
                    file.write("}\n")
            else:
                section_sets=section_info_array[1]
                file.write(f"$$ {section_type}\n")
                file.write(f"title:{section}\n")
                file.write("## SETS\n")
                for set_key in section_sets:
                    file.write(f"set:{set_key}\n")
                    file.write("{\n")
                    for item in section_sets[set_key]:
                        file.write(f"{item}\n")
                    file.write("}\n")
            file.write("\n")
