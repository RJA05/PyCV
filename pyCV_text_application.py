from pyCVdocx import *
from pyCVprofiles import *
import os


def clear():
    command = 'cls' if os.name == 'nt' else 'clear'
    os.system(command)

def new_profile():
    ...
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
                    input()
                elif int(sec_select) == len(sections):
                    state="edit profile"
            case _:
                exit_app=True


        
if __name__ == '__main__':
    main()