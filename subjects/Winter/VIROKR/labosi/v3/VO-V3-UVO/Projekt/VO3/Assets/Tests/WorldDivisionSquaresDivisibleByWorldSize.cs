using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using System.Linq;
using System.Collections.Generic;
using System;
using UnityScript.Lang;

namespace Tests
{

    public class WorldDivisionSquaresDivisibleByWorldSize
    {
        WorldDivision worldDivider;
        Vector2Int cellDimension;
        Dictionary<int, WorldDivision.Cell> cells;

        // Set up world divider
        public WorldDivisionSquaresDivisibleByWorldSize()
        {
            Vector2Int _terrainDimension = new Vector2Int(4000, 4000);
            cellDimension = new Vector2Int(1000, 1000);

            var gameObject = new GameObject();
            worldDivider = gameObject.AddComponent<WorldDivision>();

            worldDivider.Construct(_terrainDimension, cellDimension);
        }

        #region Testing Number of Cells
        [UnityTest]
        public IEnumerator TestNumberOfCells()
        {
            yield return null;
            Assert.AreEqual(16, worldDivider.Cells.Count);
        }
        #endregion

        #region Testing cells dimension
        [UnityTest]
        public IEnumerator TestCellsDimension()
        {
            yield return null;
            worldDivider.Cells.Values.ToList().ForEach(c =>
            {
                Assert.AreEqual(cellDimension.x, c.Dimension.x);
                Assert.AreEqual(cellDimension.y, c.Dimension.y);
            });
        }
        #endregion

        #region Testing Cells Start Position
        [UnityTest]
        public IEnumerator TestCellStartPositionZone1()
        {
            yield return null;
            TestCellStartPosition(1, 0, 0);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone2()
        {
            yield return null;
            TestCellStartPosition(2, 1000, 0);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone3()
        {
            yield return null;
            TestCellStartPosition(3, 2000, 0);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone4()
        {
            yield return null;
            TestCellStartPosition(4, 3000, 0);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone5()
        {
            yield return null;
            TestCellStartPosition(5, 0, 1000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone6()
        {
            yield return null;
            TestCellStartPosition(6, 1000, 1000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone7()
        {
            yield return null;
            TestCellStartPosition(7, 2000, 1000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone8()
        {
            yield return null;
            TestCellStartPosition(8, 3000, 1000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone9()
        {
            yield return null;
            TestCellStartPosition(9, 0, 2000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone10()
        {
            yield return null;
            TestCellStartPosition(10, 1000, 2000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone11()
        {
            yield return null;
            TestCellStartPosition(11, 2000, 2000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone12()
        {
            yield return null;
            TestCellStartPosition(12, 3000, 2000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone13()
        {
            yield return null;
            TestCellStartPosition(13, 0, 3000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone14()
        {
            yield return null;
            TestCellStartPosition(14, 1000, 3000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone15()
        {
            yield return null;
            TestCellStartPosition(15, 2000, 3000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone16()
        {
            yield return null;
            TestCellStartPosition(16, 3000, 3000);
        }

        private void TestCellStartPosition(int _cellIndex, int x, int y)
        {
            if (cells == null)
            {
                cells = worldDivider.Cells;
            }
            Assert.AreEqual(x, cells[_cellIndex].StartPos.x);
            Assert.AreEqual(y, cells[_cellIndex].StartPos.y);
        }
        #endregion

        #region Test FindMyZone
        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone1()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0, 0, 0);
            Assert.AreEqual(1, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone4()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(999, 0, 4000);
            Assert.AreEqual(4, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(1330, 0, 1024);
            Assert.AreEqual(6, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone11()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2100, 0, 2019);
            Assert.AreEqual(11, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone13()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(3100, 0, 999);
            Assert.AreEqual(13, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone16()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(4000, 0, 4000);
            Assert.AreEqual(16, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZoneBorder_1_and_5()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(1000, 0, 0);
            Assert.AreEqual(5, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZoneBorder_6_7_10_11()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2000, 0, 2000);
            Assert.AreEqual(11, worldDivider.FindMyZone(_playerTransform).Id);
        }
        [UnityTest]
        public IEnumerator FindMyZonePlayerInZoneBorder_12_16()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(3000, 0, 4000);
            Assert.AreEqual(16, worldDivider.FindMyZone(_playerTransform).Id);
        }
        [UnityTest]
        public IEnumerator FindMyZonePlayerInZoneBorder_15_16()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(4000, 0, 3000);
            Assert.AreEqual(16, worldDivider.FindMyZone(_playerTransform).Id);
        }
        #endregion

        #region Test for Adjacent Zones
        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0f, 0f, 0f);
            int _playerAOIM = 999;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NoNeighbours_part2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0f, 0f, 0f);
            int _playerAOIM = 1000;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NeighbourWith_2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(200f, 0f, 500f);
            int _playerAOIM = 600;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(1, neighbours.Count);
            Assert.AreEqual(2, neighbours.ElementAt(0).Id);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NeighbourWith_2_5_6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(900f, 0f, 900f);
            int _playerAOIM = 200;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(3, neighbours.Count);

            var actual = neighbours.Select(c => c.Id).ToList();
            var expected = new List<int> { 2, 5, 6 };
            CollectionAssert.AreEqual(expected, actual);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone6_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(1500f, 0f, 1500f);
            int _playerAOIM = 500;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone7_NeighbourWith_3_4_8()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(1100f, 0f, 2900f);
            int _playerAOIM = 500;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(3, neighbours.Count);

            var actual = neighbours.Select(c => c.Id).ToList();
            var expected = new List<int> { 3, 4, 8 };
            CollectionAssert.AreEqual(expected, actual);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone10_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2300f, 0f, 1300f);
            int _playerAOIM = 300;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone10_NeighbourWith_5_6_7_9_11_13_14_15()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2500f, 0f, 1500f);
            int _playerAOIM = 800;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(8, neighbours.Count);

            var actual = neighbours.Select(c => c.Id).ToList();
            var expected = new List<int> { 5, 6, 7, 9, 11, 13, 14, 15 };
            CollectionAssert.AreEqual(expected, actual);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone16_NoNeighbours_()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(4000f, 0f, 4000f);
            int _playerAOIM = 1000;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone16_NeighbourWith_11_12_15()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(3100, 0f, 3100f);
            int _playerAOIM = 300;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(3, neighbours.Count);

            var actual = neighbours.Select(c => c.Id).ToList();
            var expected = new List<int> { 11, 12, 15 };
            CollectionAssert.AreEqual(expected, actual);
        }
        #endregion
    }
}
