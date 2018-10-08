from PIL import Image, ImageDraw # For drawing animation frames
import cv2 # for recording video
import numpy as np # for arrays and random numbers

# Set up file Path
directory = "C:\\Users\\ **** \\Desktop"
file_path = directory + "\\test_video.avi"
print(file_path)

# Set up image file and drawing functions
GRID_SIZE = (30, 30)
WINDOW_SIZE = (500, 500)
BORDER = 0.1
PILE_LIMIT = 8

# Calculate tile geometry
grid_width = WINDOW_SIZE[0]/GRID_SIZE[0]
grid_height = WINDOW_SIZE[1]/GRID_SIZE[1]
buffer_width = BORDER*grid_width
tile_width = grid_width - (2*buffer_width)
tile_height = grid_height - (2*buffer_width)

#print([tile_width, tile_height, buffer_width])

# Function to update tiles
def draw_tile(x, y, color):
    x_pos = (x*grid_width) + buffer_width
    y_pos = (y*grid_height) + buffer_width
    idraw.rectangle([(x_pos, y_pos),(x_pos+tile_width, y_pos+tile_height)], fill = color, outline = (0, 0, 0))

# one-time calculations for color scaling
p0 = 0
p1 = PILE_LIMIT
q0 = 0
q1 = 1
m = (q1-q0)/(p1-p0)
b = q1 - (m*p1)

# function to apply color scale to tiles
def col_scale(val):
    #if val > p1:
        #val = p1
    val = (m*val)+b
    red = int(round(val*255, 0))
    green = int(round((1-val)*255, 0))
    blue = int(200)
    col_out = (red, green, blue)
    return col_out

#print(col_scale(0))
#idraw.line([(0, 0), (50, 50)], fill = (255, 0, 0), width = 2)
#idraw.rectangle([(60, 60),(90, 90)], fill = (0, 0, 255), outline = (0, 0, 0))

# Generate array to represent the state of the system
pile = np.zeros((GRID_SIZE[0]+2, GRID_SIZE[1]+2), dtype = int)

# Initialize video recording
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_out = cv2.VideoWriter(file_path,fourcc, 60.0, WINDOW_SIZE)

# Initialize image
im = Image.new('RGB', WINDOW_SIZE, (255, 255, 255))
idraw = ImageDraw.Draw(im)

# Loop to add to the pile
cutoff = 5000
iter = 1
while iter < cutoff:
    # Progress report
    if iter%100 == 0:
        print(iter)

    # Choose a random tile and increment its value
    grain_x = np.random.randint(1, GRID_SIZE[0]+1)
    grain_y = np.random.randint(1, GRID_SIZE[1]+1)
    pile[grain_x][grain_y] += 1

    # Avalanche event
    if True:
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                if pile[j][i] > PILE_LIMIT:
                    pile[j][i] -= 8
                    pile[j+1][i] += 2
                    pile[j-1][i] += 2
                    pile[j][i+1] += 2
                    pile[j][i-1] += 2

    # Update the image
    for i in range(GRID_SIZE[0]):
        for j in range(GRID_SIZE[1]):
            draw_tile(i, j, col_scale(pile[i+1, j+1]))

    # Add a frame to the video recording
    if iter > 0:
        pil_image = im.convert('RGB')
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        video_out.write(open_cv_image)

    # Increment to keep track of iterations
    iter += 1

#im.show()

# Stop recording video
video_out.release()
cv2.destroyAllWindows()

print("Done!")
