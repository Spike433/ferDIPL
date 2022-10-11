using UnityEngine;
using UnityEngine.UI;
using static PlayerUIManager.UIState;

public class InGameOptions : MonoBehaviour
{
    [SerializeField] Slider mouseSensitivitySlider;
    [SerializeField] Text mouseSensitivityText;
    [SerializeField] Slider runningVelocitySlider;
    [SerializeField] Text runningVelocityText;

    private PlayerUIManager playerUIManager;
    private Movement playerMovement;

    private void Awake()
    {
        playerUIManager = GetComponentInParent<PlayerUIManager>();
        playerMovement = playerUIManager.GetComponentInParent<Movement>();
    }

    private void OnEnable()
    {
        // Set default text and slider values
        int _mouseSensitivity = (int)playerMovement.lookSensitivity;
        mouseSensitivityText.text = $"VALUE: {_mouseSensitivity}";
        mouseSensitivitySlider.value = _mouseSensitivity;

        int _runningVelocity = (int)playerMovement.runningVelocity;
        runningVelocityText.text = $"VALUE: {_runningVelocity}";
        runningVelocitySlider.value = _runningVelocity;
    }

    public void OnMouseSensitivityChanged()
    {
        int _mouseSensitivity = (int)mouseSensitivitySlider.value;
        mouseSensitivityText.text = $"VALUE: {_mouseSensitivity}";
        playerMovement.lookSensitivity = _mouseSensitivity;
    }

    public void OnRunningVelocityChanged()
    {
        int _runningVelocity = (int)runningVelocitySlider.value;
        runningVelocityText.text = $"VALUE: {_runningVelocity}";
        playerMovement.runningVelocity = _runningVelocity;
    }

    public void OnBackButtonClicked()
    {
        playerUIManager.SetUIState(InPauseScreen);
    }

    public void OnResumeButtonClicked()
    {
        playerUIManager.SetUIState(OnResume);
    }
}
