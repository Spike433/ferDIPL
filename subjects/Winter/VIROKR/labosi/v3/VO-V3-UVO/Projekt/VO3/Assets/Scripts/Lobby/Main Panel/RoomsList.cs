using Photon.Pun;
using Photon.Realtime;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.UI;

public sealed class RoomsList : BasePanel
{
    [Header("Room List UI")]
    [SerializeField] GameObject roomListEntryPrefab;
    [SerializeField] GameObject roomListEntriesParent;

    [Header("Referenced panels")]
    [SerializeField] GameObject gameOptionsPanel;
    [SerializeField] GameObject insideRoomPanel;

    private Dictionary<string, RoomInfo> cachedRoomList;
    private Dictionary<string, GameObject> roomListGameObjects;

    new void Start()
    {
        cachedRoomList = new Dictionary<string, RoomInfo>();
        roomListGameObjects = new Dictionary<string, GameObject>();
    }
    public override void OnEnable()
    {
        base.OnEnable();
        JoinLobby();
    }

    public override void OnRoomListUpdate(List<RoomInfo> roomList)
    {
        ClearRoomListView();
        roomList.ForEach(r => CacheRoom(r));
        UpdateRoomListView();
    }

    public override void OnJoinRoomFailed(short returnCode, string message)
    {
        Debug.LogError($"{returnCode} = {message}");
    }

    private void OnJoinRoomButtonClicked(string _roomName)
    {
        LeaveLobby();
        PhotonNetwork.JoinRoom(_roomName);
    }

    public override void OnJoinedRoom()
    {
        ActivatePanel(insideRoomPanel);
    }

    private void UpdateRoomListView()
    {
        foreach (RoomInfo room in cachedRoomList.Values)
        {
            string name = room.Name;

            // Instantiate list entry prefab
            GameObject roomListEntry = Instantiate(roomListEntryPrefab);
            Transform entryTransform = roomListEntry.transform;
            entryTransform.SetParent(roomListEntriesParent.transform);
            entryTransform.localScale = Vector3.one;

            // Update list entry UI
            string populationInfo = room.PlayerCount + " / " + room.MaxPlayers;
            entryTransform.Find("RoomPlayersText").GetComponent<Text>().text = populationInfo;
            entryTransform.Find("RoomNameText").GetComponent<Text>().text = name;

            Button joinButton = entryTransform.Find("JoinRoomButton").GetComponent<Button>();
            joinButton.onClick.AddListener(() => OnJoinRoomButtonClicked(name));
            joinButton.enabled = (room.PlayerCount != room.MaxPlayers);

            // Cache list view entries
            roomListGameObjects.Add(name, roomListEntry);
        }
    }

    private void CacheRoom(RoomInfo room)
    {
        string name = room.Name;

        // Remove unavailable rooms
        if (!room.IsOpen || !room.IsVisible || room.RemovedFromList)
        {
            cachedRoomList.Remove(name);
            return;
        }

        if (cachedRoomList.ContainsKey(name))
        {
            cachedRoomList[name] = room;    // Update room
        }
        else
        {
            cachedRoomList.Add(name, room);  // Cache room
        }
    }

    private void ClearRoomListView()
    {
        roomListGameObjects.Values.ToList().ForEach(r => Destroy(r));
        roomListGameObjects.Clear();
    }

    public void OnBackButtonClicked()
    {
        LeaveLobby();
        ActivatePanel(gameOptionsPanel);
    }

    public override void OnLeftLobby()
    {
        ClearRoomListView();
        cachedRoomList.Clear();
    }
}