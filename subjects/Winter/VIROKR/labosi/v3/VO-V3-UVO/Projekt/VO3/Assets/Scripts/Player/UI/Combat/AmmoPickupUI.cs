using UnityEngine;
using UnityEngine.UI;

public class AmmoPickupUI : MonoBehaviour
{
    [SerializeField] Text ammoPickupText;

    private void Start()
    {
        ammoPickupText.text = "";
    }

    public void UpdateAmmoPickupText(string _objectName, double _pickupTime)
    {
        string _newText = $"Picked: {_objectName}\n";
        _newText += $"Time: {_pickupTime}";
        ammoPickupText.text = _newText;
    }

}
