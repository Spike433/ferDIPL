using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlazorCanvasTest2.Models
{
    public class Field
    {
        public readonly List<Ball> Balls = new List<Ball>();
        public double Width { get; private set; }
        public double Height { get; private set; }
        public static double min = 0.5;
        public static double max = 1;


        public void Resize(double width, double height) =>
            (Width, Height) = (width, height);

        public void StepForward()
        {
            foreach (Ball ball in Balls)
                ball.StepForward(Width, Height);
        }

        private double RandomVelocity()
        {
            Console.WriteLine("Change vel");
            Random rand = new Random();
            double v = min + (max - min) * rand.NextDouble();
            if (rand.NextDouble() > .5)
                v *= -1;
            return v;
        }

        public void AddRandomBalls(int count)
        {
            Random rand = new Random();

            for (int i = 0; i < count; i++)
            {
                Balls.Add(
                    new Ball(
                        x: (Width-100)* rand.NextDouble(),
                        y: (Height-100)* rand.NextDouble(),
                        xVel: RandomVelocity(),
                        yVel: RandomVelocity(),                       
                        color: string.Format("#{0:X6}", rand.Next(0xFFFFFF))
                    )
                );
            }
        }
    }
}
