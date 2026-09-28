from usefulFunctions import play_melody_audio
import numpy as np
import sounddevice as sd

# getting piano key data from file
def piano_keys_data(file)->(list,list,list):
    piano_index_list = []
    piano_note_list = []
    piano_hz_list = []
    # opening file data, spliting contents and appending to lists
    with open(file, 'r') as piano_directory:
        for line in piano_directory:
            line_data = (line.strip()).split(",")
            piano_index = line_data[0]
            piano_note = line_data[1]
            piano_hz = line_data[2]
            piano_index_list.append(piano_index)
            piano_note_list.append(piano_note)
            piano_hz_list.append(piano_hz)
        return piano_index_list,piano_note_list,piano_hz_list

# getting melody data from file
def melody_data(file)->(list,list):
    melody_name_list = []
    melody_list = []
    # appending file contents to lists
    with open(file, 'r') as melody_directory:
        for line in melody_directory:
           line_data = (line.strip()).split(",")
           melody_name = line_data[0]
           melody = line_data[1]
           melody_name_list.append(melody_name)
           melody_list.append(melody)
        return melody_name_list,melody_list

# to print a menu display of options
def menu_display():
    divider = "=" * 30
    print(f"Menu Options\n {divider}\n 1: Play a saved melody\n 2: Write and save a new melody\n 3: Edit a saved melody\n 4: Delete a saved melody\n 5: Quit")
    picked_option = int(input("use numbers to pick your option: "))
    return picked_option

# converting notes to frequencies
def notes_to_freq(note_sequence, note_list, hz_list):
    freq_sequence = []
    for note in note_sequence:
        if note in note_list:
            index = note_list.index(note)
            freq_sequence.append(float(hz_list[index]))
        else:
            print(f"Note {note} not found.")
    return freq_sequence

# option 1: playing a melody already saved in a list
def play_saved_melody(melody_name_list, melody_list, piano_note_list, piano_hz_list):
    # presenting already existing melodies
    print("\nAvailable Melodies:")
    for name in melody_name_list:
        print(f"- {name}")
    # user chooses melody
    choice = input("Enter the name of the melody you want to play: ")
    if choice in melody_name_list:
        index = melody_name_list.index(choice)
        notes = melody_list[index].split("-")
        freq = notes_to_freq(notes, piano_note_list, piano_hz_list)
        # plays melody from 'usefulFunctions.py'
        play_melody_audio(freq)
        print(f"playing: {choice}")
    else:
        print("Melody not found.")

# option 2: add and save a new melody
def add_new_melody(melody_name_list, melody_list, piano_note_list,):
    print("\nAdding New Melodies:")
    new_name = input("enter a name for the new melody: ")
    if new_name in melody_name_list:
        print("There is a melody already with that name!")
    elif new_name == "":
        print("you need to enter a name to proceed!")
    else:
        make_new_melody = input(f"produce a new melody for {new_name} (e.g., E4-C4-E4): ")
        melody_notes = make_new_melody.split("-")
        # validating note
        for note in melody_notes:
            if note not in piano_note_list:
                print(f"\n{note} note is invalid")
                return
        # save to file
        with open("melodies_data.txt", "a") as file1:
            file1.write(f"{new_name},{make_new_melody}\n")
        melody_name_list.append(new_name)
        melody_list.append(make_new_melody)
        print(f"\n{new_name} is successfully saved!")

