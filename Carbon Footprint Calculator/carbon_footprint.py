import tkinter
import webbrowser
import customtkinter


class UniversalFrame(customtkinter.CTkFrame):
    """The class that represents the basic frame of each question

    Methods:
        grid: Grid the Frame on the required row and column.
    """
    def __init__(self, selected = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configure(border_color=("#000000", "#FFFFFF"), border_width=3)
    
    def grid(self) -> None:
        """Grid the frame"""
        super().grid(column=1, row=1, rowspan=2, columnspan=2, sticky="nsew") 
        

class SpinBoxModern(customtkinter.CTkFrame):
    """The class which represents the spinbox used in the questions
    
    Methods:
        get: Return the value of the spinbox
        set: Set the value of the spinbox
    """    
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 from_: int, to: int,
                 starting_num: int|None = None,
                 **kwargs) -> None:
        """Initialize the object by defining important variables

        Args:
            from_ (int): The minimum value of the spinbox
            to (int): The maximum value of the spinbox
            width (int, optional): The width of the spinbox. Defaults to 100.
            height (int, optional): The height of the spinbox. Defaults to 32.
            starting_num (int | None, optional): The number to be displayed when no value is already selected. Defaults to None 
                (it is set to `from_`)
        """
        super().__init__(*args, width=width, height=height, **kwargs)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        
        self._MAX_VALUE = to
        self._MIN_VALUE = from_
        
        if starting_num is None:
            # Cannot use the `not` keyword since 0 will also come True then.
            self._number = tkinter.StringVar(self, value=str(self._MIN_VALUE))
        else:
            self._number = tkinter.StringVar(self, value=str(starting_num))
        
        # Define and grid the widgets of the spinbox
        self._number_label = customtkinter.CTkLabel(self, textvariable=self._number, width=50, font=("Calibri", 20))
        self._subtract_button = customtkinter.CTkButton(self, text="-", command=self._subtract, width=30, font=("Calibri", 20))
        self._add_button = customtkinter.CTkButton(self, text="+", command=self._add, width=30, font=("Calibri", 20))
        self._number_label.grid(row=0, column=1)
        self._subtract_button.grid(row=0, column=0)
        self._add_button.grid(row=0, column=2)
        
    def _subtract(self) -> None:
        """Subtract the value of the spinbox by 1, if the value is greater than the `_MIN_VALUE`"""
        current_number = int(self._number.get())
        if current_number > self._MIN_VALUE:
            self.set(current_number - 1)
    
    def _add(self) -> None:
        """Add the value of the spinbox by 1, if the value is greater than the `_MAX_VALUE`"""
        current_number = int(self._number.get())
        if current_number < self._MAX_VALUE:
            self.set(current_number + 1)
    
    def get(self) -> int:
        """Return the value of the spinbox"""
        return int(self._number.get())
    
    def set(self, value: int) -> None:
        """Return the value of the spinbox"""
        self._number.set(str(value))


class SpinBoxFrame(UniversalFrame):
    """The class that represents the frame which consists of a question and a spinbox
    
    Methods:
        get: Return the value of the spinbox using the `SpinBoxModern.get()` method
        set: Set the value of the spinbox
        grid: Grid the frame. Override the existing `UniversalFrame.grid()`
    """
    
    def __init__(self, question: str, from_: int, to: int, starting_num: int|None = None, *args, **kwargs) -> None:
        """Initilize the class by defining certain variables

        Args:
            question (str): The question to be displayed on the Frame
            from_ (int): The minimum number of the spinbox
            to (int): The maximum number of the spinbox
            starting_num (int|None): The number to be displayed when no value is already selected. Defaults to None 
                (it is set to `from_`)
        """
        super().__init__(*args, **kwargs)
        
        for i in range(2):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)
        
        self._question = customtkinter.CTkLabel(self, text=question, font=("Calibri", 25))
        self._from_ = from_
        self._to = to
    
    def grid(self) -> None:
        """Grid the frame. Override the existing `UniversalFrame.grid()`"""
        self._question.grid(row=0, column=0, columnspan=2)
        self._spin_box = SpinBoxModern(master=self, from_=self._from_, to=self._to)
        self._spin_box.grid(row=1, column=0)
        return super().grid()
    
    def get(self) -> int:
        """Return the value of the spinbox"""
        return self._spin_box.get()

    def set(self, value: int) -> None:
        """Set the value of the spinbox

        Args:
            value (int): The value of to be set for the spinbox"""
        self._spin_box.set(value)


