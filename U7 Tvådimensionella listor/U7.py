def print_board(board):
    """Skriver ut spelbrädet."""
    for row in range(3):
        print(" | ".join(board[row]))
        if row < 2:
            print("-" * 5)

def check_winner(board):
    """Kontrollerar om det finns en vinnare."""
    # Kolla rader
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]

    # Kolla kolumner
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]

    # Kolla diagonaler
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    return None

def is_full(board):
    """Kontrollerar om brädet är fullt."""
    for row in board:
        if " " in row:
            return False
    return True

def main():
    """Huvudfunktion som kör spelet."""
    # Initiera ett tomt 3x3 bräde
    board = [[" " for _ in range(3)] for _ in range(3)]

    # Spelare X börjar
    current_player = "X"

    while True:
        print_board(board)
        print(f"Spelare {current_player}'s tur")

        # Be spelaren om en position
        try:
            row = int(input("Välj rad (0, 1, 2): "))
            col = int(input("Välj kolumn (0, 1, 2): "))
        except ValueError:
            print("Felaktig inmatning! Ange ett heltal.")
            continue

        # Kontrollera giltighet
        if row < 0 or row > 2 or col < 0 or col > 2 or board[row][col] != " ":
            print("Ogiltigt drag! Försök igen.")
            continue

        # Gör draget
        board[row][col] = current_player

        # Kolla om någon har vunnit
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Spelare {winner} vinner!")
            break

        # Kolla om brädet är fullt
        if is_full(board):
            print_board(board)
            print("Det är oavgjort!")
            break

        # Byt spelare
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()