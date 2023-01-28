namespace QuizManager.Data
{
    public class RoundCommentManager : IComparable<RoundCommentManager>
    {
        public int RoundId { get; set; }
        public List<Comment> Comments { get; set; }        

        public int CompareTo(RoundCommentManager? other)
        {
            return RoundId.CompareTo(other.RoundId);
        }

        public override bool Equals(object? obj)
        {
            var other = obj as RoundCommentManager;
            if(other == null)
                return false;

            if(this.RoundId != other.RoundId)
                return false;

            return true;
        }
    }    
}
