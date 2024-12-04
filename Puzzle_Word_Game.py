import os
import  platform
import mysql.connector
import datetime


import random
import time

from colorama import Fore
from colorama import Style
import pygame
pygame.mixer.init()
def mysqldata():
    global mysqlpuzzle
    mysqlpuzzle=mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        port=3306,
        database='puzzlegame',
    )
    cursor1=mysqlpuzzle.cursor()
    return cursor1

def save_game_details(username,usermobilenumber,scoreR1,scoreR2,total):
    func_calling=mysqldata()
    players=(username,usermobilenumber,scoreR1,scoreR2,total)
    sql='INSERT INTO playersdetails(username,usermobilenumber,score_R1,score_R2,total,UserTime) values(%s,%s,%s,%s,%s,NOW())'
    try:
        func_calling.execute(sql,tuple(players))
        mysqlpuzzle.commit()
        print("Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"ALERT  ERROR IS:{err}")
    finally:
        func_calling.close()
def view_players_details():
    func_calling=mysqldata()
    SQL='SELECT*FROM PLAYERSDETAILS'
    try:
        func_calling.execute(SQL)
        result=func_calling.fetchall()
        print("\n*******-----players details-----*******")
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Mobile: {row[2]}, Round 1 Score: {row[3]}, Round 2 Score: {row[4]}, Total Score: {row[5]}, Timestamp: {row[6]}")
    except mysql.connector.Error as err:
            print(f"ALERT  ERROR IS:{err}")
    finally:
        func_calling.close()


rightsound=pygame.mixer.Sound("correct.mp3")
wrongsound=pygame.mixer.Sound("incorrect.mp3")
new_level_game=pygame.mixer.Sound("startend.mp3")
score=pygame.mixer.Sound("score.mp3")
listing={"letter","king","thanks","victory","power","battle","workout","palace","project","verification","envelope","victim","space","disease","company"}
listing2={"caterpillar","quarantine","ecosystem","success","butterfly","umbrella","volcano","astronomy","bustling","atmosphere","captivating","excitement","perplex","muscle","communication"}

def shuffling(word):
    words=list(word)
    shuffle_words=word
    while shuffle_words==word:
        random.shuffle(words)
        shuffle_words=''.join(words)
    return shuffle_words


def main():
    new_level_game.play()
    print(Fore.MAGENTA+Style.BRIGHT+"*** welcome to the puzzle🧩🧩  game level 1 ***")
    print(Fore.BLUE+"note:one point for every correct answer in first attempt otherwise half points")
    print()
    # introdetails()
    user_name=input("ENTER YOUR NAME:")
    user_cont_details=int(input("Enter your Mob.no:"))
    print("******************************************")
    golden_coin=0
    choices=0
    for i in listing:
        jumble_words=shuffling(i)
        print(f'{Style.BRIGHT}{Fore.BLACK}Guess The Correct Word: {jumble_words}')
        print(f"{Fore.YELLOW}If you want exit the game please type 'exit' or 'quit'.")

        user_input=input(Fore.LIGHTMAGENTA_EX+'Type your answer----->')
        choices+=1
        print()

        if user_input.lower()=="exit" or user_input.lower()=="quit":
            break

        elif user_input.lower()==i.lower():
            rightsound.play()
            print(f"{Style.BRIGHT}{Fore.GREEN}wow! {user_name} you're correct:",i)
            golden_coin+=1

        if user_input.lower()!=i.lower():

            print(f"Try again:{shuffling(jumble_words)}")
            second_option=input("------>>")
            if second_option.lower()!=i.lower() or choices==3:
                print("")
                wrongsound.play()
                print(f"{Fore.RED}oops! {user_name.upper()} you are wrong!!!the correct answer is:", i)
            elif second_option.lower()==i.lower():
                print("")
                rightsound.play()
                print(f"{Fore.GREEN}wow! {user_name} you're correct:", i)
                golden_coin+=0.5

        print()
        print()
    score.play()
    print("🪙🪙you earn:",golden_coin,"/",len(listing))
    print(Style.BRIGHT+"congrats the total gold coins collected in  round1🔥🔥👏:","🪙🪙",golden_coin)
    


    print("***")
    print("***")
    new_level_game.play()
    print(f"{Fore.MAGENTA}welcome to the round 2🧩🧩")
    print(f"{Fore.LIGHTRED_EX}Be ready for medium level puzzle game all the best {user_name}")
    new_level_game.play()
    golden_coin_round2 = 0
    choices = 0

    for i in listing2:
        jumble_words = shuffling(i)
        print(f'{Fore.BLACK}Guess The Correct Word: {jumble_words}')
        print(f"{Fore.YELLOW}If you want exit the game please type 'exit' or 'quit'.")
        user_input = input(Fore.LIGHTMAGENTA_EX + 'Type your answer----->')
        choices += 1
        print()

        if user_input.lower() == "exit" or user_input.lower() == "quit":
            break
        elif user_input.lower()==i.lower():
            rightsound.play()
            print(f"{Fore.GREEN}wow! {user_name} you're correct:",i)
            golden_coin_round2+=1
            print()
        if user_input.lower()!=i.lower():
            print(f"Try again:{shuffling(jumble_words)}")
            second_option=input("----->")
            if second_option.lower()!=i.lower() or choices==3:
                print()
                wrongsound.play()

                print(f"{Fore.RED}oops! {user_name.upper()} you are wrong!!!the correct answer is:", i)
                print()
            elif second_option.lower()==i.lower():
                print()
                rightsound.play()

                print(f"{Fore.GREEN}wow! {user_name} you're correct:", i)

                golden_coin_round2+=0.5
    print()

    score.play()
    print("Score Board")
    print("🪙🪙you earn:", golden_coin_round2, "/", len(listing2))
    print("the total gold coins collected in  round2:","🪙🪙",golden_coin_round2)
    print("total earned coins:","🪙🪙",golden_coin+golden_coin_round2)

    save_game_details(user_name, user_cont_details, golden_coin, golden_coin_round2, golden_coin + golden_coin_round2)
    score.play()
    time.sleep(score.get_length())
    view_players_details()


main()





























