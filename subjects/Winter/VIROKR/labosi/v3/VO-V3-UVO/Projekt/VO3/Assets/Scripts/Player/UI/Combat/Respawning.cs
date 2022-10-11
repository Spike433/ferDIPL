using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using static PlayerUIManager.UIState;

public class Respawning : MonoBehaviour
{
    [SerializeField] Text respawnText;

    private PlayerUIManager playerUIManager;
    private int initialRespawnTime;

    private void Awake()
    {
        playerUIManager = GetComponentInParent<PlayerUIManager>();
        initialRespawnTime = PlayerManager.LocalPlayerPrefab.GetComponent<PlayerSynchronization>().GetRespawnTime();
    }

    private void OnEnable()
    {
        respawnText.text = $"Respawning in {initialRespawnTime} seconds ...";
        StartCoroutine("RespawnTimer");
    }

    private IEnumerator RespawnTimer()
    {
        int _respawnTime = initialRespawnTime;

        while (_respawnTime > 0)
        {
            yield return new WaitForSeconds(1.0f);
            _respawnTime--;
            respawnText.text = $"Respawning in {_respawnTime} seconds...";
        }

        playerUIManager.SetUIState(Alive);
    }
}
