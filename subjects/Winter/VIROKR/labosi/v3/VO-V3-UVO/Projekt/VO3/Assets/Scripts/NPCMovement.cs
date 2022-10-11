using Photon.Pun;
using UnityEngine;

public class NPCMovement : MonoBehaviour
{
    [SerializeField] float rotationSpeed = .3f;
    [SerializeField] float movementRadius = 10f;

    private Vector3 center;
    private float angle;
    PhotonView pView;

    private void Awake()
    {
        pView = GetComponent<PhotonView>();
    }

    private void Start()
    {
        center = transform.position;
        pView.Group = 16;
    }

    private void Update()
    {
        angle += rotationSpeed * Time.deltaTime;
        var _offset = new Vector3(Mathf.Sin(angle), 0, Mathf.Cos(angle)) * movementRadius;
        transform.position = center + _offset;

        Quaternion _lookRotation = Quaternion.LookRotation(transform.position - center);
        transform.rotation = _lookRotation;
    }

}
