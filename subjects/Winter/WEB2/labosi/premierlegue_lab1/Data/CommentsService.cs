namespace QuizManager.Data
{
    public class CommentsService
    {
        public List<RoundCommentManager> GetData(int rounds)
        {
            var roundComments = new List<RoundCommentManager>();
            for (int i = 1; i < rounds + 1; i++)
            {
                roundComments.Add(new RoundCommentManager
                {
                    RoundId = i,
                    Comments = new List<Comment>()
                    {
                        new Comment() { AuthorId = "mile@volidisko.com", Created = DateTime.Now.AddHours(i).AddDays(i), Description = "Initial text1"},
                        new Comment() { AuthorId = "mile@car.com", Created = DateTime.Now.AddHours(i+1).AddDays(i+1), Description = "Initial text2"},
                        new Comment() { AuthorId = "mile@car.com", Created = DateTime.Now.AddHours(i+2).AddDays(i+2), Description = "Initial text13"}
                    }
                });
            }

            return roundComments;  
        }
    }
}
