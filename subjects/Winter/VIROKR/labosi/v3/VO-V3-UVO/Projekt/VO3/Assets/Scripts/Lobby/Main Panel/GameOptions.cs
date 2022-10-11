using UnityEngine;

public sealed class GameOptions : BasePanel
{
    [Header("Referenced panels")]
    [SerializeField] GameObject createRoomPanel;
    [SerializeField] GameObject roomListPanel;

    public void OnCreateRoomButtonClicked()
    {
        ActivatePanel(createRoomPanel);
    }

    public void OnShowRoomListButtonClicked()
    {
        ActivatePanel(roomListPanel);
    }
}
