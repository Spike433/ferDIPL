using Photon.Pun;
using UnityEngine;
using System.Linq;
using System.Text.RegularExpressions;
using Photon.Realtime;

public abstract class BasePanel : MonoBehaviourPunCallbacks
{
    private static GameObject[] panels;

    protected struct ErrorInfo
    {
        public bool isError;
        public string reason;
        public string message;
        public int fontSize;
        public Color textColor;
    }

    public virtual void Start()
    {

        if (panels == null)
        {
            // Get the top container
            var parentTransform = transform.parent.transform;
            // Find all siblings
            panels = new GameObject[parentTransform.childCount];
            for (int i = 0; i < parentTransform.childCount; i++)
            {
                panels[i] = parentTransform.GetChild(i).gameObject;
            }

            if (PhotonNetwork.IsConnected)
            {
                /**
                 * If player is already connected that means he had just left game,
                 * so he should be redirected to game options panel.
                 */
                ActivatePanel(panels[1]);
            }
            else
            {
                // If player is not connect redirect him to login panel
                ActivatePanel(panels[0]);
            }

        }
    }

    protected void ActivatePanel(GameObject _panel)
    {
        panels.ToList().ForEach(
            p => p.SetActive(p.name.Equals(_panel.name))
        );
    }

    protected void LeaveLobby()
    {
        if (PhotonNetwork.InLobby)
        {
            PhotonNetwork.LeaveLobby();
        }
    }

    protected void JoinLobby()
    {
        if (!PhotonNetwork.InLobby)
        {
            PhotonNetwork.JoinLobby();
        }
    }

    protected bool IsAlphaNumeric(string _string)
    {
        Regex r = new Regex(@"^[a-zA-Z0-9\s,]*$");
        return r.IsMatch(_string);
    }

    public override void OnDisconnected(DisconnectCause cause)
    {
        ActivatePanel(panels[0]);
    }

    public void OnExitButtonClicked()
    {
        PhotonNetwork.Disconnect();
        Application.Quit();
    }

    private void OnDestroy()
    {
        panels = null;
    }
}