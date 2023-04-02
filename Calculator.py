# Import the important modules.
import shelve
from pygame import mixer
try:
    import tkinter
except ImportError:  # Python 2
    import Tkinter as tkinter

# Initialize mixer.
mixer.init()

# Number of columns
NO_OF_COLUMNS = 9

# Sound effects.
BUTTON_CLICKED_SOUND, ERROR_SOUND = 'Mouse click.mp3', 'Error sound.mp3'

# Define all global variables.
input_user = ''  # The input by the user will be stored in this variable.
equal_to_pressed = operator_variable = irrational = False   # `equal_to_pressed` is whether equal to is pressed
# or not. `operator_variable` is whether an operator is pressed or not. `irrational` is whether euler's number (e)
# or Archimedes' constant (π) or golden ratio or phi(ϕ) is pressed or not.
operator_index = point_index = 0  # `operator_index` is the index of the operator, `point_index` is the
# index of the point.
first_time = True 


def play_sound(name_of_sound: str) -> None:
    """Get a string(name of sound effect) and play it.

    :param name_of_sound: The sound effect to be played."""
    # The mixer module of pygame is used to play sound.
    sound = mixer.Sound(name_of_sound)
    sound.play()


def integer_or_not(number: float) -> bool:
    """Get a number and return whether the number is an integer or is suffixed with .0.

    :param number: The number to be checked.
    :return: Whether the number is an integer or is suffixed with .0."""
    return number == int(number)


def history() -> None:
    """Make a new window and display the history."""
    # Play the sound effect
    play_sound(BUTTON_CLICKED_SOUND)

    def clear_() -> None:
        """Clears the memory"""
        play_sound(BUTTON_CLICKED_SOUND)
        with shelve.open('Memory.shelve', 'w') as memory_file_clear:
            
            # We open it as a written and clear it with the `clear` method.
            memory_file_clear.clear()
        # Then we delete the contents of the listbox.
        history_listbox.delete(0, tkinter.END)

    # Set the window
    window = tkinter.Tk()
    window.config(bg='#0F0F0F')
    window.title('History')
    window.geometry('500x600-800-100')
    window.resizable(False, False)

    # Configure columns.
    window.columnconfigure(0, weight=3)
    window.columnconfigure(1, weight=1)

    # Configure row.
    window.rowconfigure(0, weight=1)

    # Declare the components of the screen.
    history_listbox = tkinter.Listbox(window, relief='sunken', borderwidth=3)
    scrollbar_memory = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=history_listbox.yview)
    scrollbar_horizontal = tkinter.Scrollbar(window, orient=tkinter.HORIZONTAL,
                                             command=history_listbox.xview)
    clear = tkinter.Button(window, text='Clear', relief='raised', command=clear_,
                           background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                           activeforeground='white', font=('digital-7', 17), borderwidth=3)

    # We add the items to the `memory_listbox`.
    with shelve.open('Memory.shelve', 'r') as memory_shelve_file:
        for value in memory_shelve_file.values():
            history_listbox.insert(tkinter.END, value)

    # Grid the items.
    history_listbox.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
    scrollbar_memory.grid(row=0, column=0, sticky='nse', padx=10, pady=10)
    scrollbar_horizontal.grid(row=0, column=0, sticky='ews', padx=10, pady=10)
    clear.grid(row=0, column=1)

    # Now we attach the scrollbars and the listbox.
    history_listbox['yscrollcommand'] = scrollbar_memory.set
    history_listbox['xscrollcommand'] = scrollbar_horizontal.set

    # The main loop.
    window.mainloop()


def copy() -> None:
    """Copy the `input user` to the clipboard."""
    # Play the sound effect
    play_sound(BUTTON_CLICKED_SOUND)

    global input_user

    screen.clipboard_clear()
    screen.clipboard_append(input_user)
    screen.update()  # Just to be safe that after the screen is destroyed then also
    # we get it.


def paste() -> None:
    """Paste the content of the clipboard on the screen."""
    global input_user
    clipboard_content = input_user + screen.clipboard_get()    # The function
    # for getting the content of the clipboard.
    input_user = ''
    for character in clipboard_content:
        if character in '1234567890/*-^+().':
            # If the character is one of these only then we want to show it.
            btn_pressed(character)


