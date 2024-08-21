
import tkinter as tk
from random import randint
import csv
import webbrowser


maxrounds = 6  # number of rows / word trials
actualwritingrow = 0
overallwidth = 11  # for the Columnspan
emptyrows_above_keyboard = maxrounds + 6
#wordoftheday = ""

# window with labels, buttons etc:
window = tk.Tk()
window.title("WUERTEL")

window.option_add("*font", "lucida 10")  # Change the default Font that will affect all the widgets
window.resizable(False, False)

infobutton = tk.Button(text = "i", command = lambda: info_popup())
infobutton.grid(row = 0, column = 0)

# nested list to hold the letters/words that are typed (and are shown in the buttons/rows on top of the game). The list contains tk.Button-objects:
letterbuttonslist = []
for r in range(maxrounds): # these are the rows
    singelrow = []
    for b in range(5): # these are the single letters
        letterbutton = tk.Button(window, text = "", width = 1, height = 1, activebackground = "#d9d9d9")
        singelrow.append(letterbutton)
    letterbuttonslist.append(singelrow)
# assign the nested list to the window-grid:
for r in range(maxrounds): # r is the row index, b is the letter index
    for b in range(5):
        letterbuttonslist[r][b].grid(row = actualwritingrow + r, column = b + 3)

label_emptyrow1 = tk.Label(window, text ="")
label_infomessage = tk.Label(window, text ="")
label_lost1 = tk.Label(window, text ="")
label_lost2 = tk.Label(window, text ="", font ="lucida 10 bold")
label_id_link_text = tk.Label(window, text ="")
label_id_link_url = tk.Label(window, text ="", cursor ="hand2", fg ="#595959")

label_emptyrow1.grid(row = maxrounds, column = 0, columnspan = overallwidth)
label_infomessage.grid(row =maxrounds + 1, column = 0, columnspan = overallwidth)
label_lost1.grid(row = maxrounds + 2, column = 0, columnspan = 9)
label_lost2.grid(row = maxrounds + 2, column = 9)
label_id_link_text.grid(row = maxrounds + 3, column = 0, columnspan = overallwidth)
label_id_link_url.grid(row = maxrounds + 4, column = 0, columnspan = overallwidth)


# keyboard-buttons:
buttons = []
buttondict = {}
keyboard_for_lu = "QWERTZUIOPÜASDFGHJKLÖbYXCVBNMÄÉËe"
for letter in keyboard_for_lu:
    button = tk.Button(window, text = letter)
    button.config(width = 1, height = 1, command = lambda x = button: push_letter(x))
    buttons.append(button)
    buttondict[letter] = button  # a dictionary to be able to later refer to it with the text/button name
for row in range(0, 3):
    for col in range(0, 11):
        i = row * 11 + col
        buttons[i].grid(row = row + emptyrows_above_keyboard, column = col)

click_back_icon = tk.PhotoImage(file='backspace-30-32.png')
click_enter_icon = tk.PhotoImage(file='keyboard-return-32.png')
buttondict["b"].config(width = 30, height = 25, image = click_back_icon)
buttondict["e"].config(width = 30, height = 25, image = click_enter_icon)

restart_game = tk.Button(window, text = "Restart Game", state = tk.DISABLED, command = lambda: restartgame())
restart_game.grid(row = 15, column = 0, columnspan = overallwidth)


#-------------------------------


# function definitions for the game:
# (todo: move functions to a separate file and import, for a better readability)

def info_popup():
    popup_window = tk.Toplevel(window)
    popup_window.wm_title("Spillinfo")
    popup_label = tk.Label(popup_window, text = "Wëllkomm bei Wuertel, der lëtzebuerger Variant vum Spill Wordle. An sou fonctionneiert et:\n"
      "Et geet drëm, en Wuert mat 5 Buchstawen ze roden.\nEt as ähnlech wéi d'Spill 'Mastermind', mee et kënnen nëmmen komplett (existéirend) Wieder agin gin (keng eenzel Buchstawen).\n"
      "Wann ee Buchstaw falsch as, da gët en gro, wann de Buchstaw richteg as get en gréng.\n"
      "En orangen Buchstaw heescht, et as deen richtegen Buchstaw, awer op der falscher Plaz.\n")
    popup_label.pack()
    ok_button = tk.Button(popup_window, text = "Okay", command = popup_window.destroy)
    ok_button.pack()
    popup_window.wm_transient(window)  # to keep the toplevel window in front of the root window


def start_game():
    global randomword
    global randomword_original
    global actualround, actualwritingrow, actual_text, game_won
    actualround = 1
    actualwritingrow = 0
    actual_text = ""
    game_won = False
    # to assure that no word (to guess) comes twice in one game session:
    chosenword = possiblewordslist[randint(0, len(possiblewordslist))]
    while chosenword in anti_repeat_list:
        chosenword = possiblewordslist[randint(0, len(possiblewordslist))]
    else:
        randomword_original = chosenword
        anti_repeat_list.append(chosenword)
    randomword = randomword_original.upper()
    #print("randomword an der fonctioun:", randomword, "\n\n")  # can be uncommented if it's needed to know the word to guess for debugging or testing

