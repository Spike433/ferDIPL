{-# LANGUAGE OverloadedStrings #-}

module Main where

import Prelude                 hiding (splitAt, readFile)
import System.Timeout          (timeout)
import System.Environment      (getArgs)
import Network.Socket.Internal (SockAddr)

import Helper                  (seconds, chunks, usingMVar)
import Configuration           (defaultPort, defaultFile)
import SimulatedSocket         (listen, send, receive, withNet)

import Data.Map                (Map, empty, insert, (!), delete, member, elems)
import Data.ByteString         (readFile, append, ByteString)
import Data.ByteString.Char8   (unpack, snoc, pack)
import qualified Data.IntSet   as IS (fromList, delete, elems, null, size)

import Control.Monad           (forM_, void, when)
import Control.Concurrent      (forkIO)
import Control.Concurrent.MVar (newEmptyMVar)
import Control.Concurrent.Chan (newChan, writeChan, Chan, readChan)

main :: IO ()
main = withNet $ do
  sock <- listen defaultPort
  let get = receive sock
  let put = send sock
  putStrLn "Server listening."
  serve get put empty

serve :: IO (ByteString, SockAddr) -> (SockAddr -> ByteString -> IO ())
         -> Map SockAddr (Chan (Maybe Int)) -> IO ()
serve get put clients = do
  (message, client) <- get
  case message of
    "FEEDME" -> do
      if client `member` clients
         then serve get put clients
         else do
           chan <- newChan
           putStrLn $ "Greetings from " ++ show client ++ "."
           forkIO . handle chan $ put client
           serve get put $ insert client chan clients

    "OKIDOK" -> do
      if client `member` clients then do
        putStrLn $ "Goodbye from " ++ show client ++ "."
        writeChan (clients ! client) Nothing
        serve get put $ delete client clients
      else do
        serve get put clients

    "DIEDIE" -> do
      putStrLn $ "Told to quit by " ++ show client ++ "."
      forM_ (elems clients) $ \chan ->
        writeChan chan Nothing

    _ -> do
      when (client `member` clients) $
        writeChan (clients ! client) . Just . read $ unpack message
      serve get put clients

handle :: Chan (Maybe Int) -> (ByteString -> IO ()) -> IO ()
handle chan put = do
  putStrLn "Reading and sending entire file."
  file <- (head.(++[defaultFile])) `fmap` getArgs
  packets <- chunks `fmap` readFile file
  sending <- newEmptyMVar
  handle' chan put packets sending $ IS.fromList [1 .. length packets]

handle' chan put packets sending = loop where
  loop unsent
    | IS.null unsent = sequence_ . replicate 10 $ put "OKIDOK"
    | otherwise = do
       message <- timeout (seconds 0.05) $ readChan chan
       case message of
         Just (Just i) -> loop $ IS.delete i unsent
         Just Nothing  -> putStrLn "Client handler closed."
         Nothing -> do
           void . forkIO . usingMVar sending $ do
             putStrLn $ "Sending " ++ show (IS.size unsent) ++ " packets."
             forM_ (IS.elems unsent) $ \i ->
               put $ tagpacket (i, packets !! (i-1))
           loop unsent

tagpacket :: (Int, ByteString) -> ByteString
tagpacket (i, str) = prefix `append` str
   where prefix = snoc (pack $ show i) '/'
