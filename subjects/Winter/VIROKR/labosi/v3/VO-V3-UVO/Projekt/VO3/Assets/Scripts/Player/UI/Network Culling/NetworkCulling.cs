using ExitGames.Client.Photon;
using Photon.Pun;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using UnityEngine.UI;

public class NetworkCulling : MonoBehaviour
{
    [SerializeField] Transform playerTransform;

    // Parameters
    [Header("Culling parameters")]
    [SerializeField] int max_AOIM_radius;
    [SerializeField] int min_AOIM_radius;
    [Tooltip("In seconds.")] [SerializeField] float cullingFrequency = 1.0f;

    [Header("Network Culling UI")]
    [SerializeField] Text myZoneText;
    [SerializeField] Text adjacentZonesText;
    [SerializeField] Text incomingMessagesPerSecondText;
    [SerializeField] Text outgoingMessagesPerSecondText;
    [SerializeField] Toggle enableCullingToggle;
    [SerializeField] Toggle dynamicAoimToggle;
    [SerializeField] Text criticalZonesText;

    // Cached
    private WorldDivision zoneManager;
    private PhotonView pView;

    // Properties
    private WorldDivision.Cell myZone;
    private LinkedList<WorldDivision.Cell> adjacentZones;

    private TrafficStatsGameLevel networkStats;
    private int totalIncomingMessagesLastUpdate;
    private int incomingMessagesPerSecond;
    private int totalOutgoingMessagesLastUpdate;
    private int current_AOIM_radius;
    private float timeSinceLastUpdate;
    private int networkOverloadThreshold;
    private LinkedList<int> criticalZones;

    private void Awake()
    {
        zoneManager = FindObjectOfType<WorldDivision>();
        pView = playerTransform.GetComponent<PhotonView>();
    }

    private void Start()
    {
        criticalZones = new LinkedList<int>();
        networkOverloadThreshold = (PhotonNetwork.CurrentRoom.PlayerCount - 1) * 8;

        // Enable network traffic analysis
        var loadBalancingPeer = PhotonNetwork.NetworkingClient.LoadBalancingPeer;
        loadBalancingPeer.TrafficStatsEnabled = true;
        networkStats = loadBalancingPeer.TrafficStatsGameLevel;

        enableCullingToggle.isOn = false;
        dynamicAoimToggle.isOn = false;
        current_AOIM_radius = max_AOIM_radius;

        timeSinceLastUpdate = Time.unscaledTime;
    }

    private void Update()
    {
        float _currentTime = Time.unscaledTime;
        if ((_currentTime - timeSinceLastUpdate) >= cullingFrequency)
        {
            timeSinceLastUpdate = _currentTime;
            UpdateZonesInfo();
            SetInterestGroups();
            UpdateUI();
            CheckForNetworkOverload();
        }
    }

    private void CheckForNetworkOverload()
    {
        if (dynamicAoimToggle.isOn)
        {
            if (criticalZones.Count == 0 && incomingMessagesPerSecond >= networkOverloadThreshold)
            {
                criticalZones = new LinkedList<int>(adjacentZones.Select(c => c.Id).ToList());
                criticalZones.AddLast(myZone.Id);
                UpdateAOIM();
            }
            else
            {
                UpdateAOIM();
            }
        }
        else
        {
            criticalZones.Clear();
            UpdateAOIM();
        }

        // Adjacent zones text
        StringBuilder sb = new StringBuilder();
        sb.Append("Critical zones: ");
        if (criticalZones.Count == 0)
        {
            sb.Append("none");
        }
        else
        {
            criticalZones.ToList().ForEach(z => sb.Append(z.ToString() + ", "));
        }
        string _text = sb.ToString();
        if (!_text.Contains("none"))
        {
            _text = _text.Remove(_text.Length - 2, 2);
        }
        criticalZonesText.text = _text;

    }

    private void UpdateAOIM()
    {
        if (criticalZones.Contains(myZone.Id))
        {
            current_AOIM_radius = min_AOIM_radius;
        }
        else
        {
            criticalZones.Clear();
            current_AOIM_radius = max_AOIM_radius;
        }
    }

    private void UpdateZonesInfo()
    {
        myZone = zoneManager.FindMyZone(playerTransform.position);
        adjacentZones = zoneManager.GetNeighbours(playerTransform.position, current_AOIM_radius);
    }

    private void UpdateUI()
    {
        // Traffic stats
        int _totalIncomingMessages = networkStats.TotalIncomingMessageCount;
        incomingMessagesPerSecond = _totalIncomingMessages - totalIncomingMessagesLastUpdate;
        incomingMessagesPerSecondText.text = $"Incoming messages/s: {incomingMessagesPerSecond}";
        totalIncomingMessagesLastUpdate = _totalIncomingMessages;

        int _totalOutgoingMessages = networkStats.TotalOutgoingMessageCount;
        outgoingMessagesPerSecondText.text = $"Outgoing messages/s: {_totalOutgoingMessages - totalOutgoingMessagesLastUpdate}";
        totalOutgoingMessagesLastUpdate = _totalOutgoingMessages;

        // My zone text
        myZoneText.text = $"In zone {myZone.Id}";

        // Adjacent zones text
        StringBuilder sb = new StringBuilder();
        sb.Append("Neighbours: ");
        if (adjacentZones.Count == 0)
        {
            sb.Append("none");
        }
        else
        {
            adjacentZones.ToList().ForEach(z => sb.Append(z.Id + ", "));
        }
        string _text = sb.ToString();
        if (!_text.Contains("none"))
        {
            _text = _text.Remove(_text.Length - 2, 2);
        }
        adjacentZonesText.text = _text;
    }

    private void SetInterestGroups()
    {
        // Send updates only to my group
        pView.Group = (byte)myZone.Id;

        int numOfGroups = enableCullingToggle.isOn ? (adjacentZones.Count + 1) : zoneManager.Cells.Count;
        byte[] enableGroups = new byte[numOfGroups];

        if (enableCullingToggle.isOn)
        {
            for (int i = 0; i < adjacentZones.Count; i++)
            {
                enableGroups[i] = (byte)adjacentZones.ElementAt(i).Id;
            }
            enableGroups[numOfGroups - 1] = (byte)myZone.Id;
        }
        else
        {
            for (int i = 0; i < numOfGroups; i++)
            {
                enableGroups[i] = (byte)(i + 1); // Index of 1st available group is 1
            }
        }

        PhotonNetwork.SetInterestGroups(new byte[0], enableGroups);
    }

    public int Get_AOIM_Radius()
    {
        return current_AOIM_radius;
    }

    public float GetCullingFrequency()
    {
        return cullingFrequency;
    }

}