# def simplify_equation(string: str) -> str:
#     """Get a mathematical equation and return it after simplifying.
#
#     param string: The mathematical equation.
#     return: The answer as a string."""
#     string = string.replace('+', ' + ')
#     string = string.replace('*', ' * ')
#     string = string.replace('-', ' - ')
#     string = string.replace('/', ' / ')
#     string = string.replace('^', ' ^ ')
#     equation = string.split()
#     if equation[0] == '+':
#         equation.remove('+')
#     elif equation[0] == '-':
#         equation.remove('-')
#         equation[0] = str(float(equation[0]) * -1)
#     while len(equation) > 1:
#         if equation[1] == '+':
#             equation[0] = float(equation[0]) + float(equation[2])
#             equation.remove('+')
#             equation.pop(1)
#         elif equation[1] == '-':
#             equation[0] = float(equation[0]) - float(equation[2])
#             equation.remove('-')
#             equation.pop(1)
#         elif equation[1] == '*':
#             if equation[2] == '-':
#                 equation[2] = float(equation[3]) * -1
#                 equation.pop(3)
#             equation[0] = float(equation[0]) * float(equation[2])
#             equation.remove('*')
#             equation.pop(1)
#         elif equation[1] == '/':
#             if equation[2] == '-':
#                 equation[2] = float(equation[3]) * -1
#                 equation.pop(3)
#             try:
#                 equation[0] = float(equation[0]) / float(equation[2])
#                 equation.remove('/')
#                 equation.pop(1)
#             except ZeroDivisionError:
#                 return 'Division by zero is not defined'
#         else:
#             if equation[2] == '-':
#                 equation[2] = float(equation[3]) * -1
#                 equation.pop(3)
#             equation[0] = float(equation[0]) ** float(equation[2])
#             equation.remove('^')
#             equation.pop(1)
#     return str(equation[0])
# This is my function for simplifying the equation. Although, now I have found out that there is an in-built function
# called eval.


def is_numeric(string: str) -> bool:
    """Get a string and check whether it is a float or not.

    :param string: The string to be checked.
    :return: Whether `string` is a float or not."""
    try:
        string = float(string)
        # If we don't get an error, then it is a float. So, we return True.
        return True
    except ValueError:
        # If we get an error while converting to float, then it is not a float. So, we return False.
        return False


def backspace_(string: str) -> None:
    """Get a string and remove the last character from it and then display it.

    :param string: The string whose last character is to be removed."""
    global input_user
    if len(string) == 0:
        # If it is already an empty string:
        btn_pressed('')
        play_sound(ERROR_SOUND)
    else:
        input_user = ''
        # We make it an empty string so that the equation does not appear twice.
        btn_pressed(string.removesuffix(string[-1]))


