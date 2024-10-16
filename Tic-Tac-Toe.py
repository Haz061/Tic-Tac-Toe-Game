import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        self.board = [None] * 9
        self.current_player = 'X'
        self.game_active = True  # Allow interaction from the start

        # Default colors for X and O
        self.color_x = '#FF0000'  # Red
        self.color_o = '#0000FF'  # Blue
        self.bg_color = '#FFFFFF'  # Default background color (white)

        # Expanded color options
        self.colors = [
            '#FF0000', '#FF7F00', '#FFFF00', '#7FFF00', '#00FF00', 
            '#00FF7F', '#00FFFF', '#007FFF', '#0000FF', '#7F00FF', 
            '#FF00FF', '#FF007F', '#FFFFFF', '#000000', '#C0C0C0',
            '#808080', '#800000', '#FF4500', '#FFD700', '#ADFF2F',
            '#8A2BE2', '#5F9EA0', '#D2691E', '#FF6347', '#4682B4',
            '#FF1493', '#00BFFF', '#1E90FF', '#7FFF00', '#FFD700'
        ]
        
        self.buttons = [tk.Button(master, text='', font=('Arial', 48), width=3, height=1,
                                   command=lambda i=i: self.make_move(i)) for i in range(9)]

        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.master, text="Select Color for X", command=self.open_color_selection_x).grid(row=0, column=0, columnspan=3)
        tk.Button(self.master, text="Select Color for O", command=self.open_color_selection_o).grid(row=1, column=0, columnspan=3)
        tk.Button(self.master, text="Select Grid Background Color", command=self.open_bg_color_selection).grid(row=2, column=0, columnspan=3)
        tk.Button(self.master, text="Reset Text Color", command=self.reset_text_color).grid(row=3, column=0, columnspan=3)
        tk.Button(self.master, text="Reset Background Color", command=self.reset_bg_color).grid(row=4, column=0, columnspan=3)

        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row=row + 5, column=col, sticky='nsew')

        # Configure row and column weights to make the grid square
        for i in range(3):
            self.master.grid_rowconfigure(i + 5, weight=1)
            self.master.grid_columnconfigure(i, weight=1)

    def open_bg_color_selection(self):
        color_window = tk.Toplevel(self.master)
        color_window.title("Select Background Color")

        tk.Label(color_window, text="Select Background Color:").grid(row=0, column=0, columnspan=5, pady=(10, 0))
        for i, color in enumerate(self.colors):
            button = tk.Button(color_window, bg=color, width=3, height=1,
                               command=lambda c=color: self.set_bg_color(c, color_window))
            row = 1 + i // 5  # Create a new row every 5 colors
            col = i % 5
            button.grid(row=row, column=col, padx=5, pady=5)

    def set_bg_color(self, color, color_window):
        self.bg_color = color  # Store selected background color
        for button in self.buttons:
            button.config(bg=self.bg_color)  # Change the background color of the grid buttons
        color_window.destroy()  # Close the color selection window

    def reset_bg_color(self):
        self.bg_color = '#FFFFFF'  # Reset to default background color (white)
        for button in self.buttons:
            button.config(bg=self.bg_color)  # Change the background color of the grid buttons

    def open_color_selection_x(self):
        color_window = tk.Toplevel(self.master)
        color_window.title("Select Color for X")

        tk.Label(color_window, text="Select Color for X:").grid(row=0, column=0, columnspan=5, pady=(10, 0))
        for i, color in enumerate(self.colors):
            button = tk.Button(color_window, bg=color, width=3, height=1,
                               command=lambda c=color: self.set_color_x(c, color_window))
            row = 1 + i // 5  # Create a new row every 5 colors
            col = i % 5
            button.grid(row=row, column=col, padx=5, pady=5)

    def set_color_x(self, color, color_window):
        self.color_x = color
        self.update_existing_colors('X')  # Update colors on the board for X
        color_window.destroy()  # Close the X color selection window

    def open_color_selection_o(self):
        color_window = tk.Toplevel(self.master)
        color_window.title("Select Color for O")

        tk.Label(color_window, text="Select Color for O:").grid(row=0, column=0, columnspan=5, pady=(10, 0))
        for i, color in enumerate(self.colors):
            button = tk.Button(color_window, bg=color, width=3, height=1,
                               command=lambda c=color: self.set_color_o(c, color_window))
            row = 1 + i // 5  # Create a new row every 5 colors
            col = i % 5
            button.grid(row=row, column=col, padx=5, pady=5)

    def set_color_o(self, color, color_window):
        self.color_o = color
        self.update_existing_colors('O')  # Update colors on the board for O
        color_window.destroy()  # Close the O color selection window

    def update_existing_colors(self, player):
        for i, cell in enumerate(self.board):
            if cell == player:
                color = self.color_x if player == 'X' else self.color_o
                self.buttons[i].config(fg=color)

    def reset_text_color(self):
        # Store previous colors for updating existing buttons
        previous_color_x = self.color_x
        previous_color_o = self.color_o

        self.color_x = '#FF0000'  # Reset to default color for X
        self.color_o = '#0000FF'  # Reset to default color for O

        # Update existing buttons to reflect the new text colors
        for i in range(9):
            if self.board[i] == 'X':
                self.buttons[i].config(fg=self.color_x)
            elif self.board[i] == 'O':
                self.buttons[i].config(fg=self.color_o)

    def make_move(self, index):
        if self.game_active and self.board[index] is None:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player,
                                        fg=self.color_x if self.current_player == 'X' else self.color_o)
            winner = self.check_winner()
            if winner:
                self.highlight_winner(winner)
                self.show_end_game_dialog(f"{self.current_player} wins!")  # Show end game dialog for win
                self.game_active = False  # Set the game to inactive
            elif all(cell is not None for cell in self.board):
                self.show_end_game_dialog("It's a draw!")  # Show end game dialog for draw
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(self.board[i] == self.current_player for i in combo):
                return combo  # Return the winning combination
        return None

    def highlight_winner(self, combo):
        for i in combo:
            self.buttons[i].config(bg='#90EE90')  # Highlight winning buttons in light green

    def show_end_game_dialog(self, message):
        self.dialog = tk.Toplevel(self.master)
        self.dialog.title("Game Over")
        self.dialog.transient(self.master)  # Keep the dialog on top

        tk.Label(self.dialog, text=message, padx=20, pady=20).pack()

        play_again_button = tk.Button(self.dialog, text="Play Again", command=lambda: [self.reset_game(), self.dialog.destroy()])
        play_again_button.pack(side=tk.LEFT, padx=20, pady=10)

        exit_button = tk.Button(self.dialog, text="Exit", command=self.master.quit)
        exit_button.pack(side=tk.RIGHT, padx=20, pady=10)

        # Ensure dialog remains on top and blocks interaction with the main window
        self.dialog.focus_set()  # Make the dialog focused
        self.dialog.grab_set()   # Block interaction with the main window

    def reset_game(self):
        self.board = [None] * 9
        for button in self.buttons:
            button.config(text='', bg=self.bg_color)  # Reset button text and color
        self.current_player = 'X'
        self.game_active = True  # Reset game to active state
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
