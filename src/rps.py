CHOICES = ['rock', 'paper', 'scissors']

def get_winner(p1_choice, p2_choice):
    """Returns 1 if p1 wins, 2 if p2 wins, 0 for tie."""
    if p1_choice == p2_choice:
        return 0
    if (p1_choice == 'rock' and p2_choice == 'scissors') or \
       (p1_choice == 'paper' and p2_choice == 'rock') or \
       (p1_choice == 'scissors' and p2_choice == 'paper'):
        return 1
    return 2