class CheckBoxFrame(UniversalFrame):
    """The class that represents the frame for the kind of questions which include checkboxes
    
    Methods:
        grid: Grid the checkbox frame. Override the `grid` method of the `UniversalFrame`
        get: Get the values of the checkboxes in the form of a list of bools.
    """
    def __init__(self, question: str, options: tuple, *args, **kwargs) -> None:
        """Initialize the list and create certain variables

        Args:
            question (str): The question to be displayed
            options (tuple): The options (checkboxes)
        """
        super().__init__(*args, **kwargs)
        
        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
            
        self._question = customtkinter.CTkLabel(self, text=question, font=("Calibri", 25))
        self._checkboxes = []
        for option in options:
            checkbox = customtkinter.CTkCheckBox(self, corner_radius=10, text=option, font=("Calibri", 20))
            self._checkboxes.append(checkbox)
    
    def grid(self) -> None:
        """Grid the frame"""
        self._question.grid(row=0, column=0, columnspan=3)
        for index in range(len(self._checkboxes)):
            self._checkboxes[index].grid(row=index//3 + 1, column=index % 3)
        return super().grid()
    
    def get(self) -> list[bool]:
        """Get the value of the checkboxes by a list of bools

        Returns:
            list[bool]: List of bools in the order of the `options` argument. True if checked and False if unchecked
        """
        state_of_checkbox = []
        for checkbox in self._checkboxes:
            state_of_checkbox.append(bool(checkbox.get()))
        return state_of_checkbox


class ListBoxFrame(UniversalFrame):
    """The class that represents the frame with listboxes
    
    Methods:
        grid: Grid the frame. Override the `grid` method of the UniversalFrame
        get: Get the value returned by the listbox"""
    def __init__(self, question: str, options: list,*args, **kwargs) -> None:
        """Initialize the class

        Args:
            question (str): The question to be asked
            options (list): The options in the listbox
        """
        super().__init__(*args, **kwargs)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self._listbox = customtkinter.CTkOptionMenu(self, values=options, corner_radius=10, font=("Calibri", 20))
        self._question = customtkinter.CTkLabel(self, text=question, font=("Calibri", 25))
    
    def grid(self) -> None:
        """Grid the frame"""
        self._listbox.grid(row=1, column=0)
        self._question.grid(row=0, column=0)
        return super().grid()

    def get(self) -> str:
        """Get the value of the listbox"""
        return self._listbox.get()
    

class Main(object):
    """The class that represents the main program
    
    Methods:
        run: Run the program
    """
    
    def __init__(self) -> None:
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        
        self._screen = customtkinter.CTk()
        self._screen.geometry("500x400")
        for i in range(4):
            self._screen.columnconfigure(i, weight=1)
            self._screen.rowconfigure(i, weight=1)
            
        label = customtkinter.CTkLabel(self._screen, text="Carbon Footprint Calculator", font=("Calibri", 35))
        self._active_frame = 0   # The index of the active frame (frame bring displayed)
        
        self._all_frames = [SpinBoxFrame(master=self._screen, question="How many people live with you?", from_=0, to=20),
                      ListBoxFrame(master=self._screen, question="How would you describe your house?", 
                                   options=["Apartment", "Large house", "Medium sized house", "Small house"]),
                      ListBoxFrame(master=self._screen, question="How often do you eat meat?", 
                                   options=["Daily", "Few times a week", "I am a vegetarian", "I am a vegan and eat only wild meat"]),
                      ListBoxFrame(master=self._screen, question="What best describes your diet?", options=["Most of my food is prepackaged", "My diet is a good balance of fresh and convenience food", 
                                                                                                         "I eat only fresh, locally grown or hunted food"]),
                      ListBoxFrame(master=self._screen, question="How often do you use your washing machine?", options=["9 times a week", "4-9 times a week", "1-3 times a week", "I do not have a washing machine"]),
                      ListBoxFrame(master=self._screen, question="How often do you use your Dishwasher?", options=["9 times a week", "4-9 times a week", "1-3 times a week", "I do not have a Dishwasher"]),
                      SpinBoxFrame(master=self._screen, question="How many times do you purchase furniture each year? (Enter 0 for second hand furniture)", from_=0, to=20),
                      SpinBoxFrame(master=self._screen, question="How many trash cans do you fill per week?", from_=0, to=4),
                      CheckBoxFrame(master=self._screen, question="Which of these do you recycle?", options=("Steel", "Paper", "Plastic", "Aluminium", "Glass", "Food Waste (Compost)")),
                      ListBoxFrame(master=self._screen, question="How much do you travel with your personal vehicle per year?", 
                                   options=["Less than 1000 miles", "1000-10,000 miles", "10,000-15,000 miles", "More than 15,000 miles", "I don't have a car"]),
                      ListBoxFrame(master=self._screen, question="How much do you travel by public transport per year?", 
                                   options=["Less than 1000 miles", "1000-10,000 miles", "10,000-15,000 miles", "15,000-20,000 miles", "More than 20,000 miles", "I don't travel"]),
                      ListBoxFrame(master=self._screen, question="How much do you travel by flights per year?", 
                                   options=["Within my state", "Nearby state or country", "Another continent"])]
        
        self._length_index = len(self._all_frames) - 1
        
        for frame in self._all_frames:
            frame.grid()
            
        self._show_frame(self._all_frames[self._active_frame])   # active_frame is 0
        
        label.grid(row=0, column=1, columnspan=2, sticky="nsew")
        
        self._mode_btn = customtkinter.CTkSegmentedButton(self._screen, values=["Light", "Dark"], 
                                                         command=self._mode_button, corner_radius=8, 
                                                         font=("Calibri", 17), fg_color=["#999999", "#404040"])
        self._mode_btn.set("Dark")
        self._mode_btn.grid(row=0, column=0)
        
        self._next_button = customtkinter.CTkButton(self._screen, corner_radius=8, 
                                              text_color="white", text="Next", height=40, 
                                              font=("Calibri", 17), command=self._next)
        self._next_button.grid(row=3, column=3)
        
        self._prev_button = customtkinter.CTkButton(self._screen, corner_radius=8, 
                                              text_color="white", text="Previous", height=40, 
                                              font=("Calibri", 17), command=self._prev)
        self._prev_button.grid(row=3, column=0)
        
        self._screen = self._screen
        
    def _next(self) -> None:
        """Display the next frame of the active frame using `self._all_frame`"""
        # We do not need to check if the selected item is the last frame or not, since the command is being changed when the active frame
        # has become last because we need to calculate then.
        if self._active_frame == self._length_index - 1:
            # If the active frame is the second last frame, the next frame is the last frame, so we need to set the text of the button
            # to Calculate
            self._next_button.configure(text="Calculate", command=self._calculate_carbon_footprint)
        self._active_frame += 1
        frame = self._all_frames[self._active_frame]    # The current new frame
        self._show_frame(frame)
        
    def _prev(self) -> None:
        """Display the previous frame using the `self._all_frames`"""
        if self._active_frame == 0:
            # If the active frame is the first frame, do nothing
            return None
        else:
            if self._active_frame == self._length_index:
                # If the current frame is the last frame, then we need to change the text and the command of the button to next
                self._next_button.configure(text="Next", command=self._next)
            self._active_frame -= 1
        self._show_frame(self._all_frames[self._active_frame])
    
    def _calculate_carbon_footprint(self) -> None:
        """Calculate the new carbon footprint and create a new screen"""
        
        selected_items = []    # This will help in calculating carbon footprint
        for frame in self._all_frames:
            selected_items.append(frame.get())
        
        # Logic for calculating carbon footprint (all the values have been taken from wikihow.com)
        frame = self._all_frames[self._active_frame]
        selected_items[self._active_frame] = frame.get()
        carbon_points = 0
        selected_item_first = selected_items[0]
        if selected_item_first > 5:
            carbon_points += 2
        else:
            carbon_points += 14 - (2*selected_item_first)
        selected_second_question = {"Apartment": 2,
                                    "Small": 4,
                                    "Medium": 7,
                                    "Large": 10}
        carbon_points += selected_second_question[selected_items[1].split()[0]]
        selected_second_question.clear()
        selected_third_question = {"Daily": 10,
                                   "Few times a week": 8,
                                   "I am a vegetarian": 4,
                                   "I am a vegan and eat only wild meat": 2}
        carbon_points += selected_third_question[selected_items[2]]
        selected_third_question.clear()
        selected_fourth_question = {"Most of my food is prepackaged": 12,
                                    "My diet is a good balance of fresh and convenience food": 6,
                                    "I eat only fresh, locally grown or hunted food": 2}
        carbon_points += selected_fourth_question[selected_items[3]]
        selected_fourth_question.clear()
        selected_five_and_six_questions = {"9 times a week": 3,
                                           "4-9 times a week": 2,
                                           "1-3 times a week": 1}
        carbon_points += selected_five_and_six_questions.get(selected_items[4], 0)
        carbon_points += selected_five_and_six_questions.get(selected_items[5], 0)
        selected_five_and_six_questions.clear()
        seventh_selected_item = selected_items[6]
        if seventh_selected_item > 7:
            carbon_points += 10
        elif 5 <= seventh_selected_item <= 7:
            carbon_points += 8
        elif 3 <= seventh_selected_item < 5:
            carbon_points += 6
        elif 0 < seventh_selected_item < 3:
            carbon_points += 4
        else:
            carbon_points += 2
        selected_eigth_item = selected_items[7]
        if selected_eigth_item == 0:
            carbon_points += 5
        else:
            carbon_points += (selected_eigth_item + 1) * 10
        selected_ninth_question = selected_items[8].count(True)
        carbon_points += 4*(6-selected_ninth_question)
        selected_tenth_question = {"Less than 1000 miles": 4,
                                   "1000-10,000 miles": 6,
                                   "10,000-15,000 miles": 10,
                                   "More than 15,000 miles": 12,
                                   "I don't have a car": 0}
        carbon_points += selected_tenth_question[selected_items[9]]
        selected_tenth_question.clear()
        selected_11_question = {"Less than 1000 miles": 2,
                                "1000-10,000 miles": 4,
                                "10,000-15,000 miles": 6,
                                "15,000-20,000 miles": 10,
                                "More than 20,000 miles": 12,
                                "I don't travel": 0}
        carbon_points += selected_11_question[selected_items[10]]
        selected_11_question.clear()
        selected_12_question = {"Within my state": 2,
                                "Nearby state or country": 6,
                                "Another continent": 20}
        carbon_points += selected_12_question[selected_items[11]]
        new_screen = customtkinter.CTk()
        new_screen.geometry("500x300")
        if carbon_points <= 60:
            label = customtkinter.CTkLabel(master=new_screen, 
                                           text=f"Your carbon footprint points is {carbon_points},\n you are making a small impact on this planet",
                                           font=("Calibri", 25))
        else:
            label = customtkinter.CTkLabel(master=new_screen, text=f"Your carbon footprint points is {carbon_points},\n You need to improve your lifestyle as your points are more than 60",
                                           font=("Calibri", 25))
        new_screen.rowconfigure(0, weight=1)
        new_screen.rowconfigure(1, weight=3)
        new_screen.rowconfigure(2, weight=1)
        new_screen.rowconfigure(3, weight=1)
        for i in range(4):
            new_screen.columnconfigure(i, weight=1)
        label.grid(row=1, column=1, columnspan=2,sticky="nsew")
        button = customtkinter.CTkButton(master=new_screen, text="Ways to reduce carbon footprint", 
                                         command=lambda: webbrowser.open("https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiQs8T6rtr8AhVSUGwGHSkQDP4QFnoECAgQAw&url=https%3A%2F%2Fsustainability.georgetown.edu%2Fcommunity-engagement%2Fthings-you-can-do%2F&usg=AOvVaw2oNPGlj1Svz0KrBvbLzLBk"),
                                         font=("Calibri", 20))
        button.grid(row=2, column=1, columnspan=2)
        self._screen.destroy()
        new_screen.mainloop()
    
    def _mode_button(self, selected: str) -> None:
        """Light or dark mode

        Args:
            selected (str): Light or dark mode (this argument is passed on its own)"""
        customtkinter.set_appearance_mode(selected)
    
    def _show_frame(self, frame: customtkinter.CTkFrame) -> None:
        """Shows the frame passed in the argument

        Args:
            frame (customtkinter.CTkFrame): The frame to be shown"""
        frame.tkraise()
        
    def run(self) -> None:
        """Run the program"""
        self._screen.mainloop()


if __name__ == "__main__":
    main = Main()
    main.run()
