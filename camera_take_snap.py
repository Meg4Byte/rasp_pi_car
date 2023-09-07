import cv2
import numpy as np
import datetime

# Initialize the OpenCV window
cv2.namedWindow("Screenshot Capture")

# Create a counter for screenshots
screenshot_counter = 0

while True:
    # Capture key presses
    key = cv2.waitKey(1) & 0xFF

    # Capture a screenshot when "O" key is pressed
    if key == ord("o"):
        # Capture the screen
        screen = np.array(ImageGrab.grab())

        # Generate a timestamp for the filename
        timestamp = datetime.datetime.now().strftime("%d.%m.%Y_%H:%M:%S")

        # Create a filename based on the timestamp
        filename = f"{timestamp}.png"

        # Save the screenshot
        cv2.imwrite(filename, screen)
        print(f"Screenshot saved as {filename}")

        # Increment the screenshot counter
        screenshot_counter += 1

    # Exit the loop when the "q" key is pressed
    elif key == ord("q"):
        break

# Close the OpenCV window
cv2.destroyAllWindows()
