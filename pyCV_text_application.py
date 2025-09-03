from pyCVdocx import *
from pyCVprofiles import *
import os

## this is a nightmare i should start over again or just use AI cause it is impossible to deal with this hahahahahaha
def clear():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def new_profile():
    print("WIP")
    input()

def print_section(title, section):
    s_type=section[0]
    print(f"Editing: {title} ({s_type} section)")
    if s_type == "NAME" or s_type == "PROFILE":
        print(f"{section[1]}")
        print("")
    elif s_type == "CONTACT":
        print("Contact info:")
        for i in section[1].keys():
            print(f"{i}: {section[1][i]}")
        print("")
    elif s_type != "WORK" and s_type!="EDUCATION":
        section_data=section[1]
        section_sets=section[2]
        for i in section_data.keys():
            print(f"{i}: {section_data[i]}")
        print("SETS:")
        for set_key in section_sets:
            print(f"set {set_key}")
            for item in section_sets[set_key]:
                print(f"{item}")
            print("")
    elif s_type == "WORK" or s_type == "EDUCATION":
        section_sets=section[1]
        print("SETS:")
        for set_key in section_sets:
            print(f"set {set_key}")
            for item in section_sets[set_key]:
                print(f"{item}")
            print("")
    print("======================================================================\n")

def get_set(profile,sec_select, set_type):
    sections=list(profile.keys())
    title=sections[int(sec_select)]
    match set_type:
        case "WORK": #for education and project / work sections
            projects=[]
            add_stuff=input("Add another project? (y/n)")
            while add_stuff == "y":
                clear()
                print_section(title,profile[sections[int(sec_select)]])
                title=input("type the title or position: ")
                time=input("type the length of the project/title (start date - end date or just a year): ")
                skills=input(" type the skills you used sepparated by commas (skill 1,skill 2): ")
                projects.append(f"{title}:{time}:{skills}")
                add_stuff=input("Add another project? (y/n)")
            profile=add_set(profile, sec_select, projects)
            
        case "EDUCATION":
            projects=[]
            add_stuff=input("Add another title? (y/n)")
            while add_stuff == "y":
                clear()
                print_section(title,profile[sections[int(sec_select)]])
                title=input("type the title: ")
                time=input("type the length time (start date - end date or just the year of completion): ")
                skills=input("type the school or institution: ")
                projects.append(f"{title}:{time}:{skills}")
                add_stuff=input("Add another title? (y/n)")
            profile=add_set(profile, sec_select, projects)

        case "LIST":
            if profile[sections[int(sec_select)]][1]["type"]=="names":
                items=[]
                add_stuff=input("Add another item (y/n)")
                while add_stuff == "y":
                    clear()
                    print_section(title,profile[sections[int(sec_select)]])
                    item_name = input("type the name of the item: ")
                    item=input("type the item: ")
                    items.append(f"{item_name}:{item}")

                    add_stuff=input("Add another item? (y/n)")
                profile=add_set(profile, sec_select, items)


            else:  
                items=[]
                add_stuff=input("Add another item (y/n)")
                while add_stuff == "y":
                    clear()
                    print_section(title,profile[sections[int(sec_select)]])
                    item=input("type the item: ")
                    items.append(item)
                    add_stuff=input("Add another item? (y/n)")
                profile=add_set(profile, sec_select, items)

        case "TEXT":
            clear()
            print_section(title,profile[sections[int(sec_select)]])
            text=[input("type in the text for your section: ")]
            profile=add_set(profile, sec_select, text)

    return profile

def add_set(profile,sec_select,new_set):
    sections=list(profile.keys())
    title=sections[int(sec_select)]
    profile[sections[int(sec_select)]][-1][str(1+len(profile[sections[int(sec_select)]][-1].keys()))]=new_set
    return profile

