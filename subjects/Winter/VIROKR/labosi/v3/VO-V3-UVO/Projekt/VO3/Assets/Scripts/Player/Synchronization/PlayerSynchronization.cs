using ExitGames.Client.Photon;
using Photon.Pun;
using System;
using System.Collections;
using UnityEngine;

public class PlayerSynchronization : MonoBehaviourPunCallbacks, IPunObservable, IObservableOptionsObserver
{
    [SerializeField] int respawnTime = 8;
    [SerializeField] ParticleSystem muzzleFlash;

    private const float DEGREES_IN_CIRCLE = 360;
    private const float NUM_OF_WALK_ANIMATIONS = 8;
    private const float DEGREES_PER_ANIMATION = DEGREES_IN_CIRCLE / NUM_OF_WALK_ANIMATIONS;

    private const float WALK_FORWARD_START = DEGREES_IN_CIRCLE - (DEGREES_PER_ANIMATION) / 2;
    private const float WALK_FORWARD_END = (WALK_FORWARD_START + DEGREES_PER_ANIMATION) % DEGREES_IN_CIRCLE;
    private const float WALK_FORWARD_RIGHT_END = WALK_FORWARD_END + DEGREES_PER_ANIMATION;
    private const float WALK_RIGHT_END = WALK_FORWARD_RIGHT_END + DEGREES_PER_ANIMATION;
    private const float WALK_BACKWARD_RIGHT_END = WALK_RIGHT_END + DEGREES_PER_ANIMATION;
    private const float WALK_BACKWARD_END = WALK_BACKWARD_RIGHT_END + DEGREES_PER_ANIMATION;
    private const float WALK_BACKWARD_LEFT_END = WALK_BACKWARD_END + DEGREES_PER_ANIMATION;
    private const float WALK_LEFT_END = WALK_BACKWARD_LEFT_END + DEGREES_PER_ANIMATION;

    enum AnimationState
    {
        IDLE,
        WALK_FORWARD,
        WALK_FORWARD_RIGHT,
        WALK_RIGHT,
        WALK_BACKWARD_RIGHT,
        WALK_BACKWARD,
        WALK_BACKWARD_LEFT,
        WALK_LEFT,
        WALK_FORWARD_LEFT
    }

    private byte bulletsFired;

    private IObservableOptions observableOptionsManager;
    private PlayerManager.ObservableOptions observableOptions;
    private NetworkSimulation networkSimulation;

    private Animator animator;
    private AnimationState animationState;

    private Vector3 previousPosition;
    private Vector3 newPosition;
    private Quaternion previousRotation;
    private Quaternion newRotation;

    private PhotonView pView;

    private float timeBetweenUpdates;
    private float timeSinceLastUpdate;
    private float[] randomNumbers = new float[] { 0.111f, 0.92f, 0.51f, 0.32f, 0.71f, 0.21f, 0.42f, 0.82f, 0.61f };
    private int randomIndex;

    private float terrainLength;
    private float terrainWidth;
    private float worldBorderWidth = 1f;

    public override void OnEnable()
    {
        base.OnEnable();
        PhotonNetwork.NetworkingClient.EventReceived += OnPlayerDeath;

        observableOptionsManager.Attach(this);
        previousPosition = newPosition = transform.position;
        previousRotation = newRotation = transform.rotation;

        timeBetweenUpdates = 1.0f / PhotonNetwork.SerializationRate;
        timeSinceLastUpdate = 0f;
    }

    public override void OnDisable()
    {
        base.OnDisable();
        PhotonNetwork.NetworkingClient.EventReceived -= OnPlayerDeath;
        observableOptionsManager.Detach(this);
    }
    private void Awake()
    {
        pView = GetComponent<PhotonView>();
        observableOptionsManager = PlayerManager.instance;
        animator = GetComponent<Animator>();
    }

    private void Start()
    {
        animationState = AnimationState.IDLE;
        var _worldDivision = FindObjectOfType<WorldDivision>();
        terrainLength = _worldDivision.terrainLength;
        terrainWidth = _worldDivision.terrainWidth;
    }

