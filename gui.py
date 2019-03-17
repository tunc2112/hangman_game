import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
import os
import words_core


class MainWindow(object):
	def __init__(self):
		self.root_width = 490
		self.root_height = 500
		self.BG = "black"

		self.root = tk.Tk()
		self.root.wm_title("Hangman game")
		self.root.resizable(0,0)
		self.root.geometry("{w}x{h}".format(w=self.root_width, h=self.root_height))
		self.root.configure(background=self.BG)

		self.game_core = words_core.hangman_core("words.txt")
		self.a_game = words_core.hangman_game(self.game_core.get_random_word())
		# print(self.a_game.word_to_guess)

		self.show_logo()
		self.show_hangman()
		self.show_guess_word_frame()
		self.show_characters_pad()

		self.root.mainloop()

	def show_logo(self):
		self.logo_image = ImageTk.PhotoImage(Image.open("img/hangman_logo.png"))  # 450 * 120
		self.logo = tk.Label(self.root, image=self.logo_image, bg=self.BG,
		width=self.root_width)
		# self.logo.place(x=(self.root_width-self.logo_image.width())//2, y=0)
		self.logo.grid(row=0, column=0, sticky='nsew', columnspan=2)

	def show_hangman(self):
		self.hangman_images = []
		for i in range(self.a_game.max_incorrect_guesses+1):
			self.hangman_images.append(ImageTk.PhotoImage(Image.open("img/hangman{:0>2}.png".format(i))))  # 250 * 300

		self.hangman_frame = tk.Label(self.root, image=self.hangman_images[0], bg='black', 
			width=self.hangman_images[0].width(), height=self.hangman_images[0].height())
		self.hangman_frame.grid(row=1, column=0, sticky='nsw')

	def show_guess_word_frame(self):
		self.guessing_frame = tk.Frame(self.root, width=len(self.a_game.word_to_guess), height=50, bg=self.BG)  #"red")
		self.guessing_frame.grid(row=2, column=0, sticky='nsew', columnspan=2)

		self.guessing_word = [None] * len(self.a_game.word_to_guess)
		for i in range(len(self.guessing_word)):
			self.guessing_word[i] = tk.Label(self.guessing_frame, width=2, text="__", font="Consolas 24", bg=self.BG, fg="white")
			self.guessing_word[i].grid(row=0, column=i)

	def show_characters_pad(self):
		self.char_image = [ImageTk.PhotoImage(Image.open("img/png/btn_{}.png".format(chr(i+97)))) for i in range(26)]
		self.char_btn = [None] * 26
		self.char_btn_bg = [None] * 26
		
		self.btn_table = tk.Frame(self.root, bg=self.BG)
		self.btn_table.grid(row=1, column=1, sticky='nsw')

		for i in range(len(self.char_btn)):
			self.char_btn_bg[i] = tk.Frame(self.btn_table, bg=self.BG, width=self.char_image[i].width(), height=self.char_image[i].height())

			self.char_btn[i] = tk.Button(self.char_btn_bg[i], bg=self.BG, relief="flat", borderwidth=0, image=self.char_image[i],
				command=lambda i=i: self.check_guess(i))
			
			self.char_btn_bg[i].grid(row=i//5, column=i%5)
			self.char_btn[i].pack()

	def check_guess(self, char_id):
		self.char_btn[char_id].pack_forget()

		char = chr(char_id+97)
		if char in self.a_game.chars_list:
			cnt_opened_chars = 0
			for i in range(len(self.guessing_word)):
				if char == self.a_game.word_to_guess[i]:
					self.guessing_word[i].configure(text=char)

				# print(self.guessing_word[i]["text"])
				if self.guessing_word[i]["text"] != '__':
					cnt_opened_chars += 1

			if cnt_opened_chars == len(self.guessing_word):
				self.end_game()
				messagebox.showinfo("Game over", "Tada! You have completed the game!")
		else:
			self.a_game.incorrect_guesses += 1
			# print(self.a_game.incorrect_guesses)
			self.hangman_frame.configure(image=self.hangman_images[self.a_game.incorrect_guesses])
			if self.a_game.is_gameover():
				self.end_game()
				messagebox.showinfo("Game over", "BOUM! Game over!\nThe answer is {}.".format(self.a_game.word_to_guess))

	def end_game(self):
		for i in range(26):
			self.char_btn[i].config(state="disabled")
