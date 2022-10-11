public static class PhotonRaiseEventCodes
{
    /**
     * Initially photon offers codes in range [0, 199] to use in raise event functions.
     * 0 is reserved for caching events.
     * Event codes in range [1, 199] are free to use if they are not already declared below.
     */
    public const int AMMO_PICKUP_REQ = 189;
    public const int AMMO_PICKUP_ACK = 190;
    public const int PLAYER_DEAD = 191;
}
