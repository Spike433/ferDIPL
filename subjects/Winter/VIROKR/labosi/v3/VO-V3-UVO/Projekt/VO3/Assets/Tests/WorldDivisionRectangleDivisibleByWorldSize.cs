using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using System.Linq;
using System.Collections.Generic;

namespace Tests
{
    public class WorldDivisionRectangleDivisibleByWorldSize
    {
        WorldDivision worldDivider;
        Vector2Int cellDimension;
        Dictionary<int, WorldDivision.Cell> cells;

        // Set up world divider
        public WorldDivisionRectangleDivisibleByWorldSize()
        {
            Vector2Int _terrainDimension = new Vector2Int(4000, 4000);
            cellDimension = new Vector2Int(2000, 800);

            var gameObject = new GameObject();
            worldDivider = gameObject.AddComponent<WorldDivision>();

            worldDivider.Construct(_terrainDimension, cellDimension);
        }

        #region Testing Number of Cells
        [UnityTest]
        public IEnumerator TestNumberOfCells()
        {
            yield return null;
            Assert.AreEqual(10, worldDivider.Cells.Count);
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
            TestCellStartPosition(2, 2000, 0);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone3()
        {
            yield return null;
            TestCellStartPosition(3, 0, 800);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone4()
        {
            yield return null;
            TestCellStartPosition(4, 2000, 800);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone5()
        {
            yield return null;
            TestCellStartPosition(5, 0, 1600);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone6()
        {
            yield return null;
            TestCellStartPosition(6, 2000, 1600);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone7()
        {
            yield return null;
            TestCellStartPosition(7, 0, 2400);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone8()
        {
            yield return null;
            TestCellStartPosition(8, 2000, 2400);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone9()
        {
            yield return null;
            TestCellStartPosition(9, 0, 3200);
        }

        [UnityTest]
        public IEnumerator TestCellStartPositionZone10()
        {
            yield return null;
            TestCellStartPosition(10, 2000, 3200);
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
            Vector3 _playerTransform = new Vector3(799f, 0, 1999f);
            Assert.AreEqual(1, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone4()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(801, 0, 2001);
            Assert.AreEqual(4, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2399, 0, 4000);
            Assert.AreEqual(6, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZone10()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(4000, 0, 4000);
            Assert.AreEqual(10, worldDivider.FindMyZone(_playerTransform).Id);
        }

        [UnityTest]
        public IEnumerator FindMyZonePlayerInZoneBorder_1_and_2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0, 0, 2000);
            Assert.AreEqual(2, worldDivider.FindMyZone(_playerTransform).Id);
        }
        [UnityTest]
        public IEnumerator FindMyZonePlayerInZoneBorder_3_4_5_6()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(1600, 0, 2000);
            Assert.AreEqual(6, worldDivider.FindMyZone(_playerTransform).Id);
        }
        [UnityTest]
        public IEnumerator FindMyZonePlayerInZoneBorder_7_9()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(3200, 0, 100);
            Assert.AreEqual(9, worldDivider.FindMyZone(_playerTransform).Id);
        }
        #endregion

        #region Test for Adjacent Zones
        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0f, 0f, 0f);
            int _playerAOIM = 799;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NoNeighbours_part2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(0f, 0f, 0f);
            int _playerAOIM = 800;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone1_NeighbourWith_2()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(199, 0f, 1500);
            int _playerAOIM = 600;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(1, neighbours.Count);
            Assert.AreEqual(2, neighbours.ElementAt(0).Id);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone6_NeighbourWith_3_4_5_7_8()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(2000f, 0f, 2000f);
            int _playerAOIM = 1000;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(5, neighbours.Count);

            var actual = neighbours.Select(c => c.Id).ToList();
            var expected = new List<int> { 3, 4, 5, 7, 8 };
            CollectionAssert.AreEqual(expected, actual);
        }

        [UnityTest]
        public IEnumerator GetNeighbours_PlayerInZone10_NoNeighbours()
        {
            yield return null;
            Vector3 _playerTransform = new Vector3(4000, 0f, 4000);
            int _playerAOIM = 800;
            LinkedList<WorldDivision.Cell> neighbours = worldDivider.GetNeighbours(_playerTransform, _playerAOIM);
            Assert.AreEqual(0, neighbours.Count);
        }
        #endregion
    }
}
