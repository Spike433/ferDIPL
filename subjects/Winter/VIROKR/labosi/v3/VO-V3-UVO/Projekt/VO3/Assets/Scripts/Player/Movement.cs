using UnityEngine;

public class Movement : MonoBehaviour
{
    public float lookSensitivity = 3f;
    public float runningVelocity = 100f;
    [SerializeField] float walkingVelocity = 5f;
    [SerializeField] GameObject fpsCamera;

    private Vector3 velocity = Vector3.zero;
    private Vector3 rotation = Vector3.zero;
    private float cameraUpDownRotation = 0f;
    private float currentCameraUpDownRotation = 0f;

    private Rigidbody rigidBody;
    private float currentVelocity;

    private float terrainLength;
    private float terrainWidth;
    private float worldBorderWidth = 1f;

    void Start()
    {
        currentVelocity = walkingVelocity;
        rigidBody = GetComponent<Rigidbody>();

        var _worldDivision = FindObjectOfType<WorldDivision>();
        terrainLength = _worldDivision.terrainLength;
        terrainWidth = _worldDivision.terrainWidth;
    }

    void Update()
    {
        currentVelocity = (Input.GetKey(KeyCode.Space)) ? runningVelocity : walkingVelocity;

        float _xMovement = Input.GetAxisRaw("Horizontal");
        float _zMovement = Input.GetAxisRaw("Vertical");

        Vector3 _movementHorizontal = transform.right * _xMovement;
        Vector3 _movementVertical = transform.forward * _zMovement;
        Vector3 _movementVelocity = (_movementVertical + _movementHorizontal).normalized * currentVelocity;

        Move(_movementVelocity);

        // Rotation
        float _yRotation = Input.GetAxis("Mouse X");
        Vector3 _rotationVector = new Vector3(0, _yRotation, 0) * lookSensitivity;

        Rotate(_rotationVector);

        float _cameraUpDown = Input.GetAxis("Mouse Y") * lookSensitivity;
        RotateCamera(_cameraUpDown);
    }

    private void FixedUpdate()
    {
        if (velocity != Vector3.zero)
        {
            Vector3 _newPosition = rigidBody.position + velocity * Time.fixedDeltaTime;

            /**
             * Check if player is outside the world borders and correct it if he is 
             * since colliders don't work well with fast moving objects.
             */
            if (_newPosition.x < worldBorderWidth)
            {
                _newPosition.x = worldBorderWidth;
            }
            else if (_newPosition.x > (terrainLength - worldBorderWidth))
            {
                _newPosition.x = terrainLength - worldBorderWidth;
            }

            if (_newPosition.z < worldBorderWidth)
            {
                _newPosition.z = worldBorderWidth;
            }
            else if (_newPosition.z > (terrainWidth - worldBorderWidth))
            {
                _newPosition.z = terrainWidth - worldBorderWidth;
            }

            rigidBody.MovePosition(_newPosition);
        }

        rigidBody.MoveRotation(rigidBody.rotation * Quaternion.Euler(rotation));

        if (fpsCamera != null)
        {
            currentCameraUpDownRotation -= cameraUpDownRotation;
            currentCameraUpDownRotation = Mathf.Clamp(currentCameraUpDownRotation, -85, 85);
            fpsCamera.transform.localEulerAngles = new Vector3(currentCameraUpDownRotation, 0, 0);
        }
    }

    private void Move(Vector3 movementVelocity)
    {
        velocity = movementVelocity;
    }

    private void Rotate(Vector3 rotationVector)
    {
        rotation = rotationVector;
    }

    private void RotateCamera(float cameraUpDown)
    {
        cameraUpDownRotation = cameraUpDown;
    }
}
