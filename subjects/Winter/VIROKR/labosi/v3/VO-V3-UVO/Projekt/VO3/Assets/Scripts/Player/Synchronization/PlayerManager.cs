using UnityEngine;
using Photon.Pun;
using System.Collections.Generic;
using System.Collections;

public class PlayerManager : MonoBehaviour, IObservableOptions, IObservableOptionsAdapter
{
    public struct ObservableOptions
    {
        public bool position;
        public bool rotation;
        public bool interpolation;
        public bool extrapolation;
    }

    [SerializeField] GameObject playerPrefab;
    [SerializeField] float loadingTime = 1f;
    [SerializeField] Canvas loadingScreen;

    private const int PLAYER_START_POST = 100;
    private const int POSITION_OFFSET = 10;
    public static PlayerManager instance;
    public static GameObject LocalPlayerPrefab { get; set; }

    private ObservableOptions observableOptions;
    private LinkedList<IObservableOptionsObserver> observers;

    // Singleton
    private void Awake()
    {
        if (instance != null)
        {
            Destroy(gameObject);
        }
        else
        {
            instance = this;
        }
    }

    void Start()
    {
        if (PhotonNetwork.IsConnectedAndReady && playerPrefab != null && LocalPlayerPrefab == null)
        {
            StartCoroutine(InstantiatePlayer());
        }
    }

    private IEnumerator InstantiatePlayer()
    {
        observers = new LinkedList<IObservableOptionsObserver>();

        observableOptions = new ObservableOptions
        {
            position = false,
            rotation = false,
            interpolation = false,
            extrapolation = false
        };

        // To avoid synchronization issues due to scene loading
        yield return new WaitForSeconds(loadingTime);
        int _offset = POSITION_OFFSET * PhotonNetwork.LocalPlayer.ActorNumber;
        int _pos = PLAYER_START_POST + _offset;

        LocalPlayerPrefab = PhotonNetwork.Instantiate(playerPrefab.name, new Vector3(_pos, 0f, _pos), Quaternion.identity);

        // Wait other player instantion messages
        yield return new WaitForSeconds(loadingTime);
        loadingScreen.enabled = false;
    }

    public ObservableOptions GetObservableOptions()
    {
        return observableOptions;
    }

    public void OnSyncPositionChange(bool _value)
    {
        observableOptions.position = _value;
        Notify();
    }

    public void OnSyncRotationChange(bool _value)
    {
        observableOptions.rotation = _value;
        Notify();
    }

    public void OnInterpolationChange(bool _value)
    {
        observableOptions.interpolation = _value;
        Notify();
    }

    public void OnExtrapolationChange(bool _value)
    {
        observableOptions.extrapolation = _value;
        Notify();
    }

    public void Attach(IObservableOptionsObserver observer)
    {
        observers.AddLast(observer);
    }

    public void Detach(IObservableOptionsObserver observer)
    {
        observers.Remove(observer);
    }

    public void Notify()
    {
        foreach (var o in observers)
        {
            o.OnObservableOptionsChange(observableOptions);
        }
    }
}