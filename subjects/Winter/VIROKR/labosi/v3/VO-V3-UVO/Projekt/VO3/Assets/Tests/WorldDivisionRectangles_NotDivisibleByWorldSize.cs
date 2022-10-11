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

    public class WorldDivisionRectangles_NotDivisibleByWorldSize
    {
        WorldDivision worldDivider;
        Vector2Int cellDimension;
        Dictionary<int, WorldDivision.Cell> cells;

        // Set up world divider
        public WorldDivisionRectangles_NotDivisibleByWorldSize()
        {
            Vector2Int _terrainDimension = new Vector2Int(4100, 6025);
            cellDimension = new Vector2Int(2000, 3000);

            var gameObject = new GameObject();
            worldDivider = gameObject.AddComponent<WorldDivision>();

            worldDivider.Construct(_terrainDimension, cellDimension);
            cells = worldDivider.Cells;
        }

        #region Testing Number of Cells
        [UnityTest]
        public IEnumerator TestNumberOfCells()
        {
            yield return null;
            Assert.AreEqual(9, worldDivider.Cells.Count);
        }
        #endregion

        #region Testing cells dimension
        [UnityTest]
        public IEnumerator TestRectangleCells_WithInitialDimension()
        {
            yield return null;
            int[] _cellsWithInitialDimension = new int[] { 1, 2, 4, 5 };
            foreach (int _id in _cellsWithInitialDimension)
            {
                Assert.AreEqual(cellDimension.x, cells[_id].Dimension.x);
                Assert.AreEqual(cellDimension.y, cells[_id].Dimension.y);
            }
        }

        [UnityTest]
        public IEnumerator TestCellDimension_Zone3()
        {
            yield return null;
            Assert.AreEqual(100, cells[3].Dimension.x);
            Assert.AreEqual(cellDimension.y, cells[3].Dimension.y);
        }

        [UnityTest]
        public IEnumerator TestCellDimension_Zone6()
        {
            yield return null;
            Assert.AreEqual(100, cells[6].Dimension.x);
            Assert.AreEqual(cellDimension.y, cells[6].Dimension.y);
        }

        [UnityTest]
        public IEnumerator TestCellDimension_Zone7()
        {
            yield return null;
            Assert.AreEqual(cellDimension.x, cells[7].Dimension.x);
            Assert.AreEqual(25, cells[7].Dimension.y);
        }

        [UnityTest]
        public IEnumerator TestCellDimension_Zone8()
        {
            yield return null;
            Assert.AreEqual(cellDimension.x, cells[8].Dimension.x);
            Assert.AreEqual(25, cells[8].Dimension.y);
        }

        [UnityTest]
        public IEnumerator TestCellDimension_Zone9()
        {
            yield return null;
            Assert.AreEqual(100, cells[9].Dimension.x);
            Assert.AreEqual(25, cells[9].Dimension.y);
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
            TestCellStartPosition(2, 2000, 0);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone3()
        {
            yield return null;
            TestCellStartPosition(3, 4000, 0);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone4()
        {
            yield return null;
            TestCellStartPosition(4, 0, 3000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone5()
        {
            yield return null;
            TestCellStartPosition(5, 2000, 3000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone6()
        {
            yield return null;
            TestCellStartPosition(6, 4000, 3000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone7()
        {
            yield return null;
            TestCellStartPosition(7, 0, 6000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone8()
        {
            yield return null;
            TestCellStartPosition(8, 2000, 6000);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone9()
        {
            yield return null;
            TestCellStartPosition(9, 4000, 6000);
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
        public IEnumerator FindMyZone_PlayerInZone1()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0, 0, 0);
            Assert.AreEqual(1, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZone2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2999, 0, 2100);
            Assert.AreEqual(2, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZone3()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0, 0, 4100);
            Assert.AreEqual(3, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZone5()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(5999, 0, 2001);
            Assert.AreEqual(5, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZone6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(5999, 0, 4001);
            Assert.AreEqual(6, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZone7()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6025, 0, 1999);
            Assert.AreEqual(7, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZone8()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6001, 0, 2001);
            Assert.AreEqual(8, worldDivider.FindMyZone(_playerTransform).Id);
        }


        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZone9()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6025, 0, 4100);
            Assert.AreEqual(9, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZoneBorder_1_2_4_5()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(3000, 0, 2000);
            Assert.AreEqual(5, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZoneBorder_2_3_5_6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(3000, 0, 4000);
            Assert.AreEqual(6, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZoneBorder_7_8()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6025, 0, 2000);
            Assert.AreEqual(8, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZone_PlayerInZoneBorder_5_6_8_9()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6000, 0, 4000);
            Assert.AreEqual(9, worldDivider.FindMyZone(_playerTransform).Id);
        }
        #endregion

        #region Test for Adjacent Zones
        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0f, 0f, 0f);
            int _playerAOIM = 1999;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NoNeighbours_part2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0f, 0f, 0f);
            int _playerAOIM = 2000;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NeighbourWith_2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(1000f, 0f, 1600f);
            int _playerAOIM = 600;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(1, neighbours.Count);
            Assert.AreEqual(2, neighbours.ElementAt(0).Id);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NeighbourWith_2_4_5()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2999f, 0f, 1999f);
            int _playerAOIM = 200;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(3, neighbours.Count);

            var actual = neighbours.Select(c => c.Id).ToList();
            var expected = new List<int> { 2, 4, 5 };
            CollectionAssert.AreEqual(expected, actual);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone3_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(1000f, 0f, 4100f);
            int _playerAOIM = 99;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone5_NeighbourWith_4_6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(4500f, 0f, 3000f);
            int _playerAOIM = 1001;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(2, neighbours.Count);

            var actual = neighbours.Select(c => c.Id).ToList();
            var expected = new List<int> { 4, 6 };
            CollectionAssert.AreEqual(expected, actual);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone8_NeighbourWith_9()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6025f, 0f, 3990f);
            int _playerAOIM = 11;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(1, neighbours.Count);
            Assert.AreEqual(9, neighbours.First.Value.Id);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone9_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6025f, 0f, 4100f);
            int _playerAOIM = 24;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone9_NeighbourWith_6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(6001f, 0f, 4100f);
            int _playerAOIM = 10;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(1, neighbours.Count);
            Assert.AreEqual(6, neighbours.First.Value.Id);
        }
        #endregion
    }
}