def del_set(profile,sec_select,set_to_delete:int):
    sections=list(profile.keys())
    title=sections[int(sec_select)]
    sets=profile[sections[int(sec_select)]][-1]
    sets.pop(str(set_to_delete))
    new_sets={}
    for i in range(len(sets.keys())):
        new_sets[str(i+1)]=sets[list(sets.keys())[i]]
    profile[sections[int(sec_select)]][-1]=new_sets
    return profile

def add_section(profile):
    section_types=["TEXT","WORK","LIST"]
    wrong_sec_type=True
    while wrong_sec_type:
        clear()
        print("What type of section is your new section?\n0: Text\n1: Projects/Work\n2: List")
        sec_type=input()
        if sec_type in list(map(str, range(len(section_types)))):
            wrong_sec_type=False
    clear()
    match section_types[int(sec_type)]:
        case "TEXT":
            print("=writing Text section=")
            print("Choose a text section type\n0: plain (default)\n1: cv summary/objective")
            text_section_type_selection=input()
            if text_section_type_selection=="1":
                text_section_type="summary"
            else:
                text_section_type="plain"
            title=input("type the title of your section: ")
            profile[title]=["TEXT",{'type': text_section_type},{}]
            profile=get_set(profile,str(len(profile)-1),section_types[int(sec_type)])

        case "WORK":
            print("=writing Work/Projects section=")
            title=input("type the title of your section: ")
            profile[title]=["WORK",{}]
            profile=get_set(profile,str(len(profile)-1),section_types[int(sec_type)])

        case "LIST":
            print("=writing List section=")
            print("Choose a list section type\n0: bullets(default)\n1: numbers\n2: names\n3: plain")
            list_type_selection=input()
            if list_type_selection=="1":
                list_type="numbers"
            elif list_type_selection=="2":
                list_type="names"
            elif list_type_selection=="3":
                list_type="plain"
            else:
                list_type="bullets"
            title=input("type the title of your section: ")
            profile[title]=["LIST",{"type":list_type},{}]
            profile=get_set(profile,str(len(profile)-1),section_types[int(sec_type)])
    
    return profile

def del_section(profile,section):
    profile.pop(section)
    return profile

def print_profile(profile):
    sections=list(profile.keys())
    profile_name=profile["Profile"][1]["profile"]
    print("======================================================================\n")
    print(f"Profile name: {profile_name}\n")
    print(f"Name: {profile["Name"][1]["name"]}\n")
    print("Contact info:")
    for i in profile["Contact"][1].keys():
        print(f"{i}: {profile["Contact"][1][i]}")
    print("")
    for section in sections[3:]:
        section_info_array=profile[section]
        section_type=section_info_array[0]
        if section_type != "WORK" and section_type!="EDUCATION":
            section_data=section_info_array[1]
            section_sets=section_info_array[2]
            print(f"{section_type}: {section}")
            for i in section_data.keys():
                print(f"{i}: {section_data[i]}")
            print("SETS:")
            for set_key in section_sets:
                print(f"set {set_key}")
                for item in section_sets[set_key]:
                    if len(item) >70:
                        print(item[0:66]+"...")
                    else:
                        print(f"{item}")
                print("")
        else:
            section_sets=section_info_array[1]
            print(f"{section_type}: {section}")
            print("SETS:")
            for set_key in section_sets:
                print(f"set {set_key}")
                for item in section_sets[set_key]:
                    if len(item) >70:
                        print(item[0:66]+"...")
                    else:
                        print(f"{item}")
                print("")
    print("======================================================================\n")

def print_sections(profile):
    sections=list(profile.keys())
    for i in range(len(sections)):
        print(f"{i}: {sections[i]} ({profile[sections[i]][0]})")

def handle_section_to_write(section, title,set_selections):
    section_type=section[0]
    match section_type:
        case "TEXT":
            text=query_text_sets(section,title)
            print(text)
            text_section(text,section[1],title)
        case "WORK":
            pass
        case "EDUCATION":
            pass
        case "LIST":
            pass

