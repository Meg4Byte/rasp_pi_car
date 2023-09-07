import tkinter as tk
import paramiko

def send_command(command):
    # Establish SSH connection to Raspberry Pi
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.1.16', username='pi', password='1')

    # Send the command to control the car
    if command == 'w':
        ssh.exec_command('echo "Move Forward"')
        print('Move Forward')
    elif command == 's':
        ssh.exec_command('echo "Move Backward"')
        print('Move Backward')
    elif command == 'a':
        ssh.exec_command('echo "Turn Left"')
        print('Turn Left')
    elif command == 'd':
        ssh.exec_command('echo "Turn Right"')
        print('Turn Right')

    # Close the SSH connection
    ssh.close()

# Create the GUI
root = tk.Tk()

# Create WSAD buttons
button_w = tk.Button(root, text="W", command=lambda: send_command('w'))
button_s = tk.Button(root, text="S", command=lambda: send_command('s'))
button_a = tk.Button(root, text="A", command=lambda: send_command('a'))
button_d = tk.Button(root, text="D", command=lambda: send_command('d'))

# Pack the buttons
button_w.pack()
button_s.pack()
button_a.pack()
button_d.pack()

# Start the GUI main loop
root.mainloop()
