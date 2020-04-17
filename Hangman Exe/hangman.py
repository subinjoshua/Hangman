# %%


# %%
import random
import sys
import requests
from bs4 import BeautifulSoup
import os
import bs4

"""this version of Hangman takes a word from a text called edited.txt and looks up its meaning online
and displays the meaning of the word too. Fun and quick way to learn a new word!"""
   

# PURPLE = '\033[95m'
# CYAN = '\033[96m'
# DARKCYAN = '\033[36m'
# BLUE = '\033[94m'
# GREEN = '\033[92m'
# YELLOW = '\033[93m'
# RED = '\033[91m'
# BOLD = '\033[1m'
# UNDERLINE = '\033[4m'
# END = '\033[0m'    
    
game_count = 0


def rules():
    print("\n\n\n")

    print("######\t\t\t\t Rules of the game:\t\t                   #######")
    print("## 1.You have 6 wrong tries before the hangman gets you!                           \t##")
    print("## 2.If the word given by hangman has recurring letters, all of it will be displayed\t##")
    print("##########################################################################################")
##################################################################################################################
def filler():                                              #fills visual_answer with ___
    for i in range(0,len(answer)):
        visual_answer.append("___")
        #print("Filler worked!",visual_answer)
##################################################################################################################        

               

def winning_check():
    winning_count=0
    for i in range(0,len(visual_answer)):
        if visual_answer[i].isalpha():
            winning_count=winning_count+1
        else:
            pass
    #print("winning count is {}".format(winning_count))
    if winning_count==len(answer):
        game_over_win()
    else:
        user_input()  
    
#################################################################################################################                 
def random_finder():
    m_rand=random.sample(answer,2)
    #print("Randomer works!")
    #print(m_rand,len(m_rand))
    replacer(m_rand)

def replacer(m_rand):
    #fills visual_answer with LETTERS
    for i in m_rand:
        letter_count=-1
        for j in answer:
            if i==j:
                letter_count+=1
                visual_answer[letter_count]=i
            else:
                letter_count+=1
    #print("replacer works")
    visual_clue()


def visual_clue():
    print("# This is the word : ",end="  ")                  
    for i in visual_answer:
        print(i,sep="  ", end= " ")
    print(" ")
    
    
    winning_check()
##################################################################################################################    
    
    
def user_input():
    global letter_input
    letter_input=""
    letter_input=input("# Guess a letter : ")
    letter_check(letter_input)
    letter_input=letter_input.upper()
    answer_against_input_checker(letter_input)
    
##################################################################################################################    
def letter_check(letter_input):                                  #this checks if the inupt is an alphabet
    if letter_input.isalpha():                                   #working
        return True
    else:
        print("# This only accepts letters.Try Again!\n")
        user_input()
###################################################################################################################

def answer_against_input_checker(letter_input):
    if letter_input in visual_answer:
        print("# Sorry! This letter already exists!")
        print("#")
        user_input()
    else:
        if letter_input in answer:
            #if i == letter_input:
            print("# Correct Guess!")
            print("#")
            replacer(letter_input)
            
        else:
            
            #print("answer_against_input_checker is moving to fail with value being {}".format(letter_input))
            #print(answer)
            failed_tries(letter_input)
                
##################################################################################################################
        
def failed_tries(letter_input):
    global user_try
    user_try+=1
    if user_try ==6:
        print("# {} does not exisit in the word! This was your last try :( ".format(letter_input))
        print("#")
        game_over_loss()
    else:
        print("# {} does not exisit in the word! This is your {}/6 tries ".format(letter_input,user_try))
        print("#")
    user_input()
##################################################################################################################    
def game_over_loss():
    print("# Game over!")
    print("# The word you had to guess is: ",end = " ")
    print(answer)
    print("#   _____")
    print("#  /     \\")
    print("# | () () |")
    print("#  \  ^  /")
    print("#   |||||")
    print("#   |||||")
    print("#   -----")
    print("#")
    play_again()
##################################################################################################################
def game_over_win():
    print("# YAY! You have won!")
    print("#")
    play_again()
##################################################################################################################
    
def play_again():
    print("# Would you like to play again?")
    print("#")
    restart=input("#"+" "+"Y"+"/"+"N"+"?")
    if restart=="y" or restart=="Y":
        game_refresh()
    else:
        game_stop()
##################################################################################################################

def game_stop():
    print("# Hope you have enjoyed playing this game as much as I have enjoyed making this!")
    try:
        sys.exit()
    except:
        sys.exit()

##################################################################################################################
def game_start():
    print("\t\t\t###############################################################")
    print("\t\t\t#                                                             #")
    print("\t\t\t#\t\t Welcome to Subin's Hangman game!             #")
    print("\t\t\t#                                                             #")
    print("\t\t\t###############################################################")
    global answer
    global visual_answer
    global game_count
    answer=random.choice(words).strip().upper()
    #print("answer is=",answer)
    user_try=0
    
    if game_count == 0:
        index_count=-1
        visual_answer=[] 
        rules()
        filler()
        definition(answer)
        random_finder()
        
    else:
        index_count=-1
        visual_answer=[] 
        filler()
        definition(answer)
        random_finder()
    
    
##################################################################################################################
def game_refresh():
    global visual_answer
    global user_try
    global index_count
    global game_count
    
    visual_answer.clear()
    user_try=0
    index_count=-1
    os.system('cls')
    game_count += 1
    game_start()
    
#################################################################################################################
def definition(answer):
    
    link = "https://www.vocabulary.com/dictionary"
    link = link+"/"+answer
    #print(link,answer)
    req = requests.get(link)
    if req.status_code == 200:
        word_definition = req.content
        soup = BeautifulSoup(word_definition,"html.parser")
        begin = soup.find(class_="definition")
        #print(begin)
        begin1 = begin.find("h3",class_="definition")
        if begin1 is not None:
            #print("invoking 1st")
            for i in begin1:
                if isinstance(i,bs4.element.NavigableString):
                    d=i.strip()
            print("#")
            print("# Definition of the word to be guessed:",end = " ")
            print(d)
            print("#")
        else :
            #print("invoking 2nd")
            ank = begin.tr.find_all("div")
            count = 0
            for i in ank:
                for j in i:
                    if isinstance(j,bs4.element.NavigableString) and count==0 :
                        if len(j) < 3:
                            pass
                        else:
                            d = j.strip()
                            print("#")
                            print("# Definition of the word to be guessed:",end = " ")
                            print(d)
                            print("#")
                            count = count + 1
    else:
        print("#")
        print("# Definition cannot be found, Check your internet connection!")
          
##################################################################################################################    

user_try=0
flag=True
# #code to edit the usa.txt file taken from http://www.gwicks.net/dictionaries.htm, ty gwicks.net!
# original_file= open("usa.txt","r")
# edited_file = open("edited.txt","w")
# for i in original_file:
#     i=i.strip()
#     if ((len(i)<6) or (i[-2:]=="ed") or (i[-3:]=="ing") or (i[-4:]=="ions") or (i[-1:]=="s")):
#         pass
#     else:
#         edited_file.write(i)
#         edited_file.write("\n")
# original_file.close()
# edited_file.close()


with open("edited.txt","r") as wordbook:
        words=[i for i in wordbook]
          


game_start()
    
