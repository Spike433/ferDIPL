public interface IObservableOptionsAdapter
{
    void OnSyncPositionChange(bool _value);
    void OnSyncRotationChange(bool _value);
    void OnInterpolationChange(bool _value);
    void OnExtrapolationChange(bool _value);
}
