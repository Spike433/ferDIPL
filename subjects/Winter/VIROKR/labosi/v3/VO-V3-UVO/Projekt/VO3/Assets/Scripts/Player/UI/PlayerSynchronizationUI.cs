using UnityEngine.UI;
using UnityEngine;

public class PlayerSynchronizationUI : MonoBehaviour, IObservableOptionsAdapter
{
    [SerializeField] Toggle syncPositionToggle;
    [SerializeField] Toggle syncRotationToggle;
    [SerializeField] Toggle interpolationToggle;
    [SerializeField] Toggle extrapolationToggle;

    IObservableOptionsAdapter adaptee;

    private void Awake()
    {
        adaptee = PlayerManager.instance;
    }

    private void Start()
    {
        syncPositionToggle.isOn = false;
        syncRotationToggle.isOn = false;
        interpolationToggle.isOn = false;
        extrapolationToggle.isOn = false;
    }

    public void OnSyncPositionChange(bool _value)
    {
        adaptee.OnSyncPositionChange(_value);
    }

    public void OnSyncRotationChange(bool _value)
    {
        adaptee.OnSyncRotationChange(_value);
    }

    public void OnInterpolationChange(bool _value)
    {
        adaptee.OnInterpolationChange(_value);
    }

    public void OnExtrapolationChange(bool _value)
    {
        adaptee.OnExtrapolationChange(_value);
    }
}
