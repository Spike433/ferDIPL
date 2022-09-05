module Helper where

import Configuration           (defaultPieceLen)

import Prelude                 hiding (splitAt, null)
import Control.Monad           (void)
import Data.Time.Clock         (getCurrentTime, utctDayTime)
import Data.ByteString.Char8   (ByteString, splitAt, null)
import Control.Concurrent      (threadDelay)
import Control.Concurrent.MVar (MVar, isEmptyMVar, putMVar, takeMVar)

-- Convert seconds to microseconds, for threadDelay input.
seconds :: Double -> Int
seconds = round . (1000000*)

-- Splits a string into pieceLen-sized chunks.
chunks :: ByteString -> [ByteString]
chunks bs  | null bs   = []
           | otherwise = packet : chunks rest
  where (packet, rest) = splitAt defaultPieceLen bs

-- Executes action only if var is empty. Holds var during execution.
usingMVar :: MVar a -> IO b -> IO ()
usingMVar var act = do
  notbusy <- isEmptyMVar var
  if notbusy then putMVar var undefined >> act >> void (takeMVar var)
             else threadDelay $ seconds 0.01

spam :: IO () -> IO ()
spam = sequence_ . replicate 10

timestamp :: IO String
timestamp = (filter (`notElem` ".s") . show . utctDayTime) `fmap` getCurrentTime
