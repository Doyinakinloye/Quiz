from tkinter import *
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"


class QuizzlerInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        # open a text file where the high score would be stored
        with open("high_score.txt", mode="r") as file:
            self.high_score = int(file.read())
        self.root = Tk()
        self.root.title("Quizzler")
        self.root.config(bg=THEME_COLOR, padx=40, pady=15)
        # Create a canvas where the text would be displayed
        self.canvas = Canvas(width=300, height=300, highlightthickness=0, bg="white")
        self.canvas_text = self.canvas.create_text(150,
                                                   130,
                                                   width=280,
                                                   text="",
                                                   font=("courier", 20, 'bold'))
        self.canvas.grid(column=1, row=1)
        self.score = self.quiz.score
        self.score_board = Label(text=f"score: {self.score}", fg="white", bg=THEME_COLOR, font=("courier", 15, 'bold'))
        self.score_board.grid(row=0, column=2, pady=10)
        # Tick button
        self.tick_button_image = PhotoImage(file="images/true.png")
        self.tick_button = Button(image=self.tick_button_image, highlightthickness=0, command=self.check_if_true)
        self.tick_button.grid(row=2, column=0)
        # Fail button
        self.fail_button_image = PhotoImage(file="images/false.png")
        self.fail_button = Button(image=self.fail_button_image, highlightthickness=0, command=self.check_if_true)
        self.fail_button.grid(row=2, column=2)
        self.Get_Next_Question()
        self.root.mainloop()

    # Display the next question after the button has been pressed
    def Get_Next_Question(self):
        if self.quiz.still_has_questions():
            self.canvas.config(bg="white")
            question_text = self.quiz.next_question()
            # display the text on the canvas
            self.canvas.itemconfig(self.canvas_text, text=question_text)
        else:
            self.canvas.config(bg="white")
            # add the high score to the high score text file
            if self.score > int(self.high_score):
                self.high_score = self.score
                with open("high_score.txt", mode="w") as file:
                    file.write(str(self.score))
            self.canvas.itemconfig(self.canvas_text, text=f"You have reached the end of the game\n"
                                                          f"Highest score: {self.high_score}")
            self.fail_button.config(state="disabled")
            self.tick_button.config(state="disabled")

    # Chech if the answer is correct after the button has been pressed
    def check_if_true(self):
        correct_answer = self.quiz.current_question.answer
        if correct_answer.lower() == "true":
            self.score += 1
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
            pass

        self.score_board.config(text=f"score: {self.score}")
        # Delay for one second and run the "Get_next_question" function
        self.root.after(1000, self.Get_Next_Question)
