using System.Runtime.CompilerServices;

namespace QuizManager.Data
{
    public class Scores : IComparable<Scores>
    {
        public string? Name { get; set;}
        public int Won { get; set; } = 0;
        public int Drawn { get; set; } = 0;
        public int Lost { get; set; } = 0;
        public int GoalsSum { get; set; } = 0;
        public int GottenGoals { get; set; } = 0;
        public int Score { get; set; }
        public int Diff { get; set; }

        public void CalcDiffAndDiff()
        {
            Score = Won * 3 + Drawn * 1 + Lost * 0;
            Diff = GoalsSum - GottenGoals;
        }

        public int CompareTo(Scores? other)
        {
            if(this.Score == other.Score)
            {
                return this.Diff.CompareTo(other.Diff);
            }
            else
            {
                return this.Score.CompareTo(other.Score);
            }
        }

        public override bool Equals(object? obj)
        {
            var otherName = obj as Scores;
            
            if(otherName == null) 
                return false;

            if (this.Name == otherName.Name)
                return true;

            return false;
        }

    }
}