def btn_pressed(string: str) -> None:
    """Get a string and display it on the screen.

    :param string: The string to be displayed."""
    # Play the sound effect.
    play_sound(BUTTON_CLICKED_SOUND)

    # Global variables.
    global input_user
    global operator_variable
    global equal_to_pressed
    global operator_index
    global point_index
    global irrational
    global first_time
    
    if ((string.isnumeric() or is_numeric(string)) and equal_to_pressed) or (input_user == 'Invalid Input' or
                                                                             input_user ==
                                                                             'Division by zero is undefined.' or
                                                                             input_user == 'Value too large'):
        # If the string is one of the errors, when we type the number, it should clear the string and then add
        # the current string to be added. If it is the answer, then also we need to clear but only if the value
        # to be entered is a number. If it is an operator then we do not need to clear the string.
        input_user = string
        typed = tkinter.Label(screen, text=input_user,
                              relief='sunken', background='#0F0F0F', foreground='white',
                              font=('digital-7', 17), borderwidth=6, anchor='e')
    elif string == '':
        # if the string passed was an empty string, we check whether the string was already
        # empty, if yes, we play error sound effect and then clear the `input_user`.
        if len(input_user) == 0 and not first_time:
            # If the string was already empty we play the error sound effect.
            play_sound(ERROR_SOUND)
        input_user = string
        typed = tkinter.Label(screen, text=input_user,
                              relief='sunken', background='#0F0F0F', foreground='white',
                              font=('digital-7', 17), borderwidth=6, anchor='e')
    else:
        if string in '/*^+-.':
            # If the string is an operator.
            if not operator_variable:
                # If the operator is not already pressed only then we want to let it press.
                if string != '.':
                    # Now we want to assign this new index to the `operator_variable`.
                    operator_index = len(input_user)
                    input_user += string
                    typed = tkinter.Label(screen, text=input_user,
                                          relief='sunken', background='#0F0F0F', foreground='white',
                                          font=('digital-7', 17), borderwidth=6, anchor='e')
                    # Now we set `operator_variable` to True. But we want to allow - after * or /. So there is an
                    # elif statement below.
                    if string != '':
                        operator_variable = True
                    irrational = False
                elif '.' not in input_user or point_index < operator_index:
                    # If index of the point is greater than the index of the operator, that means that a point is
                    # already there in the last number. So we do not want to allow the user to write it again. Also,
                    # if point has not been typed even once, we allow the user to type it.
                    point_index = len(input_user)
                    input_user += '.'
                    typed = tkinter.Label(screen, text=input_user, relief='sunken', background='#0F0F0F',
                                          font=('digital-7', 17), borderwidth=6, fg='white', anchor='e')
                    operator_variable = True  # So that the user cannot type an operator just after the point.
                else:
                    play_sound(ERROR_SOUND)
                    return None  # We do not do anything.
            elif len(input_user) > 1:
                # We check whether the length of `input_user` is greater than 1, so that we do not get an IndexError.
                if (input_user[-1] == '*' or input_user[-1] == '/' or input_user[-1] == '^') and string == '-':
                    # If the last string was * or / and the string is -:
                    operator_index = len(input_user)
                    input_user += string
                    typed = tkinter.Label(screen, text=input_user, relief='sunken', background='#0F0F0F',
                                          font=('digital-7', 17),
                                          borderwidth=6, fg='white', anchor='e')
                    # We now make the operator variable True.
                    operator_variable = True
                else:
                    play_sound(ERROR_SOUND)
                    return None  # We do not do anything.
            else:
                play_sound(ERROR_SOUND)
                return None  # We do not do anything.

        elif string == '3.141592653589793' or string == '2.718281828459045' or string == '1.618033988749894':
            # We do not want to add them in front of normal numbers.
            try:
                if (input_user[-1] in '+-/|^(*') and not irrational:
                    # We want to add it only if the last item was an operator.
                    input_user += string
                    typed = tkinter.Label(screen, text=input_user, relief='sunken', background='#0F0F0F',
                                          font=('digital-7', 17),
                                          borderwidth=6, fg='white', anchor='e')
                    point_index = len(input_user) - 15  # Both of them have 15 digits after `.` So we subtract 15 from
                    # the length of the user.
                    operator_variable = False
                    irrational = True
                else:
                    play_sound(ERROR_SOUND)
                    return None
            except IndexError:
                # If we get an index error, it means the length of `input_user` was 0. If the length of
                # `input_user` was 0 then we have to allow the user to press the button.
                input_user += string
                typed = tkinter.Label(screen, text=input_user, relief='sunken', background='#0F0F0F',
                                      font=('digital-7', 17),
                                      borderwidth=6, fg='white', anchor='e')
                operator_variable = False
                irrational = True
                point_index = len(input_user) - 15
        else:
            # If the string was a number or a bracket:
            if len(input_user) > 1:
                # So that we do not get an error for the next if statement.
                if input_user[-1] == '0' and input_user[-2] in '+-*/()':
                    # If the previous item was 0, we can remove 0 because 0 at the start does not matter.
                    input_user = input_user.removesuffix('0')
                if not input_user[-1] in '+-*/^' and string == '(':
                    return None
            elif input_user == '0':
                # If the only item is 0, we have to replace it with the current item.
                input_user = input_user.removesuffix('0')
            input_user += string
            typed = tkinter.Label(screen, text=input_user, relief='sunken', font=('digital-7', 17),
                                  background='#0F0F0F', borderwidth=6, fg='white', anchor='e')
            operator_variable = False
            irrational = False
    equal_to_pressed = False
    typed.grid(row=0, column=0, sticky='nsew', columnspan=NO_OF_COLUMNS)


