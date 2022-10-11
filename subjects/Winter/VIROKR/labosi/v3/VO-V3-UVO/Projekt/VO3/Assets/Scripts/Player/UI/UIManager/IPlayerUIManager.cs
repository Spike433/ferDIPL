public interface IPlayerUIManager
{
    void Attach(IPlayerUIObserver observer);
    void Detach(IPlayerUIObserver observer);
    void Notify();
}
