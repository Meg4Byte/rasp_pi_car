import curses

def main(stdscr):
    # Initialize curses
    curses.curs_set(1)  # Show the cursor
    
    # Get the size of the terminal window
    height, width = stdscr.getmaxyx()
    
    # Prompt the user for input
    stdscr.addstr(height // 2, 0, "Enter something: ")
    
    # Create an input window
    input_win = curses.newwin(1, width - len("Enter something: ") - 1, height // 2, len("Enter something: "))
    
    # Enable input for the input window
    curses.curs_set(2)  # Show cursor in input window
    input_win.refresh()
    
    # Get user input
    user_input = input_win.getstr(0, 0)
    
    # Print the user's input
    stdscr.addstr(height // 2 + 1, 0, f"You entered: {user_input.decode('utf-8')}")
    
    # Refresh the screen
    stdscr.refresh()
    
    # Wait for user input to exit
    stdscr.getch()

# Run the curses application
curses.wrapper(main)
