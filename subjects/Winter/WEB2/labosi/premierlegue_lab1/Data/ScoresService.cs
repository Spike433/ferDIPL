namespace QuizManager.Data
{
    public class ScoresService
    {
        public List<Scores> GetScores()
        {            
            var clubScores = new List<Scores>();

            foreach (var schedule in DataSaveer.schedules)
            {
                var leftOpp = schedule.Opponents.Split("-")[0].Trim();
                var rightOpp = schedule.Opponents.Split("-")[1].Trim();

                Scores? foundScoreLeft = clubScores.FirstOrDefault(x => x.Name == leftOpp);
                if (foundScoreLeft is not null)
                {
                    var s = new Scores
                    {
                        Name = foundScoreLeft.Name,
                        Won = foundScoreLeft.Won + (schedule.LeftScore > schedule.RightScore ? 1 : 0),
                        Drawn = foundScoreLeft.Drawn + (schedule.LeftScore == schedule.RightScore ? 1 : 0),
                        Lost = foundScoreLeft.Lost + (schedule.LeftScore < schedule.RightScore ? 1 : 0),
                        GoalsSum = foundScoreLeft.GoalsSum + schedule.LeftScore,
                        GottenGoals = foundScoreLeft.GottenGoals + schedule.RightScore,
                    };
                    s.CalcDiffAndDiff();

                    clubScores.Remove(foundScoreLeft);
                    clubScores.Add(s);
                }
                else
                {
                    var s = new Scores
                    {
                        Name = leftOpp,
                        Won = schedule.LeftScore > schedule.RightScore ? 1 : 0,
                        Drawn = schedule.LeftScore == schedule.RightScore ? 1 : 0,
                        Lost = schedule.LeftScore < schedule.RightScore ? 1 : 0,
                        GoalsSum = schedule.LeftScore,
                        GottenGoals = schedule.RightScore
                    };
                    s.CalcDiffAndDiff();

                    clubScores.Add(s);                    
                }

                Scores? foundScoreRight = clubScores.FirstOrDefault(x => x.Name == rightOpp);
                if (foundScoreRight is not null)
                {
                    clubScores.Remove(foundScoreRight);

                    var s = new Scores
                    {
                        Name = foundScoreRight.Name,
                        Won = foundScoreRight.Won + (schedule.LeftScore < schedule.RightScore ? 1 : 0),
                        Drawn = foundScoreRight.Drawn + (schedule.LeftScore == schedule.RightScore ? 1 : 0),
                        Lost = foundScoreRight.Lost + (schedule.LeftScore < schedule.RightScore ? 0 : 1),
                        GoalsSum = foundScoreRight.GoalsSum + schedule.RightScore,
                        GottenGoals = foundScoreRight.GottenGoals + schedule.LeftScore
                    };

                    s.CalcDiffAndDiff();
                    
                    clubScores.Add(s);
                }
                else
                {
                    var s = new Scores
                    {
                        Name = rightOpp,
                        Won = schedule.LeftScore > schedule.RightScore ? 0 : 1,
                        Drawn = schedule.LeftScore == schedule.RightScore ? 1 : 0,
                        Lost = schedule.LeftScore < schedule.RightScore ? 0 : 1,
                        GoalsSum = schedule.RightScore,
                        GottenGoals = schedule.LeftScore
                    };

                    s.CalcDiffAndDiff();

                    clubScores.Add(s);
                }
            }

            return clubScores;
        }
    }
}
