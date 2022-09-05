{-# LANGUAGE OverloadedStrings #-}

module Main where

import Prelude               hiding (concat, break, writeFile, tail)
import Helper                (spam, seconds, timestamp)
import Configuration         (defaultPort, defaultHost)
import SimulatedSocket       (opensock, send, receive, address, withNet)
import Data.IntMap           (empty, elems, insert, member, (!))
import Data.ByteString       (concat, ByteString)
import Data.ByteString.Char8 (unpack, writeFile, break, tail)
import System.Environment    (getArgs)
import Control.Concurrent    (threadDelay)

main :: IO ()
main = withNet $ do
  sock <- opensock defaultHost defaultPort
  host <- address  defaultHost defaultPort
  let put = send sock host
  let get = fst `fmap` receive sock

  (command:_) <- (++["get"]) `fmap` getArgs

  if command == "kill" then do
    spam $ put "DIEDIE"
    threadDelay $ seconds 0.5
  else do
    -- Notify the server by pinging N times.
    spam $ put "FEEDME"
    putStrLn "Client online. File requested."

    -- Get and write the two packet groups.
    (fifo'd, num'd) <- readPackets get put
    t <- timestamp
    writeFile ("primljeno-pobrkano-" ++ t) fifo'd
    writeFile ("primljeno-ispravno-" ++ t) num'd


readPackets :: IO ByteString                  -- Packet getter.
               -> (ByteString -> IO ())       -- Packet putter.
               -> IO (ByteString, ByteString) -- Packets by time and index.
readPackets get put = do
  (fifo'd, packets) <- loop empty []
  return (concat $ map (packets !) fifo'd, concat $ elems packets)
  where
  -- Loop, talking to the server.
  -- Get numerated packets. Tell the server you have them.
  -- Stop when an "OKIDOK" message is received.
  loop ps fifo = do
    message <- get
    if message == "OKIDOK" then do
      putStrLn "Got all packets!"
      spam $ put "OKIDOK"
      return (reverse fifo, ps)
    else do
      let (rawIndex, bytesWithSlash) = break (=='/') message
      put rawIndex -- Tell server we received this packet.

      -- Do we already have this packet?
      -- If yes, ignore. If no, store it.
      let index = read $ unpack rawIndex :: Int
      if index `member` ps
         then loop ps fifo
         else do let bytes = tail bytesWithSlash
                 loop (insert index bytes ps) $ index : fifo
