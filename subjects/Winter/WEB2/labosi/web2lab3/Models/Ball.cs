using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlazorCanvasTest2.Models
{
    public class Ball
    {
        public double X { get; private set; }
        public double Y { get; private set; }
        public double XVel { get; private set; }
        public double YVel { get; private set; }
        public string Color { get; private set; }

        public Ball(double x, double y, double xVel, double yVel, string color)
        {
            (X, Y, XVel, YVel, Color) = (x, y, xVel, yVel, color);
        }

        public void StepForward(double width, double height)
        {
            X += XVel;
            Y += YVel;
            if (X < 0 || X > width)
            {
                if(XVel < 3 && XVel > -3)
                XVel *= -1.1;
                else
                {
                    XVel /= 1.1;
                }
                //Console.WriteLine(XVel);
            }
            if (Y < 0 || Y > height)
            {
                if(YVel < 3 && YVel > -3)
                YVel *= -1.1;
                else
                {
                    YVel /= 1.1;
                }
                //Console.WriteLine(YVel);
            }

            if (X < 0)
                X += 0 - X;
            else if (X > width)
                X -= X - width;

            if (Y < 0)
                Y += 0 - Y;
            if (Y > height)
                Y -= Y - height;
        }
    }
}
