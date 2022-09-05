package hr.fer.rassus.firsthomework.client;

public interface ServerIf {
    // Server startup. Starts all services offered by the server.
    public void startup();

    // Server loops when in running mode. The server must be active
    // to accept client requests.
    public void loop();

    // Server shutdown. Shuts down all services started during
    // startup.
    public void shutdown();

    // Gets the running flag that indicates server running status.
    // @return running flag
    public boolean getRunningFlag();
}