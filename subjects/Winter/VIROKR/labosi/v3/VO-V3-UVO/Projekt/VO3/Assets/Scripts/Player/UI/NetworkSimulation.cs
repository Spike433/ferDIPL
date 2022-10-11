using Photon.Pun;
using Photon.Realtime;
using UnityEngine;
using UnityEngine.UI;

public class NetworkSimulation : MonoBehaviour
{

    [SerializeField] Toggle networkSimulationToggle;
    [SerializeField] Text additionalPingText;
    [SerializeField] Slider additionalPingSlider;
    [SerializeField] Text packetLossText;
    [SerializeField] Slider packetLossSlider;

    private LoadBalancingPeer networkHandler;
    private int packetLossPercentage;
    private int latency;
    private Color defaultTextColor;

    private void Awake()
    {
        networkHandler = PhotonNetwork.NetworkingClient.LoadBalancingPeer;
        defaultTextColor = additionalPingText.color;
        additionalPingText.color = Color.white;
        packetLossText.color = Color.white;
    }

    void Start()
    {
        networkSimulationToggle.isOn = false;
        additionalPingSlider.value = 0;
        packetLossSlider.value = 0;
        additionalPingText.text = $"{latency * 2} ms";
        packetLossText.text = $"{packetLossPercentage}%";
    }

    public void OnPingValueChange()
    {
        latency = (int)additionalPingSlider.value;
        additionalPingText.text = $"{latency * 2} ms";

        bool _simulationEnabled = networkSimulationToggle.isOn;
        networkHandler.IsSimulationEnabled = _simulationEnabled && latency != 0;
        networkHandler.NetworkSimulationSettings.IncomingLag = _simulationEnabled ? latency : 0;
        networkHandler.NetworkSimulationSettings.OutgoingLag = _simulationEnabled ? latency : 0;
    }

    public void OnSimulationToggleChange()
    {
        bool _simulationEnabled = networkSimulationToggle.isOn;

        networkHandler.IsSimulationEnabled = _simulationEnabled && latency != 0;
        networkHandler.NetworkSimulationSettings.IncomingLag = _simulationEnabled ? latency : 0;
        networkHandler.NetworkSimulationSettings.OutgoingLag = _simulationEnabled ? latency : 0;

        additionalPingText.color = _simulationEnabled ? defaultTextColor : Color.white;
        packetLossText.color = _simulationEnabled ? defaultTextColor : Color.white;
    }

    public void OnPacketLossPercentageChange()
    {
        packetLossPercentage = (int)packetLossSlider.value * 10;
        packetLossText.text = $"{packetLossPercentage}%";
    }

    public int GetPacketLossPercentage()
    {
        return (networkSimulationToggle.isOn) ? packetLossPercentage : 0;
    }

}