    private void Update()
    {
        if (pView.IsMine)
        {
            // Don't move my local player
            return;
        }

        timeSinceLastUpdate += Time.smoothDeltaTime;
        float _lerpFraction = timeSinceLastUpdate / timeBetweenUpdates;
        //Debug.LogError(Time.time + " \t t " + _lerpFraction);

        if (_lerpFraction > 1.1f && observableOptions.extrapolation)
        {
            UpdatePositionWithExtrapolation();
            UpdateRotationWithExtrapolation();
            timeSinceLastUpdate = 0;
        }
        else
        {
            UpdatePosition(_lerpFraction);
            UpdateRotation(_lerpFraction);
        }

        UpdateAnimation();
        UpdateVFX();
    }

    private void UpdateVFX()
    {
        if (bulletsFired > 0 && !muzzleFlash.isPlaying)
        {
            muzzleFlash.Play();
            bulletsFired--;
        }
    }

    private void UpdateRotationWithExtrapolation()
    {
        // Predict new position
        float _previousRotationY = previousRotation.eulerAngles.y;
        float _newRotationY = newRotation.eulerAngles.y;

        int _direction = 0;
        float _moveAngle = 0f;
        float _difference = 0f;
        if (_previousRotationY > _newRotationY)
        {
            _difference = Mathf.Abs(_previousRotationY - _newRotationY);
            if (_difference > DEGREES_IN_CIRCLE / 2)
            {
                _direction = 1;
                _moveAngle = _newRotationY + (DEGREES_IN_CIRCLE - _previousRotationY);
            }
            else
            {
                _direction = -1;
                _moveAngle = _previousRotationY - _newRotationY;
            }
        }
        else
        {
            _difference = Mathf.Abs(_newRotationY - _previousRotationY);
            if (_difference > DEGREES_IN_CIRCLE / 2)
            {
                _direction = -1;
                _moveAngle = _previousRotationY + (DEGREES_IN_CIRCLE - _newRotationY);
            }
            else
            {
                _direction = 1;
                _moveAngle = _newRotationY - _previousRotationY;
            }
        }

        float _velocity = _moveAngle / timeSinceLastUpdate;
        _newRotationY += _direction * _velocity * timeSinceLastUpdate;
        if (_newRotationY < 0)
        {
            _newRotationY = DEGREES_IN_CIRCLE + _newRotationY;
        }
        _newRotationY %= DEGREES_IN_CIRCLE;

        newRotation = Quaternion.Euler(newRotation.x, _newRotationY, newRotation.z);
        previousRotation = transform.rotation;
        if (Mathf.Abs(_previousRotationY - _newRotationY) < 5)
        {
            newRotation = previousRotation = transform.rotation;
        }

        //UpdateRotation(Time.smoothDeltaTime / timeSinceLastUpdate);
    }

    private void UpdatePositionWithExtrapolation()
    {
        // Predict new rotation
        Vector3 _newPosition = new Vector3(newPosition.x, 0, newPosition.z);
        Vector3 _previousPosition = new Vector3(previousPosition.x, 0, previousPosition.z);
        float _velocity = Vector3.Distance(_newPosition, _previousPosition) / timeSinceLastUpdate;

        Vector3 _moveDirection = (_newPosition - _previousPosition).normalized;
        newPosition += _moveDirection * _velocity * timeSinceLastUpdate;
        newPosition = new Vector3(newPosition.x, transform.position.y, newPosition.z);


        // Check if player is outside the world borders and correct it if he is
        if (newPosition.x < worldBorderWidth)
        {
            newPosition.x = worldBorderWidth;
        }
        else if (newPosition.x > (terrainLength - worldBorderWidth))
        {
            newPosition.x = terrainLength - worldBorderWidth;
        }

        if (newPosition.z < worldBorderWidth)
        {
            newPosition.z = worldBorderWidth;
        }
        else if (newPosition.z > (terrainWidth - worldBorderWidth))
        {
            newPosition.z = terrainWidth - worldBorderWidth;
        }

        //Debug.LogError("Difference: " + Vector3.Distance(previousPosition, newPosition));
        if (Vector3.Distance(previousPosition, newPosition) <= 0.001f)
        {
            newPosition = transform.position;
        }
        previousPosition = transform.position;
        //UpdatePosition(Time.smoothDeltaTime / timeSinceLastUpdate);
    }

