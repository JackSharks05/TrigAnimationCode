#Author: Jack de Haan
#Copy for MIT Portfolio: 4 Jan 2024
from manim import *
config.pixel_width = 1080
config.pixel_height = 1440

#Credit to heejin_park (https://infograph.tistory.com/230) for the inspiration and for helping me learn this library from scratch through this code example!
class TrigExplanation(Scene):
    
    #manim method to call (m)animations
    def construct(self):
        self.set_scene()
        self.rotations()
        self.wait(1)
        self.explainyour()
        self.wait(1)

    #Setting the scene...
    def set_scene(self):
        x_axis = Line(np.array([-6,-1,0]),np.array([6,-1,0]))
        y_axis = Line(np.array([-4,-3,0]),np.array([-4,9,0]))
        self.play(FadeIn(x_axis),FadeIn(y_axis))
        sine_label = MathTex("\sin(\\theta)",color=PURPLE).next_to(np.array([6, -1, 0]),UP)
        cosine_label = MathTex("\cos(\\theta)",color=PURPLE).next_to(np.array([-4, 8, 0]), RIGHT)
        self.play(FadeIn(sine_label),FadeIn(cosine_label))
        self.origin = np.array([-4,-1,0])
        circle = Circle(radius=1, color=PURPLE)
        circle.move_to(self.origin)

        #...raising the curtain!
        self.play(FadeIn(circle))
        self.circle = circle
        self.add_labels()
        self.wait()
        self.sine_curve_start = np.array([-3,-1,0])
        self.cosine_curve_start = np.array([-3,0,0])

    #Adding labels that represent the theta on the unit circle.
    def add_labels(self):
        x_labels = [MathTex("0", color=PURPLE), MathTex("\\frac{\pi}{2}", color=PURPLE), MathTex("\pi", color=PURPLE), MathTex("\\frac{3 \pi}{2}", color=PURPLE), MathTex("2 \pi", color=PURPLE), MathTex("\\frac{5 \pi}{2}", color=PURPLE), MathTex("3 \pi", color=PURPLE), MathTex("\\frac{7 \pi}{2}", color=PURPLE)]
        y_labels = [MathTex("0", color=PURPLE), MathTex("\\frac{\pi}{2}", color=PURPLE), MathTex("\pi", color=PURPLE), MathTex("\\frac{3 \pi}{2}", color=PURPLE), MathTex("2 \pi", color=PURPLE), MathTex("\\frac{5 \pi}{2}", color=PURPLE), MathTex("3 \pi", color=PURPLE), MathTex("\\frac{7 \pi}{2}", color=PURPLE)]
        for i in range(4):
            x_labels[i*2].next_to(np.array([i*2 -3, -1, 0]), DOWN)
            y_labels[i*2].next_to(np.array([-4, i*2, 0]), RIGHT)
            x_labels[i*2 +1].next_to(np.array([i*2 -2, -1, 0]), UP)
            y_labels[i*2 +1].next_to(np.array([-4, i*2 +1, 0]), LEFT)
        for i in range(8):
            self.play(FadeIn((x_labels[i]),(y_labels[i])))
        
    #EXPLAIN YOURSELF!!!! (sorry, i had to)
    def explainyour(self):
        explanation1 = Text("x-axis and y-axis labels correspond", color=PURPLE).next_to(np.array([-5,-4,0]))
        explanation2 = Text("to theta value on unit circle", color=PURPLE).next_to(np.array([-5,-5,0]))
        explanation3 = Text("with corresponding trig graphs.", color=PURPLE).next_to(np.array([-5,-6,0]))
        self.play(Create(explanation1))
        self.play(Create(explanation2))
        self.play(Create(explanation3))

    #Most of the code/logic from link above, though I had to figure out how to make it work vertically for cosine as well.
    def rotations(self):
        orbit = self.circle
        origin = self.origin

        dot = Dot(radius=0.08, color=PURPLE)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))
        def get_line_to_circle():
            return Line(origin, dot.get_center(), color=PURPLE)
        def get_x_line_to_curve():
            x = self.sine_curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x,y,0]), color=BLUE, stroke_width=3)
        def get_y_line_to_curve():
            x = dot.get_center()[0]
            y = self.cosine_curve_start[1] + self.t_offset * 4
            return Line(dot.get_center(), np.array([x,y,0]), color=RED, stroke_width=3)
        self.sine_curve = VGroup()
        self.sine_curve.add(Line(self.sine_curve_start,self.sine_curve_start))
        def get_x_curve():
            last_line = self.sine_curve[-1]
            x = self.sine_curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=BLUE)
            self.sine_curve.add(new_line)
            return self.sine_curve
        self.cosine_curve = VGroup()
        self.cosine_curve.add(Line(self.cosine_curve_start,self.cosine_curve_start))
        def get_y_curve():
            last_line = self.cosine_curve[-1]
            x = dot.get_center()[0]
            y = self.cosine_curve_start[1] + self.t_offset * 4
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=RED)
            self.cosine_curve.add(new_line)
            return self.cosine_curve
        dot.add_updater(go_around_circle)
        #What to update with each dot move:
        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_x_curve_line = always_redraw(get_x_line_to_curve)
        dot_to_y_curve_line = always_redraw(get_y_line_to_curve)
        sine_curve_line = always_redraw(get_x_curve)
        cosine_curve_line = always_redraw(get_y_curve)
        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_x_curve_line, dot_to_y_curve_line, sine_curve_line, cosine_curve_line)
        self.wait(8.02) #The approximate number of revolutions (because apparently just 8 wasn't gr8 enough!) [Future Jack edit if MIT sees this: I'll very likely end up taking 8.02 (Physics E&M) if first semester freshmen physics doesn't kill me first!! This number is quite a coincidence... :)]
        dot.remove_updater(go_around_circle)