def simplify(string: str) -> None:
    """Get a string(mathematical equation) and show the result on the screen.

    :param string: The mathematical equation as a string."""
    global equal_to_pressed
    global point_index
    global operator_index

    # We set operator_index to 0.
    operator_index = 0

    # We want to maintain a history. So, we add it to a variable.
    history_equation = input_user + ' = '

    # We make `input_user` an empty string so that we can only see the answer.
    btn_pressed('')    # We have passed an empty string and put an if statement
    # in the btn_pressed function to clear the `input_user` if the string is empty

    try:
        # We can get many errors like 0 division error, or the value entered by the user is invalid, therefore
        # we have this try statement.

        # If the string has a carrot sign, we change it to ** because eval function takes this as raised to
        # power.
        string = string.replace('^', "**")

        answer = eval(string)

        # If the answer is suffixed with .0, it does not look good. So, we replace that.
        if integer_or_not(answer):
            # If the number is suffixed with .0, we remove that.
            answer = int(answer)
            point_bool = False
        else:
            point_bool = True

        # Now we will display the answer.
        btn_pressed(str(answer))

        # We have added the question and the equal to sign to the `history_equation`. Now we add the answer.
        history_equation += str(answer)

        if point_bool:
            # If there was a point:
            point_index = str(answer).index('.')   # We take only the index because the answer can
            # have only one point.
    except ZeroDivisionError:
        # If we get a zero division error, we have to display that division by zero is not defined.
        history_equation += 'Division by zero is undefined.'
        btn_pressed('Division by zero is undefined.')
        play_sound(ERROR_SOUND)
    except SyntaxError:
        # We can get this error if the input by the user is wrong. So, we have to show an error.
        history_equation += 'Invalid Input'
        btn_pressed('Invalid Input')
        play_sound(ERROR_SOUND)
    except OverflowError:
        # What if the user writes something like 10^(10^(10^(10^1000)))? Obviously, a value that large
        # cannot be shown on the screen. Thus eval returns OverflowError. In that case, we display the
        # message 'Value too large'.
        history_equation += 'Value too large'
        btn_pressed('Value too large')
        play_sound(ERROR_SOUND)
    except TypeError:
        # This error can occur if the input of the user is wrong.
        history_equation += 'Invalid Input'
        btn_pressed('Invalid Input')
        play_sound(ERROR_SOUND)

    # Now we add the `history_equation` in the shelve file for displaying the history.
    with shelve.open('Memory.shelve', 'w') as memory_file:
        memory_file[str(len(memory_file))] = history_equation
        # Shelve files always take a key, so we add a number which increases everytime user presses 'equal to'.
    equal_to_pressed = True


# Set the screen
screen = tkinter.Tk()
screen.geometry('500x250-437-300')
screen.title('Calculator')
screen.resizable(False, False)

# Set the icon
screen.iconbitmap('calc_icon.ico')

# Clear the screen.
btn_pressed('')    # We have passed an empty string and put an if statement
# in the btn_pressed function to clear the `input_user` if the string is empty.
first_time = False

# Configure rows.
for i in range(4):
    screen.rowconfigure(i, weight=1)

# Configure columns.
for i in range(NO_OF_COLUMNS):
    screen.columnconfigure(i, weight=1)