    private void UpdatePosition(float _lerpFraction)
    {
        if (!observableOptions.position || previousPosition.Equals(newPosition))
        {
            return;
        }

        if (observableOptions.interpolation)
        {
            transform.position = Vector3.Lerp(previousPosition, newPosition, _lerpFraction);
        }
        else
        {
            transform.position = newPosition;
        }
    }

    private void UpdateRotation(float _lerpFraction)
    {
        if (!observableOptions.rotation || previousRotation.Equals(newRotation))
        {
            return;

        }

        if (observableOptions.interpolation)
        {
            transform.rotation = Quaternion.Lerp(previousRotation, newRotation, _lerpFraction);
        }
        else
        {
            transform.rotation = newRotation;
        }
    }

    private void UpdateAnimation()
    {
        // Idle animation
        if (previousPosition.Equals(newPosition))
        {
            SetBlendTreeParams(AnimationState.IDLE);
            return;
        }

        float _movingDirectionAngleY = Quaternion.LookRotation(new Vector3(newPosition.x, 0, newPosition.z)
                            - new Vector3(previousPosition.x, 0, previousPosition.z)).eulerAngles.y;

        /**
         * Value that represents how much degrees look direction is missing to be 
         * at the center (0 degrees).
         */
        float _lookRotationDelta = DEGREES_IN_CIRCLE - transform.rotation.eulerAngles.y;
        // Shift move direction angle for calculated delta
        float _shiftedMoveAngleY = (_movingDirectionAngleY + _lookRotationDelta) % DEGREES_IN_CIRCLE;

        /**
         * Which animation will be displayed is now decided based on shifted moving angle value (y).
         * Look direction is treated as center (0 degrees).
         * Each animation gets its angle range in which it will be displayed.
         * There is 360 degrees in a circle and 8 animations that represents walking,
         * so each animation has range of approximately 45 degrees.
         * 
         * Let's say x represents shifted moving angle (y), x = [0, 360].
         * Here are some examples which animation will be triggered based on shifted moving angle:
         * 
         * walk_forward -> (x >= 337.5 || x < 22.5)
         * walk_forward_right -> (x >= 22.5 && x < 67.5)
         * walk_forward_left -> (x >= 292.5 && x < 337.5)
         * walk_backward -> ( x >= 157.5 && x < 202.5)
         * ...
         */

        switch (_shiftedMoveAngleY)
        {
            // WALK FORWARD ANIMATION
            case float x when (x >= WALK_FORWARD_START || x < WALK_FORWARD_END):
                SetBlendTreeParams(AnimationState.WALK_FORWARD);
                break;

            // WALK FORWARD-RIGHT ANIMATION
            case float x when (x >= WALK_FORWARD_END && x < WALK_FORWARD_RIGHT_END):
                SetBlendTreeParams(AnimationState.WALK_FORWARD_RIGHT);
                break;

            // WALK RIGHT ANIMATION
            case float x when (x >= WALK_FORWARD_RIGHT_END && x < WALK_RIGHT_END):
                SetBlendTreeParams(AnimationState.WALK_RIGHT);
                break;

            // WALK BACKWARD-RIGHT ANIMATION
            case float x when (x >= WALK_RIGHT_END && x < WALK_BACKWARD_RIGHT_END):
                SetBlendTreeParams(AnimationState.WALK_BACKWARD_RIGHT);
                break;

            // WALK BACKWARD ANIMATION
            case float x when (x >= WALK_BACKWARD_RIGHT_END && x < WALK_BACKWARD_END):
                SetBlendTreeParams(AnimationState.WALK_BACKWARD);
                break;

            // WALK BACKWARD-LEFT ANIMATION
            case float x when (x >= WALK_BACKWARD_END && x < WALK_BACKWARD_LEFT_END):
                SetBlendTreeParams(AnimationState.WALK_BACKWARD_LEFT);
                break;

            // WALK LEFT ANIMATION
            case float x when (x >= WALK_BACKWARD_LEFT_END && x < WALK_LEFT_END):
                SetBlendTreeParams(AnimationState.WALK_LEFT);
                break;

            // WALK FORWARD-LEFT ANIMATION
            case float x when (x >= WALK_LEFT_END && x < WALK_FORWARD_START):
                SetBlendTreeParams(AnimationState.WALK_FORWARD_LEFT);
                break;
        }
    }

