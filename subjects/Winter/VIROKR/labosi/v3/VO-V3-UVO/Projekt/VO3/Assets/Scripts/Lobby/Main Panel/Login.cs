using UnityEngine;
using UnityEngine.UI;
using Photon.Pun;
using Photon.Realtime;

public sealed class Login : BasePanel
{
    [Header("Login UI")]
    [SerializeField] InputField playerNameInput;
    [SerializeField] Text placeholder;

    [Header("Referenced Panels")]
    [SerializeField] GameObject gameOptionsPanel;

    public override void Start()
    {
        base.Start();
        playerNameInput.ActivateInputField();
    }

    public void OnLoginButtonClicked()
    {
        string _playerName = playerNameInput.text;

        if (IsValid(out ErrorInfo _validation, _playerName))
        {
            PhotonNetwork.LocalPlayer.NickName = _playerName;
            PhotonNetwork.ConnectUsingSettings();   // Connects to fixed server ("eu")
        }
        else
        {
            playerNameInput.text = "";  // Sets placeholder as active
            placeholder.fontSize = _validation.fontSize;
            placeholder.text = _validation.message;
            placeholder.color = _validation.textColor;
        }
    }

    private bool IsValid(out ErrorInfo _errorInfo, string _playerName)
    {
        _errorInfo = new ErrorInfo
        {
            textColor = Color.red,
            fontSize = 40
        };

        if (string.IsNullOrEmpty(_playerName))
        {
            _errorInfo.isError = true;
            _errorInfo.message = "Player name must not be empty.";
        }

        if (!IsAlphaNumeric(_playerName))
        {
            _errorInfo.isError = true;
            _errorInfo.message = "Only alphanumeric characters are allowed.";
        }

        return !_errorInfo.isError;
    }

    public override void OnConnectedToMaster()
    {
        ActivatePanel(gameOptionsPanel);
    }

}