import click

# INPUTS
# ----------------------------------------------------------------------------------------------------------------------
# Window size

full_screen_answer = click.prompt("Do you want to use full screen (y/n): ")
if full_screen_answer == "y":
    full_screen_input = True
elif full_screen_answer == "n":
    full_screen_input = False

    while True:
        try:
            window_size_input = click.prompt("Enter window size (WIDTH, HEIGHT): ")
            WIDTH_input, HEIGHT_input = window_size_input.split(',')
            WIDTH_input, HEIGHT_input = int(WIDTH_input), int(HEIGHT_input)
            if WIDTH_input < 0 or HEIGHT_input < 0:
                raise ValueError
            break
        except ValueError:
            print("ERROR! Please enter a valid size:")

# ----------------------------------------------------------------------------------------------------------------------
# Default parameters

default_param_answer = input("Do you want to use default parameters (y/n): ")
if default_param_answer == "y":
    velocity_input = 0.9
    max_distance_input = 160
elif default_param_answer == "n":

    # ----------------------------------------------------------------------------------------------------------------------
    # Velocity of moving particles

    while True:
        try:
            velocity_input = click.prompt("Enter velocity of moving particles, recommended velocity "
                                          "interval – (0.5-1.2). Press ENTER for default: ",
                                          type=float, default=0.9)
            velocity_input = float(velocity_input)
            if velocity_input < 0:
                raise ValueError
            break
        except ValueError:
            print("ERROR! Please enter a positive float: ")

    # ----------------------------------------------------------------------------------------------------------------------
    # Max distance when connection between particles disappear

    while True:
        try:
            max_distance_input = click.prompt(
                "Enter max distance when connection between particles disappear, recommended max distance interval – (100-200). "
                "Press ENTER for default: ",
                type=int, default=160)
            max_distance_input = int(max_distance_input)
            if max_distance_input < 0:
                raise ValueError
            break
        except ValueError:
            print("ERROR! Please enter a positive integer: ")
else:
    print("ERROR! Please enter y or n: ")

# ----------------------------------------------------------------------------------------------------------------------
# TERMINAL MESSAGES

print("-" * 60)
print("Plexus Effect Parameters: \n"
      f">>> Velocity - {velocity_input} \n"
      f">>> Max distance - {max_distance_input} \n"
      "\nPress Esc to close the window\n"
      "Press Space to pause the window")
print("-" * 60)
