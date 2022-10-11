using UnityEngine;
using UnityEngine.UI;
using Photon.Pun;

public class GameStats : MonoBehaviour
{
    [SerializeField] Text killsText;
    [SerializeField] Text fpsText;
    [SerializeField] Text pingText;

    private int currentKills;
    private int frameCount;
    private float deltaTime;

    private void Start()
    {
        killsText.text = $"\tKILLS: {currentKills}";
    }

    void Update()
    {
        frameCount++;
        deltaTime += Time.deltaTime;
        if (deltaTime >= 1.0f)
        {
            pingText.text = $"PING: {PhotonNetwork.GetPing()} ms";
            fpsText.text = $"FPS: {frameCount}";
            deltaTime = 0f;
            frameCount = 0;
        }
    }

    public void TargetKilled()
    {
        currentKills++;
        killsText.text = $"\tKILLS: {currentKills}";
    }
}
