using System;
using System.Data.Common;
using System.Linq;
using System.Threading.Tasks;

namespace QuizManager.Data
{
    public class ScheduleService
    {
        public static Schedule[] GetData()
        {
            List<string> matches = new List<string>()
            {
                "Arsenal -Totenham",
                "Chelsea - NewCastle",

                "Arsenal - Chelsea",
                "Totenham - NewCastle",                               

                "Arsenal - NewCastle",
                "Totenham - Chelsea"
            };

            var scores = new List<int>()
            {
                1,0,
                0,2,

                1,0,
                0,1,

                2,2,
                0,0                
            };

            var scoreCounter = -1;
            return Enumerable.Range(0, 6).Select(index => new Schedule
            {
                Id = index+1,
                Date = DateTime.Now.AddDays(index),
                Opponents = matches[index],
                LeftScore = scores[++scoreCounter],
                RightScore = scores[++scoreCounter]
            }).ToArray();
        }
    }
}
