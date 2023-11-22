# animation2.py

# multiple-shot cannonball animation

from math import sqrt, sin, cos, radians, degrees
from graphics import *
from projectile import Projectile
from button import Button

class Launcher:
    def __init__(self, win):
        # draw the base shot of the launcher
        self.player_a = Circle(Point(0, 0), 3)
        self.player_a.setFill("red")
        self.player_a.setOutline("red")
        self.player_a.draw(win)

        # draw the second player's base shot
        self.player_b = self.player_a.clone()
        self.player_b.move(200, 0)
        self.player_b.draw(win)

        # draw the target
        self.target = Circle(Point(100, 20), 5)
        self.target.setFill("green")
        self.target.draw(win)

        # save the window and create initial angle and velocity as global variables
        self.win = win
        self.angle = radians(45.0)
        self.vel = 40.0
        self.shot_limit = 5
        self.shot_count = 0
        self.hit_count = 0

        # create initial "dummy" arrow1 and arrow2
        self.arrow = Line(Point(0, 0), Point(0, 0)).draw(win)

        # replace both arrows with the correct arrows
        self.redraw()

    def redraw(self):
        # undraw the arrow and draw a new one for the current values of angle and velocity
        self.arrow.undraw()

        pt2 = Point(self.vel * cos(self.angle), self.vel * sin(self.angle))

        # Arrow1
        self.arrow = Line(Point(0, 0), pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(3)

    def adjAngle(self, amt):
        # change angle by amt degrees
        self.angle = self.angle + radians(amt)
        self.redraw()

    def adjVel(self, amt):
        # change velocity by amt
        self.vel = self.vel + amt
        self.redraw()

    def fire(self):
        if self.shot_count < self.shot_limit:
            self.shot_count += 1
            return ShotTracker(self.win, degrees(self.angle), self.vel, 0.0, self.target, self)

        else:
            return None


class ShotTracker:
    def __init__(self, win, angle, velocity, height, target, launcher):
        # win is the GraphWin to display the shot, angle, velocity, and height are initial projectile parameters.
        self.proj = Projectile(angle, velocity, height)
        self.target = target
        self.launcher = launcher

        # marker1
        self.marker = Circle(Point(0, height), 3)
        self.marker.setFill("red")
        self.marker.setOutline("red")
        self.marker.draw(win)

    def update(self, dt):
        # Move the shot dt seconds farther along its flight
        self.proj.update(dt)

        # For marker 1
        center = self.marker.getCenter()
        dx = self.proj.getX() - center.getX()
        dy = self.proj.getY() - center.getY()
        self.marker.move(dx, dy)

        # Check for a hit
        if self.proj.getX() >= self.target.getCenter().getX() - 5 and \
           self.proj.getX() <= self.target.getCenter().getX() + 5 and \
           self.proj.getY() >= self.target.getCenter().getY() - 5 and \
           self.proj.getY() <= self.target.getCenter().getY() + 5:
            self.target.setFill("red")
            self.launcher.hit_count += 1

    def getX(self):
        # return the current x coordinate of the shot's center
        return self.proj.getX()

    def getY(self):
        # return the current y coordinate of the shot's center
        return self.proj.getY()

    def undraw(self):
        # undraw the shot
        self.marker.undraw()


class ProjectileApp:
    def __init__(self):
        self.win = GraphWin("Projectile Animation", 640, 480)
        self.win.setCoords(-10, -10, 210, 155)
        Line(Point(-10, 0), Point(210, 0)).draw(self.win)

        for x in range(0, 210, 25):
            Text(Point(x, -7), str(x)).draw(self.win)
            Line(Point(x, 0), Point(x, 2)).draw(self.win)

        self.launcher = Launcher(self.win)
        self.shots = []

    def updateShots(self, dt):
        alive = []
        for shot in self.shots:
            shot.update(dt)
            if shot.getY() >= 0 and shot.getX() < 210:
                alive.append(shot)
            else:
                shot.undraw()
        self.shots = alive

    def run(self):

        # main event/animation loop
        while True:
            self.updateShots(1 / 30)

            key = self.win.checkKey()
            if key in ["q", "Q"]:
                break

            if key == "Up":
                self.launcher.adjAngle(5)
            elif key == "Down":
                self.launcher.adjAngle(-5)
            elif key == "Right":
                self.launcher.adjVel(5)
            elif key == "Left":
                self.launcher.adjVel(-5)
            elif key == "f":
                shot = self.launcher.fire()
                if shot:
                    self.shots.append(shot)

            update(30)

        # Print the report
        print("\nReport:")
        print("Total Shots:", self.launcher.shot_count)
        print("Total Misses:", self.launcher.shot_count - self.launcher.hit_count)
        print("Total Hits:", self.launcher.hit_count)

        # Calculate and print grade score
        hit_percentage = (self.launcher.hit_count / self.launcher.shot_count) * 100
        print("Hit Percentage:", round(hit_percentage, 2), "%")

        if hit_percentage >= 70:
            print("Grade: A")
        elif 50 <= hit_percentage < 70:
            print("Grade: B")
        elif 30 <= hit_percentage < 50:
            print("Grade: C")
        else:
            print("Grade: F")

        self.win.close()


if __name__ == "__main__":
    ProjectileApp().run()
