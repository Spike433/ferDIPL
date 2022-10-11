using UnityEngine;
using UnityEngine.UI;
using static PlayerUIManager;

public class CombatStats : MonoBehaviour, IPlayerUIObserver
{
    [Header("Ammo UI references")]
    [SerializeField] Text currentAmmoText;
    [SerializeField] Color ammoTextColor;
    [SerializeField] Color noAmmoTextColor;

    [Header("Ammo settings")]
    [SerializeField] int currentAmmo = 20;

    [Header("Health UI references")]
    [SerializeField] Image healthBarImage;

    [Header("Health settings")]
    [SerializeField] float startHealth = 100f;
    [SerializeField] GameObject lowHealthIndicator;
    [SerializeField] float lowHealthLimit;

    private float currentHealth;
    private PlayerUIManager playerUIManager;
    private bool isRespawning;

    private void Awake()
    {
        playerUIManager = GetComponentInParent<PlayerUIManager>();
        playerUIManager.Attach(this);
    }

    private void OnEnable()
    {
        UpdateAmmoUI();
        ResetHealth();
    }

    private void UpdateAmmoUI()
    {
        currentAmmoText.text = (currentAmmo > 0) ? $"AMMO {currentAmmo}" : "NO AMMO";
        currentAmmoText.color = (currentAmmo > 0) ? ammoTextColor : noAmmoTextColor;
    }

    public void ResetHealth()
    {
        currentHealth = startHealth;
        lowHealthIndicator.SetActive(false);
        UpdateHealthUI();
    }

    private void UpdateHealthUI()
    {
        healthBarImage.fillAmount = currentHealth / startHealth;
    }

    public int GetCurrentAmmoAmount()
    {
        return currentAmmo;
    }

    public void IncreaseAmmo(int _ammoAmount)
    {
        currentAmmo += _ammoAmount;
        UpdateAmmoUI();
    }

    public void DecreaseAmmo(int _ammoAmount)
    {
        currentAmmo -= _ammoAmount;
        UpdateAmmoUI();
    }

    public bool DecreaseHealth(float _damageAmount)
    {
        // Prevent shooting at corpse
        if (isRespawning)
        {
            return false;
        }

        currentHealth -= _damageAmount;
        if (currentHealth <= 0)
        {
            playerUIManager.SetUIState(PlayerUIManager.UIState.Respawning);
            return true;
        }

        UpdateHealthUI();
        lowHealthIndicator.SetActive(currentHealth <= lowHealthLimit);
        return false;
    }

    public void OnUIChange(PlayerUIManager.UIState newState)
    {
        switch (newState)
        {
            case UIState.Respawning:
                isRespawning = true;
                break;
            case UIState.Alive:
                isRespawning = false;
                break;
        }
    }
}
