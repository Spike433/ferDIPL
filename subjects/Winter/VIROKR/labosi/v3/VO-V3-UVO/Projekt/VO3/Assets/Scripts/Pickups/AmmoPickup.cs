using ExitGames.Client.Photon;
using Photon.Pun;
using Photon.Realtime;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class AmmoPickup : MonoBehaviourPunCallbacks
{

    private const double TIME_WRAP_DIFFERENCE = 4294960.0;
    private struct PickupInfo
    {
        public double pickupTime;
        public bool isPicked;
        public LinkedList<bool> acks;
    }

    [SerializeField] int ammoAmount = 20;
    [SerializeField] MeshRenderer[] meshRenderers;

    private PickupInfo pickupInfo;
    private Collider mCollider;
    private int myActorNum;

    private void Start()
    {
        myActorNum = PhotonNetwork.LocalPlayer.ActorNumber;
        mCollider = GetComponent<Collider>();
    }

    public override void OnEnable()
    {
        base.OnEnable();
        pickupInfo = new PickupInfo
        {
            pickupTime = 0.0,
            isPicked = false,
            acks = new LinkedList<bool>()
        };

        PhotonNetwork.NetworkingClient.EventReceived += OnAmmoPicked;
    }

    public override void OnDisable()
    {
        base.OnDisable();
        PhotonNetwork.NetworkingClient.EventReceived -= OnAmmoPicked;
    }

    private void OnTriggerEnter(Collider _other)
    {
        if (_other.gameObject.tag == "Player")
        {
            mCollider.enabled = false;

            pickupInfo.isPicked = true;
            pickupInfo.pickupTime = PhotonNetwork.Time;

            PlayerManager.LocalPlayerPrefab
                         .GetComponentInChildren<AmmoPickupUI>()
                         .UpdateAmmoPickupText(gameObject.name, pickupInfo.pickupTime);

            byte _eventCode = (byte)PhotonRaiseEventCodes.AMMO_PICKUP_REQ;
            object[] _content = new object[] { gameObject.name, myActorNum, pickupInfo.pickupTime };
            SendOptions _sendOptions = new SendOptions { Reliability = true };
            RaiseEventOptions _raiseEventOptions = new RaiseEventOptions { Receivers = ReceiverGroup.Others };

            PhotonNetwork.RaiseEvent(_eventCode, _content, _raiseEventOptions, _sendOptions);
            PhotonNetwork.SendAllOutgoingCommands();

            StartCoroutine(CollectACKs(PhotonNetwork.CurrentRoom.PlayerCount - 1));
        }

    }

    private IEnumerator CollectACKs(int _numOfPLayers)
    {
        yield return new WaitUntil(() => _numOfPLayers == pickupInfo.acks.Count);
        if (!pickupInfo.acks.ToList().Contains(false))
        {
            PlayerManager.LocalPlayerPrefab.GetComponent<Combat>().IncreaseAmmo(ammoAmount);
        }

        DestroyAmmoPickup();
    }

    public void OnAmmoPicked(EventData photonEvent)
    {
        if (!IsValidAmmoEvent(photonEvent))
        {
            return;
        }

        object[] _data = (object[])photonEvent.CustomData;
        string _objectName = (string)_data[0];
        int _requestor = (int)_data[1];

        if (photonEvent.Code == PhotonRaiseEventCodes.AMMO_PICKUP_REQ)
        {
            double _enemyPickupTime = (double)_data[2];
            HandleREQ(_objectName, _requestor, _enemyPickupTime);
        }
        else
        {
            bool _ack = (bool)_data[2];
            HandleACK(_requestor, _ack);
        }
    }

    private void HandleREQ(string _objectName, int _requestor, double _enemyPickupTime)
    {
        if (!pickupInfo.isPicked)
        {
            SendACK(_objectName, _requestor, true);
            DestroyAmmoPickup();
            return;
        }

        if (_enemyPickupTime == pickupInfo.pickupTime)
        {
            // Player with smaller actor number has advantage
            SendACK(_objectName, _requestor, (PhotonNetwork.LocalPlayer.ActorNumber > _requestor));
        }

        /// It will "wrap around" from 4294967.295 to 0!
        bool _isTimeWrapped = Mathf.Abs((float)_enemyPickupTime - (float)pickupInfo.pickupTime) >= TIME_WRAP_DIFFERENCE;

        if (_isTimeWrapped)
        {
            bool _isMyTimeWrapped = pickupInfo.pickupTime < TIME_WRAP_DIFFERENCE;
            SendACK(_objectName, _requestor, _isMyTimeWrapped);
        }
        else
        {
            bool _ack = _enemyPickupTime < pickupInfo.pickupTime;
            SendACK(_objectName, _requestor, _ack);
        }
    }

    private void HandleACK(int _requestorActorNum, bool _ack)
    {
        if (!pickupInfo.isPicked)
        {
            return;
        }

        if (PhotonNetwork.LocalPlayer.ActorNumber != _requestorActorNum)
        {
            return; // This ACK is not for me
        }
        pickupInfo.acks.AddLast(_ack);
    }

    private bool IsValidAmmoEvent(EventData photonEvent)
    {
        if (photonEvent.Code != PhotonRaiseEventCodes.AMMO_PICKUP_REQ &&
            photonEvent.Code != PhotonRaiseEventCodes.AMMO_PICKUP_ACK)
        {
            return false;
        }

        object[] _data = (object[])photonEvent.CustomData;
        string _objectName = (string)_data[0];
        if (_objectName != gameObject.name)
        {
            return false;   // I don't own that object
        }

        return true;
    }

    private void SendACK(string _objectName, int _requestorActorNum, bool _canPickIt)
    {
        byte _eventCode = (byte)PhotonRaiseEventCodes.AMMO_PICKUP_ACK;
        object[] _content = new object[] { _objectName, _requestorActorNum, _canPickIt };
        SendOptions _sendOptions = new SendOptions { Reliability = true };
        RaiseEventOptions _raiseEventOptions = new RaiseEventOptions { Receivers = ReceiverGroup.Others };

        PhotonNetwork.RaiseEvent(_eventCode, _content, _raiseEventOptions, _sendOptions);
        PhotonNetwork.SendAllOutgoingCommands();
    }

    private void DestroyAmmoPickup()
    {
        mCollider.enabled = false;
        foreach (MeshRenderer mr in meshRenderers)
        {
            mr.enabled = false;
        }
        Destroy(gameObject, 5f);
    }
}