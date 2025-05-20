import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Redefined")

        # Initialize board and player data
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.moves = {"X": [], "O": []}
        self.current_player = "X"

        # Build the UI grid
        for row in range(3):
            for col in range(3):
                btn = tk.Button(root, text=" ", font=('Arial', 32), width=5, height=2,
                                command=lambda r=row, c=col: self.make_move(r, c))
                btn.grid(row=row, column=col)
                self.buttons[row][col] = btn

    def make_move(self, row, col):
        # Prevent move if cell is already taken
        if self.board[row][col] != " ":
            return

        # FIFO: remove oldest move if already 3 on board
        if len(self.moves[self.current_player]) == 3:
            old_row, old_col = self.moves[self.current_player].pop(0)
            self.board[old_row][old_col] = " "
            self.buttons[old_row][old_col].config(text=" ")

        # Record move
        self.board[row][col] = self.current_player
        self.moves[self.current_player].append((row, col))
        self.buttons[row][col].config(text=self.current_player)

        # Check for a win
        if self.check_win(self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
            return

        # Switch to the other player
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_win(self, player):
        b = self.board
        # Check rows, columns
        for i in range(3):
            if all(b[i][j] == player for j in range(3)):
                return True
            if all(b[j][i] == player for j in range(3)):
                return True
        # Check diagonals
        if all(b[i][i] == player for i in range(3)):
            return True
        if all(b[i][2 - i] == player for i in range(3)):
            return True
        return False

    def reset_game(self):
        # Reset everything to start a new game
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.moves = {"X": [], "O": []}
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ")

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
    
    
    