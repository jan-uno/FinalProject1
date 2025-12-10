from PyQt6.QtWidgets import *
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Function to initialize the GUI
        Setting the error messages to be invisible
        and setting the further input and label boxes to be invisible
        and putting score labels and inputs into a list
        """

        super().__init__()
        self.setupUi(self)

        # set input and labels boxes to be invisible
        self.score1_input.setVisible(False)
        self.score2_input.setVisible(False)
        self.score3_input.setVisible(False)
        self.score4_input.setVisible(False)

        self.score1_label.setVisible(False)
        self.score2_label.setVisible(False)
        self.score3_label.setVisible(False)
        self.score4_label.setVisible(False)

        # submitted text hidden
        self.bottom_info_label.setVisible(False)
        # submit button hidden
        self.submit_pushButton.setVisible(False)

        # error messages hidden
        self.error_message_name.setVisible(False)
        self.error_message_attempts.setVisible(False)
        self.error_message_score1.setVisible(False)
        self.error_message_score2.setVisible(False)
        self.error_message_score3.setVisible(False)
        self.error_message_score4.setVisible(False)


        # scores into a list
        self.__score_inputs_list = [
            self.score1_input,
            self.score2_input,
            self.score3_input,
            self.score4_input,
        ]

        # labels to a list
        self.__score_labels_list = [
            self.score1_label,
            self.score2_label,
            self.score3_label,
            self.score4_label,
        ]

        self.__num_scores_expected = 0

        self.continue_pushButton.clicked.connect(lambda: self.continue_button())
        self.submit_pushButton.clicked.connect(lambda: self.submit())

    def continue_button(self) -> None:
        """
        Function gets the student name and the number of attempts they input
        making sure the input is correct and prompting them to redo if not (exception handling).
        It then shows the number of attempts corresponding with what they input.
        Making them unable to edit the name and number of attempts and removing
        the continue button
        :return: None
        """

        student_name = self.student_name_input.text().strip()
        num_attempts = self.attempts_input.text()

        # resets error messages
        self.error_message_name.setVisible(False)
        self.error_message_attempts.setVisible(False)

        input_is_correct = True

        if student_name == "":
            self.error_message_name.setText("Student name cannot be empty.")
            self.error_message_name.setStyleSheet("color: red;")
            self.error_message_name.setVisible(True)
            input_is_correct = False

        try:
            num_attempts = int(num_attempts)

            if num_attempts <=0:
                self.error_message_attempts.setText("Number of attempts cannot be less than 1.")
                self.error_message_attempts.setStyleSheet("color: red;")
                self.error_message_attempts.setVisible(True)
                input_is_correct = False

            if num_attempts > 4:
                self.error_message_attempts.setText("Number of attempts cannot be more than 4.")
                self.error_message_attempts.setStyleSheet("color: red;")
                self.error_message_attempts.setVisible(True)
                input_is_correct = False

        except ValueError:
            self.error_message_attempts.setText("Number of attempts must be an integer.")
            self.error_message_attempts.setStyleSheet("color: red;")
            self.error_message_attempts.setVisible(True)
            input_is_correct = False


        if not input_is_correct:
            return

        # dynamically shows scores
        for i in range(num_attempts):
            self.__score_inputs_list[i].setVisible(True)
            self.__score_labels_list[i].setVisible(True)

        # hides scores not needed
        for i in range(num_attempts, 4):
            self.__score_inputs_list[i].setVisible(False)
            self.__score_labels_list[i].setVisible(False)

        # name and input cannot be changed
        self.student_name_input.setReadOnly(True)
        self.attempts_input.setReadOnly(True)
        self.score1_input.setFocus()

        # continue button is hidden
        # submit button is shown
        self.continue_pushButton.setVisible(False)
        self.submit_pushButton.setVisible(True)

        self.__num_scores_expected = num_attempts



    def submit(self) -> None:
        """
        This function gets the scores and uses exception handling for errors
        It then takes the inputs into the results.csv file
        It then computes their highest score
        :return: None
        """


        score_entered = self.__num_scores_expected # gets scores
        scores = [] # empty list for scores
        is_correct = True

        score_errors_list = [
            self.error_message_score1,
            self.error_message_score2,
            self.error_message_score3,
            self.error_message_score4,
        ]

        # hide previous error messages
        for label in score_errors_list:
            label.setVisible(False)

        # loop through the score inputs as dictated by the scores entered
        for i in range(score_entered):
            input_field = self.__score_inputs_list[i]
            error_label = score_errors_list[i]
            score_text = input_field.text().strip()


            if score_text == "":
                error_label.setText("Score cannot be empty.")
                error_label.setStyleSheet("color: red;")
                error_label.setVisible(True)
                is_correct = False
                continue

            try:
                score = int(score_text)

                if score < 0 or score > 100:
                    raise ValueError("Score must be between 0 and 100.")

                scores.append(score)

            except ValueError:
                error_label.setText("Score must be an integer.")
                error_label.setStyleSheet("color: red;")
                error_label.setVisible(True)

                is_correct = False

        if not is_correct:
            return

        if is_correct:
            self.bottom_info_label.setText("Submitted")
            self.bottom_info_label.setStyleSheet("color: green;")
            self.bottom_info_label.setVisible(True)


        student_name = self.student_name_input.text().strip()

        # get the max score
        max_score = max(scores)

        # fills the data with N/A for unused attempts (fewer than four attempts)
        score_results = scores + ['N/A'] * (4 - len(scores))

        # formats the data as Student Name, Score 1, Score 2, Score 3, Score 4, Max Score
        output = (f'{student_name},{score_results[0]},{score_results[1]},{score_results[2]},{score_results[3]},'
                  f'{max_score}\n')

        with open('results.csv', 'a') as outfile:
            outfile.write(output)