# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 22:22:13 2023

@author: Dan
"""
#imports including pokemon desciption function
#import pokemon_data_frame
import random
import requests
from win10toast import ToastNotifier
import smtplib
from email.message import EmailMessage


###############making txt file for debugger









# =============================================================================
# directory = "C:/Users/Dan/Desktop/Python Files/Debugging txt files"
# 
# 
# # Create the directory if it doesn't exist
# if not os.path.exists(directory):
#     os.makedirs(directory)
#     
# file_path = os.path.join(directory, "unicode.txt")
# 
# file_path = 'C:\Users\Dan\Desktop\Python Files\Debugging txt files'
#  
# with open(file_path,'a',encoding=utf-8) as Debuggerpoke:    
#     
# file.write("Some text\n")
# 
# =============================================================================


#making random dex number to add to the end of api url
random_dex_num = str(random.randint(1,1008))

url = f"https://pokeapi.co/api/v2/pokemon/{random_dex_num}" 


response = requests.get(url)

pokemon_raw_data = response.json()




# =============================================================================
# print(f"Pokedex Number: {pokemon_data_frame.dex_num}")
# print(f'\nBase Stats:\nHP: {pokemon_data_frame.base_hp}\nAttack: {pokemon_data_frame.base_att}\nDefense: {pokemon_data_frame.base_def}\nSpeaial Attack: {pokemon_data_frame.base_spa}\nSpecial Defense: {pokemon_data_frame.base_spd}\nSpeed: {pokemon_data_frame.base_speed}')
# for x in pokemon_data_frame.type_names:
#     print("Type: " + x.title())
# print("Moveset:\n")
# 
# for x in pokemon_data_frame.movesets:
#    print(x.title() + '\n')
# 
# =============================================================================

#pokemon variables
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

######nes for loop
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


 #fetching specific move descriptions 
#creating url list for all moves
moves_list_url=[]
for dictionary in raw_moveset:
    moveset_url = dictionary['move']['url']
    moves_list_url.append(moveset_url)


# =============================================================================
# def email():
#     print(f"Pokedex Number: {dex_num}\n")
#     print(poke_name.title())
#     print("")
#     print(f'\nBase Stats:\nHP: {base_hp}\nAttack: {base_att}\nDefense: {base_def}\nSpeaial Attack: {base_spa}\nSpecial Defense: {base_spd}\nSpeed: {base_speed}')
#     for x in type_names:
#         print("Type: " + x.title())
#     print("Moveset:\n")
#     
#     for x in movesets:
#        print(x.title() + '\n')
# 
# text_file = email()
# =============================================================================

#creating ,txt file
with open('Pokemon Daily Update.txt', 'w') as file:
    # Write the content to the file
    file.write(f"Pokedex Number: {dex_num}\n")
    file.write("\n")
    file.write(poke_name.title())
    file.write("\n")
    for x in type_names:
        file.write("Type: " + x.title())
    file.write("\n")
    file.write("Moveset:\n")
    file.write("\n")
    for x in movesets:
        file.write(x.title() + '\n')



 

#############notifcation

#reading text file
with open('Pokemon Daily Update.txt', 'r') as file:
    notification_message = file.read()


poke_notif = ToastNotifier()
# #displaying notication
poke_notif.show_toast("Daily Pokemon Stats",notification_message,duration=11)

###########Emailing The Stats

message = EmailMessage()
message['From'] = 'your email'
message['To'] = 'sending to email'
message['Subject'] = 'Pokemon Daily Stats'
message.set_content(str(notification_message))
     
#connect with server
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
     smtp.ehlo()
     smtp.starttls()
     smtp.ehlo()
     
     #smtp.login('your email','password')
     
    
     #send email  
     smtp.send_message(message)
     
print("email has sent")
 


with open('Sucess.txt', 'w') as confirm:
    confirm.write("the email has been sent")



# =============================================================================
# server = smtplib.SMTP('smtp.gmail,com',465)
# 
# server.starttls()
# 
# server.login()
# 
# server.sendmail("your email",'sending to')
# 
# print("email has sent")
# 
# =============================================================================




