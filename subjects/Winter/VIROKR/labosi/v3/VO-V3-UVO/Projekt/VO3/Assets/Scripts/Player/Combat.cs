using System.Collections;
using UnityEngine;
using Photon.Pun;
using ExitGames.Client.Photon;
using Photon.Realtime;

public class Combat : MonoBehaviourPunCallbacks
{
    [Header("Weapon Settings")]
    [SerializeField] float damage = 40f;
    [SerializeField] float fireRate = 0.1f;
    [SerializeField] int range = 100;
    [Header("Weapon Effects")]
    [SerializeField] ParticleSystem muzzleFlash;
    [SerializeField] AudioClip shootingSFX;
    [Header("Other stuff")]
    [SerializeField] CombatStats combatStats;
    [SerializeField] GameObject fpsCameraHolder;

    private const float cameraCenter = 0.5f;
    private bool canShoot = true;
    private Camera fpsCamera;
    private PlayerSynchronization playerSynchronization;

    private void Awake()
    {
        fpsCamera = fpsCameraHolder.GetComponent<Camera>();
        playerSynchronization = GetComponent<PlayerSynchronization>();
    }

    public override void OnEnable()
    {
        base.OnEnable();
        PhotonNetwork.NetworkingClient.EventReceived += OnPlayerDeath;
    }

    public override void OnDisable()
    {
        base.OnDisable();
        PhotonNetwork.NetworkingClient.EventReceived -= OnPlayerDeath;
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0) && canShoot && (combatStats.GetCurrentAmmoAmount() > 0))
        {
            StartCoroutine(Shoot());
        }
    }

    private IEnumerator Shoot()
    {
        canShoot = false;
        FireBullet();
        yield return new WaitForSeconds(fireRate);
        canShoot = true;
    }

    private void FireBullet()
    {
        muzzleFlash.Play();

        combatStats.DecreaseAmmo(1);
        playerSynchronization.BulletsFired(1);

        Ray _ray = fpsCamera.ViewportPointToRay(new Vector3(cameraCenter, cameraCenter));
        if (Physics.Raycast(_ray, out RaycastHit _hit, range))
        {
            var _collider = _hit.collider;
            var _photonView = _collider.GetComponent<PhotonView>();
            if (_collider.gameObject.CompareTag("Player") && !_photonView.IsMine)
            {
                _photonView.RPC("TakeDamage", RpcTarget.Others, damage);
                PhotonNetwork.SendAllOutgoingCommands();
            }
        }
    }

    public void ResetHealth()
    {
        combatStats.ResetHealth();
    }

    public void IncreaseAmmo(int _ammoAmount)
    {
        combatStats.IncreaseAmmo(_ammoAmount);
    }

    [PunRPC]
    public void TakeDamage(float _damage, PhotonMessageInfo _info)
    {
        if (_info.photonView.IsMine)
        {
            bool isDead = combatStats.DecreaseHealth(_damage);
            if (isDead)
            {
                Die(_info.Sender.ActorNumber);
            }
        }
    }

    private void Die(int _killerId)
    {
        byte _eventCode = (byte)PhotonRaiseEventCodes.PLAYER_DEAD;
        object[] _content = new object[] { PhotonNetwork.LocalPlayer.ActorNumber, _killerId };
        SendOptions _sendOptions = new SendOptions { Reliability = true };
        RaiseEventOptions _raiseEventOptions = new RaiseEventOptions { Receivers = ReceiverGroup.Others };

        PhotonNetwork.RaiseEvent((byte)_eventCode, _content, _raiseEventOptions, _sendOptions);
        PhotonNetwork.SendAllOutgoingCommands();
    }

    public void OnPlayerDeath(EventData photonEvent)
    {
        if (photonEvent.Code != PhotonRaiseEventCodes.PLAYER_DEAD)
        {
            return;
        }

        object[] _data = (object[])photonEvent.CustomData;
        int _killerActorNum = (int)_data[1];

        if (_killerActorNum == PhotonNetwork.LocalPlayer.ActorNumber && photonView.IsMine)
        {
            BroadcastMessage("TargetKilled");
        }
    }

}
