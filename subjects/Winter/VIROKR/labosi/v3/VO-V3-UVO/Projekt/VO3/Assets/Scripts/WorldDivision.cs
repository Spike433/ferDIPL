using System.Collections.Generic;
using UnityEngine;
using static MathUtils;

public class WorldDivision : MonoBehaviour
{
    [SerializeField] Terrain terrain;
    [SerializeField] Vector2Int cellDimension;

    public static WorldDivision instance;
    public int terrainWidth { get; set; }
    public int terrainLength { get; set; }

    private int cellsPerLength;
    private int cellsPerWidth;

    public Dictionary<int, Cell> Cells { get; set; }
    public bool IsZoneMapCreated { get; set; }

    public struct Cell
    {
        public int Id { get; set; }
        public Vector2Int Dimension { get; set; }
        public Vector2Int StartPos { get; set; }
    }

    // Singleton
    private void Awake()
    {
        IsZoneMapCreated = false;

        if (instance != null)
        {
            Destroy(gameObject);
        }
        else
        {
            instance = this;
        }
    }

    // For unit testing in editor mode
    public void Construct(Vector2Int _terrainDimension, Vector2Int _cellDimension)
    {
        terrainLength = _terrainDimension.x;
        terrainWidth = _terrainDimension.y;
        this.cellDimension = _cellDimension;

        Cells = new Dictionary<int, Cell>();
        DivideWorld();
    }

    private void Start()
    {
        terrainWidth = (int)terrain.terrainData.size.x;
        terrainLength = (int)terrain.terrainData.size.z;

        Cells = new Dictionary<int, Cell>();
        DivideWorld();
        IsZoneMapCreated = true;
    }

    // Divides world into squares or rectangles (zones, cells)
    private void DivideWorld()
    {
        cellsPerLength = Mathf.CeilToInt((float)terrainLength / cellDimension.x);
        cellsPerWidth = Mathf.CeilToInt((float)terrainWidth / cellDimension.y);

        // Divide by terrain width
        for (int row = 0; row < cellsPerWidth; row++)
        {
            // Divide by terrain length
            for (int col = 0; col < cellsPerLength; col++)
            {
                Cell c = new Cell
                {
                    Id = 1 + row * cellsPerLength + col, // Indexing starts from 1
                    // Cell dimension may not be divisible by terrain dimensions
                    Dimension = new Vector2Int(
                        ((col == (cellsPerLength - 1)) ? terrainLength - (cellsPerLength - 1) * cellDimension.x : cellDimension.x),
                        ((row == (cellsPerWidth - 1)) ? terrainWidth - (cellsPerWidth - 1) * cellDimension.y : cellDimension.y)),
                    StartPos = new Vector2Int(col * cellDimension.x, row * cellDimension.y)

                };
                Cells.Add(c.Id, c);
            }
        }
    }

    public Cell FindMyZone(Vector3 _playerTransform)
    {
        /*
         * Maps player z-coordinate to the world length,
         * x-coordinate to the world width.
         * Everything else is treated as normal 2D coordinate system.
         */
        float _x = _playerTransform.z;
        float _y = _playerTransform.x;

        int _inRow = Mathf.FloorToInt(_y / cellDimension.y);
        int _inCol = Mathf.FloorToInt(_x / cellDimension.x);
        if (_inRow == cellsPerWidth)
        {
            _inRow--; // Player is at the bottom edge of the world
        }
        if (_inCol == cellsPerLength)
        {
            _inCol--; // Player is at the right edge of the world
        }

        /**
         * + 1 because that is the index of the first cell.
         * Photon offers 256 interest groups [0, 255].
         * Group with index 0 is not available to programmers 
         * since it is used for broadcast messages.
         * Cells ids will be directly mapped to photon groups.
         */
        int cellID = 1 + _inRow * cellsPerLength + _inCol;
        return Cells[cellID];
    }

    public LinkedList<Cell> GetNeighbours(Vector3 _playerTransform, int _playerAOIM)
    {
        LinkedList<Cell> _adjacentCells = new LinkedList<Cell>();
        Cell _myZone = FindMyZone(_playerTransform);

        /*
         * Maps player z-coordinate to the world length,
         * x-coordinate to the world width.
         * Everything else is treated as normal 2D coordinate system.
         */
        Vector2 _center = new Vector2(_playerTransform.z, _playerTransform.x);

        foreach (Cell c in Cells.Values)
        {
            if (c.Id == _myZone.Id) continue;
            // Cell Top Line
            Vector2Int a = c.StartPos;
            Vector2Int b = new Vector2Int(c.StartPos.x + c.Dimension.x, c.StartPos.y);
            if (IsLineIntersectingCircle(a, b, _center, _playerAOIM))
            {
                _adjacentCells.AddLast(c);
                continue;
            }
            // Cell Left Line
            a = c.StartPos;
            b = new Vector2Int(c.StartPos.x, c.StartPos.y + c.Dimension.y);
            if (IsLineIntersectingCircle(a, b, _center, _playerAOIM))
            {
                _adjacentCells.AddLast(c);
                continue;
            }
            // Cell Right Line
            a = new Vector2Int(c.StartPos.x + c.Dimension.x, c.StartPos.y);
            b = new Vector2Int(c.StartPos.x + c.Dimension.x, c.StartPos.y + c.Dimension.y);
            if (IsLineIntersectingCircle(a, b, _center, _playerAOIM))
            {
                _adjacentCells.AddLast(c);
                continue;
            }
            // Cell Bootom Line
            a = new Vector2Int(c.StartPos.x, c.StartPos.y + c.Dimension.y);
            b = new Vector2Int(c.StartPos.x + c.Dimension.x, c.StartPos.y + c.Dimension.y);
            if (IsLineIntersectingCircle(a, b, _center, _playerAOIM))
            {
                _adjacentCells.AddLast(c);
                continue;
            }
        }

        return _adjacentCells;
    }
}
