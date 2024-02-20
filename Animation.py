import turtle
import time
import pygame
from PIL import Image

# Initialize pygame for background music
pygame.mixer.init()

# Load background music (replace 'background_music.mp3' with your file)
pygame.mixer.music.load('test.mp3')

# Play the background music
pygame.mixer.music.play(-1)  # -1 means play indefinitely

# Initialize the turtle screen
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Interactive Fairy Tale")

# Set the background image (replace 'background_image.png' with your file)
screen.bgpic('test.png')

# Create a turtle for drawing
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# Function to draw a rectangle for buttons
def draw_button(x, y, text):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.fillcolor("lightblue")
    pen.begin_fill()
    for _ in range(4):
        pen.forward(100)
        pen.left(90)
    pen.end_fill()
    pen.penup()
    pen.goto(x + 20, y + 40)
    pen.write(text, align="center", font=("Arial", 12, "normal"))

# Function to handle button clicks
def on_click(x, y):
    if 150 <= x <= 250 and -50 <= y <= 50:
        pen.clear()
        pen.write("You clicked the button!", align="center", font=("Arial", 16, "normal"))

# Register the button click event
screen.onclick(on_click)

# Main part of the story
pen.write("Once upon a time...", align="center", font=("Arial", 16, "normal"))

# Draw a button for the next part of the story
draw_button(150, -50, "Next")

# Display the screen
turtle.done()