def push_letter(button):
    global actualround, actualwritingrow, actual_text, game_won
    global randomword_original
    buttontext = button["text"]
    lettercounter = len(actual_text)

    if buttontext == "e":  # "e" stands for "enter"
        if len(actual_text) == 5:  # enter can only be pressed if the 5 letters of a row are filled in
            if actual_text in possiblewordslist_upper:
                checkwordfunc()
            else:
                label_infomessage.config(text ="Dat Wuert as net an der Lëscht.")
        else: # if the word is too short (not all letters of a row are filled in)
            label_infomessage.config(text ="Däi Wuert muss 5 Buchstawen hun")
    elif buttontext == "b":  # "b" stands for "backspace"
        label_infomessage.config(text ="")  # reset the label, so that a potential error message disappears again
        if lettercounter > 0:
            # if the actual row isn't already empty, the last letter is deleted from the buttons:
            actual_letterbutton = letterbuttonslist[actualwritingrow][lettercounter - 1]
            actual_letterbutton["text"] = ""
        actual_text = actual_text[0:-1]  # the last letter is also deleted from the word that we are typing
    else: # letter buttons
        label_infomessage.config(text = "")  # reset the label, so that a potential error message disappears again
        if lettercounter < 5:
            actual_text += buttontext
            letterbuttonslist[actualwritingrow][lettercounter].config(text = buttontext)

def checkwordfunc():
    global actualround, actualwritingrow, actual_text , game_won
    global randomword

    if actual_text == randomword:
        game_won = True
        rounds_word = lambda x: "Ronn" if x == 1 else "Ronnen"
        label_infomessage.config(text =f"Du hues gewonn! Du hues {actualround} {rounds_word(actualround)} gebraucht.")
        label_id_link_text.config(text = "Hei as de Link zu der Begrëffs-Erklärung:")
        label_id_link_url.config(text = "https://www.lod.lu/artikel/" + id_dict[randomword_original])
        label_id_link_url.bind("<Button-1>", lambda e: hyperlink_for_label("https://www.lod.lu/?" + id_dict[randomword_original]))
        restart_game.config(state = tk.NORMAL)
        for letterbutton in letterbuttonslist[actualwritingrow]:  # if game is won, change all buttons of the right word to green
            letterbutton.config(bg = "green")
        for i in range(5):
            buttondict[actual_text[i]]["bg"] = "green"  # change the right keyboard buttons to green
        disable_keyboard(buttons)

    else:  # if the game is not yet won or lost
        input_countercheck = list(randomword)
        text_countercheck = list(actual_text)
        # change the colour of the keyboard letters, for the green ones:
        for i in range(5):
            if actual_text[i] == input_countercheck[i]:
                input_countercheck[i] = "-"
                text_countercheck[i] = "green"
                buttondict[actual_text[i]].config(bg = "green")

        # change the colour of the keyboard letters, for the yellow and grey ones:
        for i in range(5):
            if actual_text[i] in input_countercheck:
                letterindex = input_countercheck.index(actual_text[i])
                if text_countercheck[i] != "green":
                    text_countercheck[i] = "orange"
                    input_countercheck[letterindex] = "-"
                if buttondict[actual_text[i]]["bg"] != "green":
                    buttondict[actual_text[i]].config(bg = "orange")
            else:  #if actual_text[i] not in input_countercheck
                if buttondict[actual_text[i]]["bg"] != "green" and buttondict[actual_text[i]]["bg"] != "orange":
                    buttondict[actual_text[i]].config(bg = "grey")
                if text_countercheck[i] != "green" and text_countercheck[i] != "orange":
                    text_countercheck[i] = "grey"

        # change the colour of the buttons of the display on the top:
        for i in range(5):
            letterbuttonslist[actualwritingrow][i].config(bg = text_countercheck[i])

    if actualround == maxrounds:
        if game_won != True:
            label_lost1.config(text = f"Du hues verluer. Dat gesichtent Wuert war:")
            label_lost2.config(text = f"{randomword_original}")
            label_id_link_text.config(text = "Hei as de Link zu der Begrëffs-Erklärung:")
            label_id_link_url.config(text = "https://www.lod.lu/?" + id_dict[randomword_original])
            label_id_link_url.bind("<Button-1>", lambda e:hyperlink_for_label("https://www.lod.lu/?" + id_dict[randomword_original]))
            restart_game.config(state = tk.NORMAL)
            disable_keyboard(buttons)

    actualround += 1
    actualwritingrow += 1
    actual_text = ""

def hyperlink_for_label(url):
    webbrowser.open_new_tab(url)

def disable_keyboard(keyboard_buttons):
    for button in keyboard_buttons:
       button.config(state = tk.DISABLED)

def enable_keyboard(keyboard_buttons):
    for button in keyboard_buttons:
        button.config(state = tk.NORMAL)

def restartgame():
    restart_game.config(state = tk.DISABLED)
    enable_keyboard(buttons)
    start_game()
    # reset buttons (empty the buttons):
    for singlerow in letterbuttonslist:
        for singlebutton in singlerow:
            singlebutton.config(text = "", bg = "#d9d9d9")
    # reset the keyboard buttons to grey:
    for singlebutton in buttons:
        singlebutton.config(bg = "#d9d9d9")
    # reset/delete the label texts
    label_infomessage["text"] = ""
    label_lost1["text"] = ""
    label_lost2["text"] = ""
    label_id_link_text["text"] = ""
    label_id_link_url["text"] = ""



#-------------------------------


# game itself:

# create a list with the possible words:
possiblewordsfile = "Wuertel-Wiederlescht_mat_ID-dict.csv"
possiblewordslist = []  # the original words are needed to later build the link to the explanation url
possiblewordslist_upper = []  # the list with the uppercase words is needed to check if a typed word is in the list of possible words
id_dict = {}  # the id for every word is needed to later be able to link to the url with the explanation of the word (when the game is finished)
with open(possiblewordsfile, "r") as readfile:
    readfile_dict = csv.DictReader(readfile)
    for row in readfile_dict:
        # the 2 column names are "Wuert" and "ID"
        possiblewordslist.append(row["Wuert"])
        possiblewordslist_upper.append(row["Wuert"].upper())
        id_dict[row["Wuert"]] = row["ID"]
    readfile.close()


anti_repeat_list = []


start_game()


window.mainloop()