def query_text_sets(section, title):
    sets=section[-1]
    clear()
    print("=== CREATING CV ===")
    print(f"== {section[0].capitalize()} section ==")
    print(f"= Title: {title} =")
    for text_set in sets:
        print(f"Set {text_set}:")
        print(section[-1][text_set])
    selected_set=input("type in the number of the set you want to use: ")
    if selected_set not in list(sets.keys()):
        text=query_text_sets(section,title)
    else:
        text = str(section[-1][selected_set][0])

    return text

def main():
    exit_app=False
    state="select profile"
    clear()
    print("""
                                                                            
* =*.=:##-.-+     #          -#-        :%:=:-@:      :=           @--                 
.          @=@    :%-       *.+      .+-         =-   ##:          :=                  
#          #+     =@#     .#=      #@           @*    +#+         #.                  
%.          +=      #*=   @+       : =                  .%       =*@                   
*+        : %          *% *         #                    +.      .+                    
%#-.@@#=:#:            =.@         -@:                   %.@    -:                     
:+                     *.          +=#           ::        *   .=:                     
*:                     #+           +-*         %@.        =-  @=                      
@*                     ==            :@#-     ==*=          :+@-                       
.*                     =.                +*= *-             %=.                        
                                    
    """)
    # ===================== profile selection
    print("Welcome to PyCV 0.1\n")
    while not exit_app:
        match state:
            case "select profile":

                selected_profile=""
                profiles = find_profiles()
                wrong_selection = False
                if profiles:
                    profile_idxs=list(range(len(profiles)))
                    profile_menu_options=profile_idxs+[profile_idxs[-1]+1]
                    while selected_profile not in list(map(str, profile_menu_options)):
                        if wrong_selection:
                            clear()
                            print("Please select an existing option (type only the number):")
                        else:
                            print("Select a profile:")
                        for i in profile_idxs:
                            print(f"{i}: {profiles[i]}")
                        print(f"{i+1}: Create new profile")
                        selected_profile=input()
                        wrong_selection=True
                else:
                    print("No profiles were found")
                    input("Press enter to create a profile")
                    selected_profile=1
                state="handle profile selection"

            case "handle profile selection":
                clear()
                selected_profile=int(selected_profile)
                if selected_profile>len(profiles)-1:
                    print("creating new profile")
                    state="create new profile"
                else:
                    profile=read_profile(profiles[int(selected_profile)])
                    print(f"The selected profile is: {profiles[int(selected_profile)]}\n")
                    print("it contains the following data:\n")
                    print_profile(profile)
                    state="idk"
                    if input("Confirm selected profile? (y/n)").lower()=="y":
                        clear()
                        state="action menu"
                    else:
                        clear()
                        state="select profile"
                        
            case "create new profile":
                new_profile()
                state="meh"
            
            case "action menu":

                clear()
                actions=["view profile data","edit profile","save profile","select another profile","create CV","exit"]
                print("=== Action Menu ===")
                print("what do you want to do? (Type only the number)")
                for idx in range(len(actions)):
                    print(f"{idx}: {actions[idx]}")
                selected_action=input()
                match selected_action:
                    case "0":
                        state=actions[0]
                    case "1":
                        state=actions[1]
                    case "2":
                        state=actions[2]
                    case "3":
                        clear()
                        state="select profile"
                    case "4":
                        state=actions[4]
                    case "5":
                        state=actions[5]
                    case _:
                        state="action menu"

            case "view profile data":
                clear()
                print_profile(profile)
                input("press enter to go back to action menu: ")
                state="action menu"
            
            case "edit profile":
                clear()
                p_edit_actions=["edit section","add section","remove section", "go back"]
                print_profile(profile)
                print("=== Edit Profile Menu ===")
                print("what do you want to do?")
                for i in range(len(p_edit_actions)):
                    print(f"{i}: {p_edit_actions[i]}")
                selected_action=input()
                if selected_action not in list(map(str, range(len(p_edit_actions)))):
                    if int(selected_action) == len(p_edit_actions):
                        action="go back"
                    else:
                        action="xd"
                else:
                    action=p_edit_actions[int(selected_action)]
                match action:
                    case "edit section":
                        state="edit section"
                    case "go back":
                        state="action menu"
                    case "remove section":
                        state="remove section menu"
                    case "add section":
                        state="add section menu"
                    case _:
                        state="edit profile"

            case "edit section":
                sections=list(profile.keys())
                clear()
                print("Which section do you want to edit?\n")
                print_sections(profile)
                print(f"{len(sections)}: go back")
                sec_select=input()
                if sec_select in list(map(str,range(len(sections)))):
                    #=========editing menu
                    clear()
                    title= sections[int(sec_select)]
                    print_section(title,profile[sections[int(sec_select)]])
                    if profile[sections[int(sec_select)]][0]== "NAME" or profile[sections[int(sec_select)]][0]== "PROFILE" or profile[sections[int(sec_select)]][0]== "CONTACT":
                        ###################TODO add way to edit these sections
                        print("wip")
                        input("press enter to go back")
                    else:
                        print("0: add set\n1: delete set\n2: go back")
                        add_or_back=input()
                        if add_or_back=="0":
                            clear()
                            print_section(title,profile[sections[int(sec_select)]])
                            profile=get_set(profile,sec_select,profile[sections[int(sec_select)]][0])
                        elif add_or_back=="1":
                            clear()
                            print_section(title,profile[sections[int(sec_select)]])
                            set_select=input("Which set would you like to delete? ")
                            if set_select in list(profile[sections[int(sec_select)]][-1].keys()):
                                profile=del_set(profile,sec_select,int(set_select))

                elif int(sec_select) == len(sections):
                    state="edit profile"
            
            case "add section menu":
                profile=add_section(profile)
                state="edit profile"

            case "remove section menu":
                sections=list(profile.keys())
                delete_not_allowed=["0","1","2"]
                clear()
                print("Which section do you want to delete?\n")
                print_sections(profile)
                print(f"{len(sections)}: go back")
                sec_select=input()
                if sec_select in list(map(str,range(len(sections)))) and sec_select not in delete_not_allowed:
                    section_to_delete=sections[int(sec_select)]
                    if input(f"Are you sure you want to delete{section_to_delete}? (y/n)")=="y":
                        profile=del_section(profile, section_to_delete)
                        state="edit profile"
                elif sec_select==str(len(sections)):
                    state="edit profile"
            
            case "save profile":
                clear()
                print("=Profile saving menu=")
                print("how would you like to save the current profile?\n0: save with current name\n1: save with new name\n2: go back")
                how_to_save=input()
                if how_to_save == "0":
                    write_profile(profile)
                    input(f"profile saved to {profile["Profile"][1]["profile"]} press enter to goo back")
                    state="action menu"
                elif how_to_save =="1":
                    invalid_chars = '<>:"/\\|?*'
                    new_profile_name=input("type the the name for your new profile: ")
                    clean_profile_name=''.join(c for c in new_profile_name if c not in invalid_chars)
                    profile["Profile"][1]["profile"]=clean_profile_name
                    write_profile(profile)
                    input(f"profile saved to {profile["Profile"][1]["profile"]} press enter to goo back")
                    state="action menu"
                elif how_to_save == "2":
                    state="action menu"
                
            case "create CV":
                set_selections={}
                selections={}
                sections=list(profile.keys())[3:]
                clear()
                print("=== CREATING CV ===")
                doc_style()

                print("== Contact section ==")
                contact_to_write=profile["Contact"][1]
                # wtf_python=list(profile["Contact"][1].keys())
                for i in list(contact_to_write.keys()):
                    include_contact_item=input(f"do you want to include your {i}? y/n (no is default)")
                    if include_contact_item != "y":
                        contact_to_write.pop(i)
                print("")
                profile_with_selected_contact=profile
                profile_with_selected_contact["Contact"]=contact_to_write

                for section in sections:
                    print(f"xd {section}")
                    handle_section_to_write(profile[section],section,set_selections)
                    print("")
                    input()
                
            case _:
                exit_app=True


        
if __name__ == '__main__':
    main()