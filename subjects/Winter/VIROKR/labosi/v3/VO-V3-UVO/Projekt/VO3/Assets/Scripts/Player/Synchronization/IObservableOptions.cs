public interface IObservableOptions
{
    void Attach(IObservableOptionsObserver observer);
    void Detach(IObservableOptionsObserver observer);
    void Notify();
}
