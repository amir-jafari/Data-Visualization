import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Initialize line data
line_data = []

# Function to draw the line on the canvas
def draw_line(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if not line_data:
            line_data.append([x, y])
        else:
            line_data.append([x, y])
            canvas[:] = 255  # Clear the canvas
            for i in range(len(line_data) - 1):
                x1, y1 = line_data[i]
                x2, y2 = line_data[i + 1]
                cv2.line(canvas, (x1, y1), (x2, y2), (0, 0, 0), 2)

            # Plot the line on the Matplotlib canvas
            ax.clear()
            ax.set_xlim(0, canvas.shape[1])
            ax.set_ylim(canvas.shape[0], 0)
            ax.plot([p[0] for p in line_data], [canvas.shape[0] - p[1] for p in line_data], 'r-', lw=2)
            st.pyplot(fig)

# Streamlit app
st.set_option('deprecation.showPyplotGlobalUse', False)

# Create a blank canvas
canvas = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Create a figure and axis for Matplotlib
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_title("Click on the canvas to draw a line")

# Set up the OpenCV canvas event handler
cv2.namedWindow("Canvas")
cv2.setMouseCallback("Canvas", draw_line)

# Display the canvas and handle events
while True:
    cv2.imshow("Canvas", canvas)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
