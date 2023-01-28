using System;
using System.ComponentModel.DataAnnotations;

namespace QuizManager.Data
{
    public class Schedule
    {
        public int Id { get; set; }
        public string? Opponents { get; set; }
        
        [Required(ErrorMessage = "Goals should be between 0 and 100")]
        [Range(0, 100, ErrorMessage = "Wrong input")]
        public int LeftScore { get; set; }

        [Required(ErrorMessage = "Goals should be between 0 and 100")]
        [Range(0, 100, ErrorMessage = "Wrong input")]
        public int RightScore { get; set; }

        public DateTime Date { get; set; }        
    }    
}
