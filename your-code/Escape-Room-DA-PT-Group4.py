#LIBRARIES:
###########
import webbrowser
from IPython.display import Image

# define rooms and items

# DOORS:#
#########
door_a = {
    "name": "door a",
    "type": "door",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

door_d = {
    "name": "door d",
    "type": "door",
}

# KEYS:#
########
key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

# FURNITURES:#
##############
couch = {
    "name": "couch",
    "type": "furniture",
}

piano = {
    "name": "piano",
    "type": "furniture",
}

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}
  
dresser = {
    "name": "dresser",
    "type": "furniture",
}

dining_table = {
    "name": "dining table",
    "type": "furniture",
}


# ROOMS:#
#########
game_room = {
    "name": "game room",
    "type": "room",
    "image": "Gameroom_picture.jpeg"
}

bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
    "image": "Bedroom1_picture.jpeg"
}

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
    "image": "Bedroom2_picture.jpeg"
}

living_room = {
    "name": "living room",
    "type": "room",
    "image": "Livingroom_picture.jpeg"
}

outside = {
  "name": "outside"
}

#all_rooms = [game_room, outside]
all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

#all_doors = [door_a]
all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related
object_relations = {
    #GameRoom:
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "door a": [game_room, bedroom_1],
    #Bedroom1:
    "bedroom 1": [queen_bed, door_a, door_b, door_c],
    "queen bed": [key_b],
    "door b": [bedroom_1, bedroom_2],
    #Bedroom2:
    "bedroom 2": [double_bed, dresser, door_b],
    "double bed": [key_c],
    "dresser": [key_d],
    #Livingroom:
    "living room": [dining_table, door_c, door_d],
    "dining table": [], #There is no key on the table. Not sure if we have to change this.
    "door c": [bedroom_1, living_room],
    "door d": [living_room, outside],
    #Outside:
    "outside": [door_d]
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")

    open_webbrowser("https://youtu.be/PkSwcpGqk5I",2, True)
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
        open_webbrowser("https://tenor.com/es/ver/winner-gif-13816408",0, True)
    else:
        print("You are now in " + room["name"])
        
        #For input to 1=explore or 2=examine:
        while True:
            try:
                intended_action = int(input("What would you like to do? Type 1 for explore or 2 for examine?"))
                break
            except:
                print("That's not a valid option!")
                
        if intended_action == 1: #explore
            explore_room(room)
            play_room(room)
        elif intended_action == 2:#examine
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 1 for explore or 2 for examine.")
            play_room(room)
            
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
        
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

    show_room_image(room)

     
def show_room_image(room):
    """
    Function to open images from .\Img\ folder
    """
    path = ".\Img\\" + room["image"]
    display(Image(filename = path, width=300, height=300)) 
        

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
    
    if(next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)
        
#Function to open a webbrowser:
def open_webbrowser(link_video,new_value, autoraise_value):
    try:
        webbrowser.open(link_video, new=new_value, autoraise=autoraise_value)
    except:
        print('Web browser failed to open, so I will sing for you instead ♩ ♪ ♫ ♬ ♩ ♪ ♫ ♬')

game_state = INIT_GAME_STATE.copy()

start_game()