    private void SetBlendTreeParams(AnimationState _newAnimationState)
    {
        if (_newAnimationState == animationState)
        {
            return;
        }

        animationState = _newAnimationState;

        switch (animationState)
        {
            case AnimationState.IDLE:
                animator.SetFloat("Horizontal", 0f);
                animator.SetFloat("Vertical", 0f);
                break;
            case AnimationState.WALK_FORWARD:
                animator.SetFloat("Horizontal", 0f);
                animator.SetFloat("Vertical", 1f);
                break;
            case AnimationState.WALK_FORWARD_RIGHT:
                animator.SetFloat("Horizontal", 1f);
                animator.SetFloat("Vertical", 1f);
                break;
            case AnimationState.WALK_RIGHT:
                animator.SetFloat("Horizontal", 1f);
                animator.SetFloat("Vertical", 0f);
                break;
            case AnimationState.WALK_BACKWARD_RIGHT:
                animator.SetFloat("Horizontal", 1f);
                animator.SetFloat("Vertical", -1f);
                break;
            case AnimationState.WALK_BACKWARD:
                animator.SetFloat("Horizontal", 0f);
                animator.SetFloat("Vertical", -1f);
                break;
            case AnimationState.WALK_BACKWARD_LEFT:
                animator.SetFloat("Horizontal", -1f);
                animator.SetFloat("Vertical", -1f);
                break;
            case AnimationState.WALK_LEFT:
                animator.SetFloat("Horizontal", -1f);
                animator.SetFloat("Vertical", 0f);
                break;
            case AnimationState.WALK_FORWARD_LEFT:
                animator.SetFloat("Horizontal", -1f);
                animator.SetFloat("Vertical", 1f);
                break;
        }
    }

    public void OnPlayerDeath(EventData photonEvent)
    {
        if (photonEvent.Code != PhotonRaiseEventCodes.PLAYER_DEAD)
        {
            return;
        }

        object[] _data = (object[])photonEvent.CustomData;
        int _senderActorNum = (int)_data[0];

        if (pView.CreatorActorNr == _senderActorNum)
        {
            animator.SetBool("IsDead", true);
            StartCoroutine(RespawnPlayer());
        }
    }

    private IEnumerator RespawnPlayer()
    {
        yield return new WaitForSeconds(respawnTime);
        animator.SetBool("IsDead", false);
    }

    public void OnPhotonSerializeView(PhotonStream stream, PhotonMessageInfo info)
    {
        if (stream.IsWriting)
        {
            // Position
            Vector3 _pos = transform.position;
            stream.SendNext(_pos.x);
            stream.SendNext(_pos.z);
            // Rotation
            stream.SendNext(transform.rotation.eulerAngles.y);
            // Combat
            stream.SendNext(bulletsFired);
            bulletsFired = 0;
        }
        else
        {
            if (PlayerManager.LocalPlayerPrefab != null && networkSimulation == null)
            {
                networkSimulation = PlayerManager.LocalPlayerPrefab.GetComponentInChildren<NetworkSimulation>();
            }
            // Position
            float posX = (float)stream.ReceiveNext();
            float posZ = (float)stream.ReceiveNext();
            // Rotation
            float rotationY = (float)stream.ReceiveNext();
            // Combat
            bulletsFired += (byte)stream.ReceiveNext();

            if (networkSimulation != null)
            {
                float _packetLoss = networkSimulation.GetPacketLossPercentage() / 100.0f;
                float _rand = randomNumbers[randomIndex];
                randomIndex = (randomIndex + 1) % randomNumbers.Length;

                if ((1.0f - _packetLoss) > _rand)
                {
                    previousPosition = transform.position;
                    newPosition = new Vector3(posX, transform.position.y, posZ);
                    previousRotation = transform.rotation;
                    newRotation = Quaternion.Euler(previousRotation.x, rotationY, previousRotation.z);

                    timeSinceLastUpdate = 0;
                }
            }
        }
    }

    public void OnObservableOptionsChange(PlayerManager.ObservableOptions newObservableOptions)
    {
        observableOptions = newObservableOptions;
    }

    public int GetRespawnTime()
    {
        return respawnTime;
    }

    public void BulletsFired(byte _amount)
    {
        bulletsFired += _amount;
    }

}
