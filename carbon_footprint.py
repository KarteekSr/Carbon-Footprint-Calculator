import tkinter
import webbrowser
import customtkinter


class UniversalFrame(customtkinter.CTkFrame):
    def __init__(self, selected = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configure(border_color=("#000000", "#FFFFFF"), border_width=3)
        self.selected = selected
    
    def grid(self) -> None:
        super().grid(column=1, row=1, rowspan=2, columnspan=2, sticky="nsew") 
        

class SpinBoxModern(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 from_: int, to: int,
                 starting_num: int|None = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.MAX_VALUE = to
        self.MIN_VALUE = from_
        if not starting_num:
            self.number = tkinter.StringVar(self, value=str(self.MIN_VALUE))
        else:
            self.number = tkinter.StringVar(self, value=str(starting_num))
        self.number_label = customtkinter.CTkLabel(self, textvariable=self.number, width=50, font=("Calibri", 20))
        self.subtract_button = customtkinter.CTkButton(self, text="-", command=self._subtract, width=30, font=("Calibri", 20))
        self.add_button = customtkinter.CTkButton(self, text="+", command=self._add, width=30, font=("Calibri", 20))
        self.number_label.grid(row=0, column=1)
        self.subtract_button.grid(row=0, column=0)
        self.add_button.grid(row=0, column=2)
        
    def _subtract(self) -> None:
        current_number = int(self.number.get())
        if current_number > self.MIN_VALUE:
            self.set(current_number - 1)
    
    def _add(self) -> None:
        current_number = int(self.number.get())
        if current_number < self.MAX_VALUE:
            self.set(current_number + 1)
    
    def get(self):
        return int(self.number.get())
    
    def set(self, value):
        self.number.set(str(value))


class SpinBoxFrame(UniversalFrame):
    def __init__(self, label1: str, from_: int, to: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i in range(2):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)
        self.label1 = customtkinter.CTkLabel(self, text=label1, font=("Calibri", 25))
        self.from_ = from_
        self.to = to
    
    def grid(self) -> None:
        self.label1.grid(row=0, column=0, columnspan=2)
        self.spin_box = SpinBoxModern(master=self, from_=self.from_, to=self.to)
        self.spin_box.grid(row=1, column=0)
        return super().grid()
    
    def get(self) -> None:
        return self.spin_box.get()


class CheckBoxFrame(UniversalFrame):
    def __init__(self, label1: str, options: tuple, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i in range(3):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        self.label1 = customtkinter.CTkLabel(self, text=label1, font=("Calibri", 25))
        self.checkboxes = []
        for option in options:
            checkbox = customtkinter.CTkCheckBox(self, corner_radius=10, text=option, font=("Calibri", 20))
            self.checkboxes.append(checkbox)
    
    def grid(self) -> None:
        self.label1.grid(row=0, column=0, columnspan=3)
        if self.selected:
            for index in range(len(self.checkboxes)):
                self.checkboxes[index].select()
        
        for index in range(len(self.checkboxes)):
            self.checkboxes[index].grid(row=index//3 + 1, column=index % 3)
        return super().grid()
    
    def get(self) -> list:
        state_of_checkbox = []
        for checkbox in self.checkboxes:
            state_of_checkbox.append(bool(checkbox.get()))
        return state_of_checkbox


class ListBoxFrame(UniversalFrame):
    def __init__(self, label1: str, options: list,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.listbox = customtkinter.CTkOptionMenu(self, values=options, corner_radius=10, font=("Calibri", 20))
        self.label1 = customtkinter.CTkLabel(self, text=label1, font=("Calibri", 25))
        if self.selected:
            self.listbox.set(self.selected)
    
    def grid(self) -> None:
        self.listbox.grid(row=1, column=0)
        self.label1.grid(row=0, column=0)
        return super().grid()

    def get(self) -> str:
        return self.listbox.get()
    

class Main(object):
    """The class that represents the main program
    
    Attributes:

    Methods:
    
    """
    
    def __init__(self) -> None:
        # self.appearance_mode = "Dark"
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")
        self.screen = customtkinter.CTk()
        self.screen.geometry("500x400")
        for i in range(4):
            self.screen.columnconfigure(i, weight=1)
            self.screen.rowconfigure(i, weight=1)
        label = customtkinter.CTkLabel(self.screen, text="Carbon Footprint Calculator", font=("Calibri", 35))
        self.active_frame = 0
        # self.active_frame2 = 0
        # spinbox_frame = SpinBoxFrame(master=self.screen, from_=1, to=15, label1="How many people live with you?", corner_radius=20)
        # spinbox_frame.grid()
        # listbox_frame = ListBoxFrame(master=self.screen, label1="Where do you live?", 
        #                             options=["Large House", "Medium-sized house", "Small house", "Apartment"])
        #listbox_frame.grid()
        self.all_frames = [SpinBoxFrame(master=self.screen, label1="How many people live with you?", from_=0, to=20),
                      ListBoxFrame(master=self.screen, label1="How would you describe your house?", 
                                   options=["Apartment", "Large house", "Medium sized house", "Small house"]),
                      ListBoxFrame(master=self.screen, label1="How often do you eat meat?", 
                                   options=["Daily", "Few times a week", "I am a vegetarian", "I am a vegan and eat only wild meat"]),
                      ListBoxFrame(master=self.screen, label1="What best describes your diet?", options=["Most of my food is prepackaged", "My diet is a good balance of fresh and convenience food", 
                                                                                                         "I eat only fresh, locally grown or hunted food"]),
                      ListBoxFrame(master=self.screen, label1="How often do you use your washing machine?", options=["9 times a week", "4-9 times a week", "1-3 times a week", "I do not have a washing machine"]),
                      ListBoxFrame(master=self.screen, label1="How often do you use your Dishwasher?", options=["9 times a week", "4-9 times a week", "1-3 times a week", "I do not have a Dishwasher"]),
                      SpinBoxFrame(master=self.screen, label1="How many times do you purchase furniture each year? (Enter 0 for second hand furniture)", from_=0, to=20),
                      SpinBoxFrame(master=self.screen, label1="How many trash cans do you fill per week?", from_=0, to=4),
                      CheckBoxFrame(master=self.screen, label1="Which of these do you recycle?", options=("Steel", "Paper", "Plastic", "Aluminium", "Glass", "Food Waste (Compost)")),
                      ListBoxFrame(master=self.screen, label1="How much do you travel with your personal vehicle per year?", 
                                   options=["Less than 1000 miles", "1000-10,000 miles", "10,000-15,000 miles", "More than 15,000 miles", "I don't have a car"]),
                      ListBoxFrame(master=self.screen, label1="How much do you travel by public transport per year?", 
                                   options=["Less than 1000 miles", "1000-10,000 miles", "10,000-15,000 miles", "15,000-20,000 miles", "More than 20,000 miles", "I don't travel"]),
                      ListBoxFrame(master=self.screen, label1="How much do you travel by flights per year?", 
                                   options=["Within my state", "Nearby state or country", "Another continent"])]
        self.selected_items = [None] * len(self.all_frames)
        self.length_index = len(self.all_frames) - 1
        for frame in self.all_frames:
            frame.grid()
        self.show_frame(self.all_frames[self.active_frame])   # active_frame is 0
        # radiobutton_frame = CheckBoxFrame(master=self.screen, 
        #                                     options=("Glass", "Plastic", "Paper", "Aluminium", 
        #                                             "Steel", "Food Waste (Compost)"),
        #                                     label1="Which of these materials do you recycle")
        # radiobutton_frame.grid()
        label.grid(row=0, column=1, columnspan=2, sticky="nsew")
        self.mode_btn = customtkinter.CTkSegmentedButton(self.screen, values=["Light", "Dark"], 
                                                         command=self.mode_button, corner_radius=8, 
                                                         font=("Calibri", 17), fg_color=["#999999", "#404040"])
        self.mode_btn.set("Dark")
        self.next_button = customtkinter.CTkButton(self.screen, corner_radius=8, 
                                              text_color="white", text="Next", height=40, 
                                              font=("Calibri", 17), command=self.next)
        self.next_button.grid(row=3, column=3)
        self.prev_button = customtkinter.CTkButton(self.screen, corner_radius=8, 
                                              text_color="white", text="Previous", height=40, 
                                              font=("Calibri", 17), command=self.prev)
        self.prev_button.grid(row=3, column=0)
        self.mode_btn.grid(row=0, column=0)
        self.screen = self.screen
        
    def next(self) -> None:
        frame = self.all_frames[self.active_frame]
        self.selected_items[self.active_frame] = frame.get()
        if self.active_frame == self.length_index:
            return None
        else:
            if self.active_frame == self.length_index - 1:
                self.next_button.configure(text="Calculate", command=self.calculate_carbon_footprint)
            self.active_frame += 1
        selected_item = self.selected_items[self.active_frame]
        if selected_item:
            self.all_frames[self.active_frame].selected = selected_item
        frame = self.all_frames[self.active_frame]
        self.show_frame(frame)
        
    def prev(self) -> None:
        if self.active_frame == 0:
            return None
        else:
            if self.active_frame == self.length_index:
                self.next_button.configure(text="Next", command=self.next)
            self.active_frame -= 1
        selected_item = self.selected_items[self.active_frame]
        if selected_item:
            self.all_frames[self.active_frame].selected = selected_item
        self.show_frame(self.all_frames[self.active_frame])
    
    def calculate_carbon_footprint(self):
        frame = self.all_frames[self.active_frame]
        self.selected_items[self.active_frame] = frame.get()
        carbon_points = 0
        selected_item_first = self.selected_items[0]
        if selected_item_first > 5:
            carbon_points += 2
        else:
            carbon_points += 14 - (2*selected_item_first)
        selected_second_question = {"Apartment": 2,
                                    "Small": 4,
                                    "Medium": 7,
                                    "Large": 10}
        carbon_points += selected_second_question[self.selected_items[1].split()[0]]
        selected_second_question.clear()
        selected_third_question = {"Daily": 10,
                                   "Few times a week": 8,
                                   "I am a vegetarian": 4,
                                   "I am a vegan and eat only wild meat": 2}
        carbon_points += selected_third_question[self.selected_items[2]]
        selected_third_question.clear()
        selected_fourth_question = {"Most of my food is prepackaged": 12,
                                    "My diet is a good balance of fresh and convenience food": 6,
                                    "I eat only fresh, locally grown or hunted food": 2}
        carbon_points += selected_fourth_question[self.selected_items[3]]
        selected_fourth_question.clear()
        selected_five_and_six_questions = {"9 times a week": 3,
                                           "4-9 times a week": 2,
                                           "1-3 times a week": 1}
        carbon_points += selected_five_and_six_questions.get(self.selected_items[4], 0)
        carbon_points += selected_five_and_six_questions.get(self.selected_items[5], 0)
        selected_five_and_six_questions.clear()
        seventh_selected_item = self.selected_items[6]
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
        selected_eigth_item = self.selected_items[7]
        if selected_eigth_item == 0:
            carbon_points += 5
        else:
            carbon_points += (selected_eigth_item + 1) * 10
        selected_ninth_question = self.selected_items[8].count(True)
        carbon_points += 4*(6-selected_ninth_question)
        selected_tenth_question = {"Less than 1000 miles": 4,
                                   "1000-10,000 miles": 6,
                                   "10,000-15,000 miles": 10,
                                   "More than 15,000 miles": 12,
                                   "I don't have a car": 0}
        carbon_points += selected_tenth_question[self.selected_items[9]]
        selected_tenth_question.clear()
        selected_11_question = {"Less than 1000 miles": 2,
                                "1000-10,000 miles": 4,
                                "10,000-15,000 miles": 6,
                                "15,000-20,000 miles": 10,
                                "More than 20,000 miles": 12,
                                "I don't travel": 0}
        carbon_points += selected_11_question[self.selected_items[10]]
        selected_11_question.clear()
        selected_12_question = {"Within my state": 2,
                                "Nearby state or country": 6,
                                "Another continent": 20}
        carbon_points += selected_12_question[self.selected_items[11]]
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
        self.screen.destroy()
        new_screen.mainloop()
    
    def mode_button(self, selected):
        customtkinter.set_appearance_mode(selected)
    
    def show_frame(self, frame: customtkinter.CTkFrame):
        frame.tkraise()
        
    def run(self):
        self.screen.mainloop()


if __name__ == "__main__":
    main = Main()
    main.run()