# option 3: edit an existing melody
def edit_melody(melody_name_list, melody_list, piano_note_list):
    print("\nEdit a Saved Melody")
    print("Available Melodies:")
    for name in melody_name_list:
        print(f"- {name}")
    # user selects melody name
    selected_name = input("Enter the name of the melody you want to edit: ")
    if selected_name not in melody_name_list:
        print(f"\n{selected_name} does not exist!")
        return
    # getting and splitting melody notes
    index = melody_name_list.index(selected_name)
    note_sequence = melody_list[index].split("-")
    # display edit options
    while True:
        print("\nEdit Options:\n1. Replace a note (all occurrences)\n2. Replace a note by position\n3. Delete a note (all occurrences)\n4. Delete a note by position\n5. Return to main menu")
        choice = int(input("\nChoose an edit option (1-5): "))

        # edit 1: replace all occurrences of a note
        if choice == 1:
            print(f"{melody_list[index]}")
            # finding notes to replace
            old_note = input("Enter the note to replace: ").strip().upper()
            new_note = input("Enter the new note: ").strip().upper()
            if old_note not in note_sequence:
                print(f"'{old_note}' was not found in the melody.")
            elif new_note not in piano_note_list:
                print(f"'{new_note}' is not a valid note.")
            else:
                # replacing of the notes
                for i in range(len(note_sequence)):
                    if note_sequence[i] == old_note:
                        note_sequence[i] = new_note
                print("Notes replaced successfully.")

        # edit 2: replace a note by position
        elif choice == 2:
            print(f"{melody_list[index]}")
            # finding position
            position = int(input(f"Enter the position (1 to {len(note_sequence)}): ")) - 1
            if 0 <= position < len(note_sequence):
                new_note = input("Enter the new note: ").strip().upper()
                # replacing the note
                if new_note in piano_note_list:
                    note_sequence[position] = new_note
                    print(f"Note '{new_note}' replaced at position {position}.")
                else:
                    print(f" note '{new_note}' is invalid.")
            else:
                print(f"{position} is out of range (1 to {len(note_sequence)}.")

        # delete all occurrences of a note
        elif choice == 3:
            print(f"{melody_list[index]}")
            #finding note to be deleted
            del_note = input("Enter the note to delete: ").strip().upper()
            if del_note not in note_sequence:
                print(f"Note '{del_note}' not found in melody.")
            else:
                # deleting and updating melody
                updated_sequence = []
                for note in note_sequence:
                    if note != del_note:
                        updated_sequence.append(note)
                note_sequence = updated_sequence
                print(f"Notes '{del_note}' successfully deleted.")

        # edit 4: delete note by position
        elif choice == 4:
            print(f"{melody_list[index]}")
            # finding position to pop the note
            position1 = int(input(f"Enter the position to delete (1 to {len(note_sequence)}): ")) - 1
            if 0 <= position1 < len(note_sequence):
                note_deleted = note_sequence.pop(position1)
                print(f"Note '{note_deleted}' deleted from position {position1}.")
            else:
                print(f"Position {position1} is out of range (1 to {len(note_sequence)}).")

        # return to main menu
        elif choice == 5:
            break

        else:
            print("Invalid choice. Try again.")

        # returning and linking up the melodies
        edited_sequence = "-".join(note_sequence)
        melody_list[index] = edited_sequence
        # updating files with new saved edits
        with open("melodies_data.txt", "w") as file2:
            for name, notes in zip(melody_name_list, melody_list):
                file2.write(f"{name},{notes}\n")
        print(f"Melody '{selected_name}' updated and saved.")

# option 4: delete an existing melody
def delete_melody(melody_name_list, melody_list):
    print("\nDelete a Saved Melody")
    # if no melodies available
    if not melody_name_list:
        print("No melodies are available.")

    print("Available Melodies:")
    for name in melody_name_list:
        print(f"- {name}")
    # finding melody to delete
    melody_for_del = input("Enter the name of the melody you want to delete: ").strip()
    if melody_for_del not in melody_name_list:
        print(f"{melody_for_del} is not a saved melody.")
        return
    # deleting melody
    delete_index = melody_name_list.index(melody_for_del)
    del melody_name_list[delete_index]
    del melody_list[delete_index]
    # updating file with deleted melody
    with open("melodies_data.txt", "w") as file3:
        for name,notes in zip(melody_name_list,melody_list):
            file3.write(f"{name},{notes}\n")
    print(f"'{melody_for_del}' has been successfully deleted!")

def main():
    # loading data for files
    piano_index_list,piano_note_list,piano_hz_list = piano_keys_data('piano_keys.txt')
    melody_name_list,melody_list = melody_data('melodies_data.txt')

    # options from menu_display()
    while True:
        picked_option = menu_display()

        if picked_option == 1:
            play_saved_melody(melody_name_list, melody_list, piano_note_list, piano_hz_list)
        elif picked_option == 2:
            add_new_melody(melody_name_list, melody_list, piano_note_list)
        elif picked_option == 3:
            edit_melody(melody_name_list, melody_list, piano_note_list)
        elif picked_option == 4:
            delete_melody(melody_name_list, melody_list)
        elif picked_option == 5:
            break
        else:
            print("not an option!")
main()