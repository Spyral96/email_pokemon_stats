# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 22:22:13 2023

@author: Dan
"""
#imports including pokemon desciption function
import random
import requests
from win10toast import ToastNotifier
import smtplib
from email.message import EmailMessage
import os
import pandas as pd


###############making txt file for debugger

directory = "C:/Users/Dan/Desktop/Python Files/Debugging txt files"

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)
    
file_path = os.path.join(directory, "Debugger.txt")
 
with open(file_path,'a') as Debuggerpoke:    
    
    Debuggerpoke.write("First gate \n")



    #making random dex number to add to the end of api url
    random_dex_num = str(random.randint(1,1008))
    
    url = f"https://pokeapi.co/api/v2/pokemon/{random_dex_num}" 
    
    
    response = requests.get(url)
    
    pokemon_raw_data = response.json()
    
    
    #######
    
    
    ########   Variables      #######
    
    base_hp = pokemon_raw_data['stats'][0]["base_stat"]
    
    base_att = pokemon_raw_data['stats'][1]["base_stat"]
    
    base_def = pokemon_raw_data['stats'][2]["base_stat"]
    
    base_spa = pokemon_raw_data['stats'][3]["base_stat"]
    
    base_spd = pokemon_raw_data['stats'][4]["base_stat"]
    
    base_speed = pokemon_raw_data['stats'][5]["base_stat"]
    
    poke_name = pokemon_raw_data ["name"]
    
    type_uncleaned_data = pokemon_raw_data['types'][0:]
    
    type_names = []
    #adding stats for base stat total
    bst = base_hp + base_att + base_def + base_spa + base_spd + base_speed 
    
    dex_num = pokemon_raw_data['id']
    
    #second debug trigger
    Debuggerpoke.write('Second Gate \n')
        
        
    ###### pokemon"s type(s) for loop
    for entry in type_uncleaned_data:
        type_name = entry['type']['name']
        type_names.append(type_name)
    
    #creating intail blank move list to soon be appended
    movesets = []
    
    #creating specific data location for moveset
    raw_moveset = pokemon_raw_data['moves'] 
    
    #looping through moveset and appending to movesets list
    for dictionary in raw_moveset:
        moveset = dictionary['move']['name']
        movesets.append(moveset)
    
    
    
    ########fetching specific move descriptions################ 
    #creating url list for all moves (Linking to a different apis)
    moves_list_url=[]
    
    #looping through each dictionary that each row contains the api urls
    for dictionary in raw_moveset: 
        moveset_url = dictionary['move']['url']
        #appending to move_list_url
        moves_list_url.append(moveset_url)
    
    
    #looping each url to be insert in requesting
    #making json list for each of the urls moves_list_url
    move_description = []
    for url in moves_list_url:
             second_respnse = requests.get(url)
             pokemon_moveset_specific_data = second_respnse.json()
             move_description.append(pokemon_moveset_specific_data)
             
    #just made the a list for each moves' attrabutes          
    
    #debug checkpoint    
    Debuggerpoke.write("Third Gate \n")
      
    
    #fetching our values from multiple json dictionaries (move_description)
    #making list for each 
    
    move_power = []
    move_accuracy = []
    effect_entry = []
    move_type = []
    damage_type = []
    
    
    #looping through dictionries json values and adding DERSIRED values to blank lists
    for move_desc in move_description:
        damage_type.append(move_desc['damage_class']['name'])
        move_type.append(move_desc['type']['name'])
        
        #if move's entry is left blank
        effect_entries = move_desc['effect_entries']
        if effect_entries:
            effect_entry.append(effect_entries[0]['short_effect'])
        else:
            effect_entry.append("N/A")
        
        
        #if power has no value!
        if move_desc['power'] is None:
            move_desc['power'] = "N/A"
            move_power.append(move_desc['power'])
        else:
            move_power.append(move_desc['power'])
            
        #if accuracy has no value
        if move_desc['accuracy'] is None:
            move_desc['accuracy'] = "N/A"
            move_accuracy.append(move_desc['accuracy'])
        
        else:
            move_accuracy.append(move_desc['accuracy'])
    
    #debug checkpoint
    Debuggerpoke.write("Fourth Gate \n")
    
    #making a dictionary with the values(lists(line 95-99)) i want to turn it into pandas data frame
    
    move_detail_dict = {'moveset': movesets,
                        'move_types': move_type,        
                        'move_powers':move_power,
                        'move_accuracys':move_accuracy,
                        'effect_entrys': effect_entry,                            
                        'damage_types':damage_type
    }
    
    
    #our pandas dataframe (6 rows)
    move_df = pd.DataFrame(move_detail_dict,columns= ['moveset','move_types','move_powers','move_accuracys','effect_entrys','damage_types'])
    
    #debug checkpoint
    Debuggerpoke.write('5th Gate \n')
    
    
    #creating ,txt file  (To use for the email and notifaction)
    with open('Pokemon Daily Update.txt', 'w') as file:
        # Write the content to the file
        
        file.write(poke_name.title())
        file.write("\n")
        for x in type_names:
            file.write("Type: " + x.title())
        file.write("\n")
        file.write(f"Pokedex Number: {dex_num}")
        file.write(f'\nBase Stats:\nHP: {base_hp}\nAttack: {base_att}\nDefense: {base_def}\nSpeaial Attack: {base_spa}\nSpecial Defense: {base_spd}\nSpeed: {base_speed}')
        
        file.write('\n')
        file.write("Moveset:\n")
        file.write('\n')
        for move,typing,power,acc,entry,dam_type  in zip(move_df['moveset'],move_df['move_types'],move_df['move_powers'],move_df['move_accuracys'],move_df['effect_entrys'],move_df['damage_types']):
            file.write(f'{move.title()}\n Type: {typing.title()}\n Power: {power}\n Accuracy: {acc}\n Damage Type: {dam_type.title()}\n Description: {entry} \n \n')
    
    #debug checkpoint
    Debuggerpoke.write("Sixth Gate \n")
        
    #reading text file (turning our file into a varaible we can use)
    with open('Pokemon Daily Update.txt', 'r') as file:
        notification_message = file.read()
    
    #############notifcation###############
    
    poke_notif = ToastNotifier()
    # #displaying notication
    poke_notif.show_toast("Daily Pokemon Stats",notification_message,duration=11)
    
    ###########Emailing The Stats
    
    message = EmailMessage()
    message['From'] = 'your email'
    message['To'] = 'send to email'
    message['Subject'] = 'Pokemon Daily Stats'
    message.set_content(str(notification_message))
         
    #connect with server
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
         smtp.ehlo()
         smtp.starttls()
         smtp.ehlo()
         
         smtp.login('your email','your password')
         
        
         #send email  
         smtp.send_message(message)
         
    print("email has sent")
 
    Debuggerpoke.write("Email is sent")
