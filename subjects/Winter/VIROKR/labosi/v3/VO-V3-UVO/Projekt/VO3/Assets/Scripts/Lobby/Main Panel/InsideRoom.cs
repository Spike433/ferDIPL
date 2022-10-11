using Photon.Pun;
using Photon.Realtime;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using UnityEngine.UI;

public sealed class InsideRoom : BasePanel
{
    // Parameters
    [Header("Inside Room UI")]
    [SerializeField] Text roomInfoText;
    [SerializeField] GameObject startGameButton;

    [Header("Player List Entry")]
    [SerializeField] GameObject playerListPrefab;
    [SerializeField] GameObject playerListContainer;

    [Header("Referenced Panels")]
    [SerializeField] GameObject gameOptionsPanel;

    // Properties
    private Dictionary<int, GameObject> playerListGameObjects;
    private const string levelName = "GameWorld";

    public override void OnEnable()
    {
        base.OnEnable();
        PhotonNetwork.AutomaticallySyncScene = true;
        JoinLobby();
        UpdateRoomInfo();
    }

    private void UpdateRoomInfo()
    {
        UpdateRoomInfoText();
        startGameButton.SetActive(PhotonNetwork.LocalPlayer.IsMasterClient);

        if (playerListGameObjects == null)
        {
            playerListGameObjects = new Dictionary<int, GameObject>();
        }
        foreach (Player player in PhotonNetwork.PlayerList)
        {
            AddPlayerInRoomList(player);
        }
    }

    public override void OnPlayerEnteredRoom(Player newPlayer)
    {
        UpdateRoomInfoText();
        AddPlayerInRoomList(newPlayer);
    }

    public override void OnPlayerLeftRoom(Player otherPlayer)
    {
        UpdateRoomInfoText();
        Destroy(playerListGameObjects[otherPlayer.ActorNumber].gameObject);
        playerListGameObjects.Remove(otherPlayer.ActorNumber);

        // In case master left room and you are the new one
        startGameButton.SetActive(PhotonNetwork.LocalPlayer.IsMasterClient);
        playerListGameObjects[PhotonNetwork.MasterClient.ActorNumber]
                                     .transform
                                     .Find("MasterIndicator")
                                     .gameObject
                                     .SetActive(true);
    }

    public void OnLeaveGameButtonClicked()
    {
        DestroyListEntries();
        PhotonNetwork.LeaveRoom();
        LeaveLobby();

        ActivatePanel(gameOptionsPanel);
    }

    private void DestroyListEntries()
    {
        foreach (GameObject player in playerListGameObjects.Values)
        {
            Destroy(player);
        }
        playerListGameObjects.Clear();
        playerListGameObjects = null;
    }

    private void AddPlayerInRoomList(Player newPlayer)
    {
        GameObject playerListEntry = Instantiate(playerListPrefab);

        Transform playerTransform = playerListEntry.transform;
        playerTransform.SetParent(playerListContainer.transform);
        playerTransform.localScale = Vector3.one;

        playerTransform.Find("PlayerNameText").GetComponent<Text>().text = newPlayer.NickName;
        playerTransform.Find("PlayerIndicator").gameObject
                       .SetActive(newPlayer.ActorNumber == PhotonNetwork.LocalPlayer.ActorNumber);
        playerTransform.Find("MasterIndicator").gameObject
                       .SetActive(PhotonNetwork.MasterClient.ActorNumber == newPlayer.ActorNumber);

        playerListGameObjects.Add(newPlayer.ActorNumber, playerListEntry);
    }

    private void UpdateRoomInfoText()
    {
        StringBuilder sb = new StringBuilder();
        sb.Append("Room: ");
        sb.Append(PhotonNetwork.CurrentRoom.Name);
        sb.Append(", ");
        sb.Append("Players: ");
        sb.Append(PhotonNetwork.CurrentRoom.PlayerCount);
        sb.Append("/");
        sb.Append(PhotonNetwork.CurrentRoom.MaxPlayers);
        roomInfoText.text = sb.ToString();
    }

    public void OnStartGameButtonClicked()
    {
        if (PhotonNetwork.IsMasterClient)
        {
            var _roomOptions = PhotonNetwork.CurrentRoom;
            _roomOptions.IsVisible = false;
            _roomOptions.IsOpen = false;
            PhotonNetwork.LoadLevel(levelName);
        }
    }
}
