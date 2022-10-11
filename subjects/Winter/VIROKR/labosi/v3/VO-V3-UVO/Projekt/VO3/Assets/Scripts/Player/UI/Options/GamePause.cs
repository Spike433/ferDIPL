using Photon.Pun;
using UnityEngine;
using UnityEngine.SceneManagement;
using static PlayerUIManager.UIState;

public class GamePause : MonoBehaviourPunCallbacks
{

    private PlayerUIManager playerUIManager;

    private void Awake()
    {
        playerUIManager = GetComponentInParent<PlayerUIManager>();
    }

    public void OnResumeButtonClicked()
    {
        playerUIManager.SetUIState(OnResume);
    }

    public void OnOptionsButtonClicked()
    {
        playerUIManager.SetUIState(InOptionsScreen);
    }

    public void OnLeaveGameButtonClicked()
    {
        PhotonNetwork.LeaveRoom();
        SceneManager.LoadScene(0);
    }

    public void OnExitGameButtonClicked()
    {
        PhotonNetwork.Disconnect();
        Application.Quit();
    }

}
