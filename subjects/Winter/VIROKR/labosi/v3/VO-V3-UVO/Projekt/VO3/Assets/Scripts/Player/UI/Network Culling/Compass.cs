using UnityEngine;
using UnityEngine.UI;

public class Compass : MonoBehaviour
{
    [SerializeField] RawImage compassImage;
    [SerializeField] Transform playerTransform;

    private void Update()
    {
        compassImage.uvRect = new Rect(((playerTransform.localEulerAngles.y + 90) % 360) / 360, 0, 1, 1);
    }
}
