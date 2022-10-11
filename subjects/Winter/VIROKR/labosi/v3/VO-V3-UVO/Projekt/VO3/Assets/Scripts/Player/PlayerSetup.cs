using UnityEngine;
using Photon.Pun;
using System.Linq;
using Photon.Realtime;
using static PlayerUIManager;

public class PlayerSetup : MonoBehaviourPunCallbacks, IPlayerUIObserver
{
    // Parameters
    [SerializeField] GameObject playerUI;

    [Header("Models")]
    [SerializeField] GameObject[] soldierModelParts;
    [SerializeField] GameObject[] soldierHands;

    [Header("Camera")]
    [SerializeField] GameObject fpsCamera;

    // Cached
    private bool isMe;
    private Animator animator;
    private Movement movement;
    private Combat combat;
    private PlayerUIManager playerUIManager;

    private void Awake()
    {
        isMe = photonView.IsMine;
        animator = GetComponent<Animator>();
        movement = GetComponent<Movement>();
        combat = GetComponent<Combat>();
        playerUIManager = GetComponentInChildren<PlayerUIManager>();
    }

    public override void OnEnable()
    {
        base.OnEnable();
        if (isMe)
        {
            playerUIManager.Attach(this);
        }
    }

    public override void OnDisconnected(DisconnectCause cause)
    {
        if (isMe)
        {
            Debug.LogError("Disconnectalo me");
            playerUIManager.Detach(this);
        }
    }

    private void Start()
    {
        // Initialization
        soldierModelParts.ToList().ForEach(part => part.SetActive(!isMe));
        animator.SetBool("IsMe", isMe);
        playerUI.SetActive(isMe);
        fpsCamera.SetActive(isMe);

        ActivatePlayerControls(isMe);
    }

    public void OnUIChange(UIState newState)
    {
        if (!isMe)
        {
            return;
        }

        switch (newState)
        {
            case UIState.Alive:
                animator.SetBool("IsDead", false);
                ActivatePlayerControls(true);
                break;

            case UIState.Respawning:
                animator.SetBool("IsDead", true);
                ActivatePlayerControls(false);
                break;
            case UIState.OnResume:
                bool isDead = animator.GetBool("IsDead");
                ActivatePlayerControls(!isDead);
                break;
            case UIState.InPauseScreen:
                ActivatePlayerControls(false);
                break;
            case UIState.InOptionsScreen:
                ActivatePlayerControls(false);
                break;
        }
    }

    private void ActivatePlayerControls(bool _activate)
    {
        movement.enabled = _activate;
        combat.enabled = _activate;
        soldierHands.ToList().ForEach(part => part.SetActive(_activate));
    }

}