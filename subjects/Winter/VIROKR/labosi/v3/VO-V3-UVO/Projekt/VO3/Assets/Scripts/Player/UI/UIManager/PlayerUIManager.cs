using System.Collections.Generic;
using UnityEngine;

public class PlayerUIManager : MonoBehaviour, IPlayerUIManager
{
    public enum UIState
    {
        Alive,
        Respawning,
        InPauseScreen,
        InOptionsScreen,
        OnResume
    }

    [SerializeField] GameObject gameStatsUI;
    [SerializeField] GameObject networkCullingUI;
    [SerializeField] GameObject networkSimulationUI;
    [SerializeField] GameObject deadReckoningUI;
    [SerializeField] GameObject synchronizationUI;
    [SerializeField] GameObject ammoPickupUI;

    [SerializeField] GameObject combatStatsUI;
    [SerializeField] GameObject respawnUI;
    [SerializeField] GameObject pauseScreenUI;
    [SerializeField] GameObject optionsScreenUI;

    private List<IPlayerUIObserver> observers = new List<IPlayerUIObserver>();
    private UIState state;

    private void OnEnable()
    {
        // Always active
        gameStatsUI.SetActive(true);
        networkCullingUI.SetActive(true);
        networkSimulationUI.SetActive(true);
        deadReckoningUI.SetActive(true);
        synchronizationUI.SetActive(true);
        ammoPickupUI.SetActive(true);

        pauseScreenUI.SetActive(false);
        optionsScreenUI.SetActive(false);

        SetUIState(UIState.Alive);
    }

    private void OnDisable()
    {
        gameStatsUI.SetActive(false);
        networkCullingUI.SetActive(false);
        combatStatsUI.SetActive(false);
        respawnUI.SetActive(false);
        pauseScreenUI.SetActive(false);
        optionsScreenUI.SetActive(false);
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            SetUIState((state == UIState.InPauseScreen || state == UIState.InOptionsScreen) ? UIState.OnResume : UIState.InPauseScreen);
        }
    }

    public void SetUIState(UIState _state)
    {
        this.state = _state;
        Notify();

        switch (state)
        {
            case UIState.Alive:
                OnAlive();
                break;
            case UIState.Respawning:
                OnRespawning();
                break;
            case UIState.InPauseScreen:
                OnPauseScreen();
                break;
            case UIState.InOptionsScreen:
                OnOptionsScreen();
                break;
            case UIState.OnResume:
                OnResume();
                break;
        }
    }


    private void OnAlive()
    {
        combatStatsUI.SetActive(true);
        respawnUI.SetActive(false);
    }

    private void OnRespawning()
    {
        combatStatsUI.SetActive(false);
        respawnUI.SetActive(true);
    }

    private void OnPauseScreen()
    {
        pauseScreenUI.SetActive(true);
        optionsScreenUI.SetActive(false);
    }

    private void OnOptionsScreen()
    {
        optionsScreenUI.SetActive(true);
        pauseScreenUI.SetActive(false);
    }

    private void OnResume()
    {
        optionsScreenUI.SetActive(false);
        pauseScreenUI.SetActive(false);
    }

    public void Attach(IPlayerUIObserver observer)
    {
        observers.Add(observer);
    }

    public void Detach(IPlayerUIObserver observer)
    {
        observers.Remove(observer);
    }

    public void Notify()
    {
        foreach (var observer in observers)
        {
            observer.OnUIChange(state);
        }
    }
}
