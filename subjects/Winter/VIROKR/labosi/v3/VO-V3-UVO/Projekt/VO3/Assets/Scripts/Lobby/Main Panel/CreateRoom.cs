using System.Collections.Generic;
using System.Linq;
using Photon.Pun;
using Photon.Realtime;
using UnityEngine;
using UnityEngine.UI;

public sealed class CreateRoom : BasePanel
{
    // Parameters
    [Header("Create Room UI")]
    [SerializeField] InputField roomNameInput;
    [SerializeField] InputField maxPlayersInput;
    [SerializeField] Text roomNamePlaceholder;
    [SerializeField] Text maxPlayersPlaceholder;

    [Header("Referenced Panels")]
    [SerializeField] GameObject gameOptionsPanel;
    [SerializeField] GameObject insideRoomPanel;

    // Properties
    private List<string> roomListNames;
    private const int minNumOfPlayers = 3;
    private const int maxNumOfPlayers = 5;

    public override void OnEnable()
    {
        base.OnEnable();
        JoinLobby();
    }
    public override void OnDisable()
    {
        base.OnDisable();
        LeaveLobby();
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.Tab)
            && !maxPlayersInput.isFocused)
        {
            maxPlayersInput.ActivateInputField();
        }
    }

    public override void OnRoomListUpdate(List<RoomInfo> roomList)
    {
        roomListNames = roomList.Select(r => r.Name).ToList();
    }

    public void OnCreateRoomButtonClicked()
    {
        bool canCreate = IsValid(out ErrorInfo _roomNameValidation, out ErrorInfo _maxPlayersValidation);

        if (canCreate)
        {
            RoomOptions _roomOptions = new RoomOptions
            {
                IsVisible = true,
                MaxPlayers = (byte)int.Parse(maxPlayersInput.text)
            };
            PhotonNetwork.CreateRoom(roomNameInput.text, _roomOptions);
        }
        else
        {
            if (_roomNameValidation.isError)
            {
                roomNameInput.text = "";
                roomNamePlaceholder.text = _roomNameValidation.message;
                roomNamePlaceholder.color = _roomNameValidation.textColor;
            }
            if (_maxPlayersValidation.isError)
            {
                maxPlayersInput.text = "";
                maxPlayersPlaceholder.text = _maxPlayersValidation.message;
                maxPlayersPlaceholder.color = _maxPlayersValidation.textColor;
            }
        }
    }

    private bool IsValid(out ErrorInfo _roomNameValidation, out ErrorInfo _maxPlayersValidation)
    {
        _roomNameValidation = new ErrorInfo
        {
            textColor = Color.red
        };
        _maxPlayersValidation = new ErrorInfo
        {
            textColor = Color.red
        };

        // Validate room name
        string _roomName = roomNameInput.text;
        if (string.IsNullOrEmpty(_roomName))
        {
            _roomNameValidation.isError = true;
            _roomNameValidation.message = "Name must not be empty.";
        }
        else if (!IsAlphaNumeric(_roomName))
        {
            _roomNameValidation.isError = true;
            _roomNameValidation.message = "Name can contain only alphanumeric characters!";
        }
        else if (roomListNames.Contains(_roomName))
        {
            _roomNameValidation.isError = true;
            _roomNameValidation.message = "Name already exists.";
        }

        // Validate number of max. players
        string _maxPlayers = maxPlayersInput.text;
        if (string.IsNullOrEmpty(_maxPlayers))
        {
            _maxPlayersValidation.isError = true;
            _maxPlayersValidation.message = "Field must not be empty.";
            return !_roomNameValidation.isError && !_maxPlayersValidation.isError;
        }

        bool isNumeric = int.TryParse(_maxPlayers, out int n);
        if (!isNumeric)
        {
            _maxPlayersValidation.isError = true;
            _maxPlayersValidation.message = "Field accepts numbers only!";
        }
        else if (n < minNumOfPlayers || n > maxNumOfPlayers)
        {
            _maxPlayersValidation.isError = true;
            _maxPlayersValidation.message = $"Range [{minNumOfPlayers}, {maxNumOfPlayers}]";
        }

        return !_roomNameValidation.isError && !_maxPlayersValidation.isError;
    }

    public override void OnJoinedRoom()
    {
        ActivatePanel(insideRoomPanel);
    }

    public void OnCancelButtonClicked()
    {
        ActivatePanel(gameOptionsPanel);
    }
}