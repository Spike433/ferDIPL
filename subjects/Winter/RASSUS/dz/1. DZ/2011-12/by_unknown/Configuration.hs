module Configuration where

import Network.Socket (HostName, PortNumber)

defaultHost :: HostName
defaultHost = "localhost"

defaultPort :: PortNumber
defaultPort = 3000

defaultDelay :: Double
defaultDelay = 0.05

defaultLosses :: Double
defaultLosses = 0.05

defaultPieceLen :: Int
defaultPieceLen = 10000

defaultFile :: FilePath
defaultFile = "pjesma.wav"
