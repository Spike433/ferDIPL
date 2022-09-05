module SimulatedSocket where

import Helper             (seconds)
import Configuration      (defaultDelay, defaultLosses, defaultPieceLen)
import Data.ByteString    (ByteString)
import Control.Monad      (void, unless)
import Control.Concurrent (forkIO, threadDelay)
import System.Random      (randomIO)

import Network.BSD               (hostAddress, getHostByName)
import Network.Socket.Internal   (SockAddr(SockAddrInet))
import Network.Socket.ByteString (sendTo, recvFrom)
import Network.Socket (
  HostName, Socket, getAddrInfo, withSocketsDo,
  defaultProtocol, SocketType(Datagram), addrFamily, socket,
  addrAddress, bindSocket, AddrInfoFlag(AI_PASSIVE), addrFlags,
  defaultHints, PortNumber)

address :: HostName -> PortNumber -> IO SockAddr
address hostname port = do
  host <- hostAddress `fmap` getHostByName hostname
  return $ SockAddrInet port host

opensock :: HostName -> PortNumber -> IO Socket
opensock host port  = do
  server <- head `fmap` getAddrInfo Nothing (Just host) (Just $ show port)
  socket (addrFamily server) Datagram defaultProtocol

listen :: PortNumber -> IO Socket
listen port = do
  let hints = Just $ defaultHints { addrFlags = [AI_PASSIVE] }
  server <- head `fmap` getAddrInfo hints Nothing (Just $ show port)
  sock <- socket (addrFamily server) Datagram defaultProtocol
  bindSocket sock $ addrAddress server
  return sock

send :: Socket -> SockAddr -> ByteString -> IO ()
send sock addr message = void.forkIO $ do
  messageLost <- (defaultLosses >=) `fmap` randomIO
  unless messageLost $ do
    threadDelay . seconds . (defaultDelay *) . (0.5+) =<< randomIO
    void $ sendTo sock message addr

receive :: Socket -> IO (ByteString, SockAddr)
receive = flip recvFrom $ defaultPieceLen + 20

withNet :: IO a -> IO a
withNet = withSocketsDo

-- For using SockAddr as Data.Map keys.
instance Ord SockAddr where
  (SockAddrInet p h) `compare` (SockAddrInet p' h') =
    let portsEq = p `compare` p'
    in  if portsEq == EQ then h `compare` h' else portsEq
  _ `compare` _ = undefined
