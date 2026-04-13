using DataBaseModels;
using Domain.Entities;

namespace API.Infrastructure.Persistence.Context;
using Microsoft.EntityFrameworkCore;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options) { }

    public DbSet<UserSession> UserSessions { get; set; }
    public DbSet<Message> Messages { get; set; }
    public DbSet<QuizRequest> QuizRequests { get; set; }
    public DbSet<QuizItem> QuizItems { get; set; }
    public DbSet<SubmittedAnswer> SubmittedAnswers { get; set; }
    public DbSet<EvaluationResult> EvaluationResults { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // 1. Session to Messages (One-to-Many)
        modelBuilder.Entity<Message>()
            .HasOne(m => m.UserSession)
            .WithMany(s => s.Messages)
            .HasForeignKey(m => m.UserSessionId)
            .OnDelete(DeleteBehavior.Cascade);

        // 2. Session to QuizRequests (One-to-Many)
        modelBuilder.Entity<QuizRequest>()
            .HasOne(q => q.UserSession)
            .WithMany(s => s.QuizRequests)
            .HasForeignKey(q => q.UserSessionId);

        // 3. QuizRequest to QuizItems (One-to-Many)
        modelBuilder.Entity<QuizItem>()
            .HasOne(i => i.QuizRequest)
            .WithMany(r => r.QuizItems)
            .HasForeignKey(i => i.QuizRequestId);

        // 4. QuizItem to SubmittedAnswer (One-to-One)
        modelBuilder.Entity<SubmittedAnswer>()
            .HasOne(a => a.QuizItem)
            .WithOne(i => i.SubmittedAnswer)
            .HasForeignKey<SubmittedAnswer>(a => a.QuizItemId);

        // 5. SubmittedAnswer to EvaluationResult (One-to-One)
        modelBuilder.Entity<EvaluationResult>()
            .HasOne(e => e.SubmittedAnswer)
            .WithOne(a => a.Evaluation)
            .HasForeignKey<EvaluationResult>(e => e.SubmittedAnswerId);

        // Indexing for Performance (NFR-2)
        modelBuilder.Entity<UserSession>()
            .HasIndex(s => s.ExternalUserId);
    }
}