# Define the components of the screen.
btn0 = tkinter.Button(screen, text='0', command=lambda: btn_pressed('0'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')
btn1 = tkinter.Button(screen, text='1', command=lambda: btn_pressed('1'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')
btn2 = tkinter.Button(screen, text='2', command=lambda: btn_pressed('2'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')

btn3 = tkinter.Button(screen, text='3', command=lambda: btn_pressed('3'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')
btn4 = tkinter.Button(screen, text='4', command=lambda: btn_pressed('4'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')
btn5 = tkinter.Button(screen, text='5', command=lambda: btn_pressed('5'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')

btn6 = tkinter.Button(screen, text='6', command=lambda: btn_pressed('6'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')
btn7 = tkinter.Button(screen, text='7', command=lambda: btn_pressed('7'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')
btn8 = tkinter.Button(screen, text='8', command=lambda: btn_pressed('8'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')

btn9 = tkinter.Button(screen, text='9', command=lambda: btn_pressed('9'), relief='raised', borderwidth=3,
                      font=('digital-7', 17),
                      background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                      activeforeground='white')
add = tkinter.Button(screen, text='+', command=lambda: btn_pressed('+'), relief='raised', borderwidth=3,
                     font=('digital-7', 17),
                     background='#1B1B1B', foreground='white', activebackground='#1B1B1B', activeforeground='white')
minus = tkinter.Button(screen, text='-', command=lambda: btn_pressed('-'), relief='raised', borderwidth=3,
                       font=('digital-7', 17),
                       background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                       activeforeground='white')

multiply = tkinter.Button(screen, text='*', command=lambda: btn_pressed('*'), relief='raised', borderwidth=3,
                          font=('digital-7', 17),
                          background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                          activeforeground='white')
divide = tkinter.Button(screen, text='/', command=lambda: btn_pressed('/'), relief='raised', borderwidth=3,
                        font=('digital-7', 17),
                        background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                        activeforeground='white')
equal = tkinter.Button(screen, text='=', command=lambda: simplify(input_user), relief='raised', borderwidth=3,
                       font=('digital-7', 17),
                       background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                       activeforeground='white')

point = tkinter.Button(screen, text='.', command=lambda: btn_pressed('.'), relief='raised', borderwidth=3,
                       font=('digital-7', 17),
                       background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                       activeforeground='white')
backspace = tkinter.Button(screen, text='Backspace', command=lambda: backspace_(input_user),
                           relief='raised', borderwidth=3, font=('digital-7', 17), background='#1B1B1B',
                           foreground='white',
                           activebackground='#1B1B1B', activeforeground='white')
bracket_open = tkinter.Button(screen, text='(', command=lambda: btn_pressed('('),
                              relief='raised', borderwidth=3, font=('digital-7', 17), background='#1B1B1B',
                              foreground='white',
                              activebackground='#1B1B1B', activeforeground='white')

bracket_close = tkinter.Button(screen, text=')', command=lambda: btn_pressed(')'),
                               relief='raised', borderwidth=3, font=('digital-7', 17), background='#1B1B1B',
                               foreground='white',
                               activebackground='#1B1B1B', activeforeground='white')
cancel = tkinter.Button(screen, text='Clear', command=lambda: btn_pressed(''), relief='raised',
                        borderwidth=3, font=('digital-7', 17),
                        background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                        activeforeground='white')    # We have passed an empty string and put an if statement
# in the btn_pressed function to clear the `input_user` if the string is empty.
raised_to = tkinter.Button(screen, text='^', command=lambda: btn_pressed('^'),
                           relief='raised', borderwidth=3, font=('digital-7', 17),
                           background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                           activeforeground='white')

pi = tkinter.Button(screen, text='π', command=lambda: btn_pressed('3.141592653589793'),
                    font=('digital-7', 17), relief='raised', borderwidth=3,
                    background='#1B1B1B', foreground='white', activebackground='#1B1B1B', activeforeground='white')
euler_number = tkinter.Button(screen, text='e', command=lambda: btn_pressed('2.718281828459045'),
                              font=('arial', 15), relief='raised', borderwidth=3,
                              background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                              activeforeground='white')
copy_btn = tkinter.Button(screen, text='Copy', relief='raised', borderwidth=3, command=copy, font=('digital-7', 17),
                          background='#1B1B1B', foreground='white', activebackground='#1B1B1B',
                          activeforeground='white')

phi = tkinter.Button(screen, text='ϕ', relief='raised', borderwidth=3, background='#1B1B1B', foreground='white',
                     activebackground='#1B1B1B', activeforeground='white', command=lambda:
                     btn_pressed('1.618033988749894'), font=('digital-7', 17))
history_btn = tkinter.Button(screen, relief='raised', text='History', borderwidth=3, font=('digital-7', 17),
                             background='#1B1B1B', foreground='white', command=history,
                             activebackground='#1B1B1B', activeforeground='white')
paste_btn = tkinter.Button(screen, relief='raised', text='Paste', borderwidth=3, font=('digital-7', 17),
                           command=paste,
                           background='#1B1B1B', foreground='white', activebackground='#11151C',
                           activeforeground='white')

# Grid the items.
buttons = [history_btn, btn1, btn2, btn3, btn0, point, euler_number, pi, phi,
           cancel, btn4, btn5, btn6, minus, divide, bracket_open, raised_to, paste_btn,
           backspace, btn7, btn8, btn9, add, multiply, bracket_close, equal, copy_btn
           ]

# While griding, we can see that there is a pattern. The row changes by -1 every third time and the column is
# 012345678901234567890123456789. So, we implement this with the for loop below.
index_of_item = 0
row_ = 3
for i in range(int(len(buttons) / NO_OF_COLUMNS)):
    for column_ in range(0, NO_OF_COLUMNS):
        buttons[index_of_item].grid(row=row_, column=column_, sticky='nsew')
        index_of_item += 1
    row_ -= 1

# We clear the list after its job is done.
buttons.clear()

# The main loop.
screen.mainloop()
