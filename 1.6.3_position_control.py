"""
This demonstrates the code for Practical 1, specifically via:
```
posBot.move_square(forward_dist=833, turn_amount=250)
```
This makes the robot move in a square using position control, callibrated by
  our empirically derived values
"""

from bot_control.PositionControl import PositionControlBot
from common import ControlProcedure, PiBot, curse_print, main_wrapper


def control_loop(posBot: PositionControlBot, letter: str):
    if letter == "w":
        curse_print("Moving forward")
        posBot.move_forward()
    elif letter == "a":
        curse_print("Turning left")
        posBot.turn_left()
    elif letter == "s":
        curse_print("Moving backward")
        posBot.move_backward()
    elif letter == "d":
        curse_print("Turning right")
        posBot.turn_right()
    elif letter == "y":
        curse_print("Moving in a square")
        posBot.move_square(forward_dist=833, turn_amount=250)
    elif letter == "u":
        curse_print("Moving in a square stop every 10sec")
        posBot.move_square_10(forward_dist=833, turn_amount=250)
    elif letter == "x":
        curse_print("Stopping")
        posBot.stop()
    else:
        curse_print(f"Unknown command: {letter}")


def main():
    bot = PiBot()
    posControlBot = PositionControlBot(bot, 300)

    def control_loop_fn(inp: str):
        control_loop(posControlBot, inp)

    control_proc = ControlProcedure(control_loop_fn)
    control_proc.start_procedure()


if __name__ == "__main__":
    main_wrapper(main)
