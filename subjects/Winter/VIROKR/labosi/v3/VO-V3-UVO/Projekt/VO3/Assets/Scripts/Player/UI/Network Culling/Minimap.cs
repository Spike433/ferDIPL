using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;

public class Minimap : MonoBehaviour
{
    [SerializeField] Transform playerTransform;

    [Header("Minimap UI")]
    [SerializeField] GameObject miniMapPanel;
    [SerializeField] Sprite borderImage;
    [SerializeField] Sprite AOIM_Image;

    // Properties
    private WorldDivision zoneManager;
    private NetworkCulling networkCulling;

    private int AOIM_Radius;
    private float cullingFrequency;
    private float timeSinceLastUpdate;

    private Vector2 scaleRatio;
    private RectTransform AOIM_CircleRect;

    private void Awake()
    {
        zoneManager = FindObjectOfType<WorldDivision>();
        networkCulling = transform.parent.GetComponentInChildren<NetworkCulling>();
    }

    private void Start()
    {
        AOIM_Radius = networkCulling.Get_AOIM_Radius();
        cullingFrequency = networkCulling.GetCullingFrequency();

        var _panelRect = miniMapPanel.GetComponent<RectTransform>();
        StartCoroutine(InitializeZoneMap(_panelRect));
        timeSinceLastUpdate = Time.unscaledTime;
    }

    void Update()
    {
        float _currentTime = Time.unscaledTime;
        if ((_currentTime - timeSinceLastUpdate) >= cullingFrequency)
        {
            timeSinceLastUpdate = _currentTime;
            Vector3 _playerPos = playerTransform.position;

            if (AOIM_Radius != networkCulling.Get_AOIM_Radius())
            {
                AOIM_Radius = networkCulling.Get_AOIM_Radius();
                AOIM_CircleRect.sizeDelta = new Vector2(2 * AOIM_Radius / scaleRatio.x, 2 * AOIM_Radius / scaleRatio.y);
            }
            AOIM_CircleRect.localPosition = new Vector3((_playerPos.z - (float)AOIM_Radius) / scaleRatio.x, -(_playerPos.x - (float)AOIM_Radius) / scaleRatio.y, 0f);
        }
    }

    private IEnumerator InitializeZoneMap(RectTransform _parentRect)
    {
        // Just in case hierarchy or script execution order messes up
        yield return new WaitUntil(() => zoneManager.IsZoneMapCreated);

        var cells = zoneManager.Cells.Values;
        scaleRatio = new Vector2(zoneManager.terrainLength / _parentRect.rect.width,
                                          zoneManager.terrainWidth / _parentRect.rect.height);

        foreach (WorldDivision.Cell c in cells)
        {
            AddZoneToPanel(c, _parentRect, scaleRatio);
        }

        Add_AOIM_Panel(_parentRect, scaleRatio);
        AddWorldDirections(_parentRect);
    }

    private void AddWorldDirections(RectTransform parentRect)
    {
        AddDirectionText(parentRect, "N", new Vector2(0.45f, 0.9f), new Vector2(0.55f, 1f));
        AddDirectionText(parentRect, "E", new Vector2(0.9f, 0.45f), new Vector2(1f, 0.55f));
        AddDirectionText(parentRect, "S", new Vector2(0.45f, 0f), new Vector2(0.55f, 0.1f));
        AddDirectionText(parentRect, "W", new Vector2(0f, 0.45f), new Vector2(0.1f, 0.55f));
    }

    private void AddDirectionText(RectTransform parentRect, string direction, Vector2 anchorMin, Vector2 anchorMax)
    {
        // Add text to the text holder
        GameObject _textHolder = new GameObject(direction);
        Text _text = _textHolder.AddComponent<Text>();
        _textHolder.transform.SetParent(parentRect.transform, false);

        RectTransform _textRect = _text.GetComponent<RectTransform>();
        // Center in parent
        // Set text holder anchors relative to parent      
        _textRect.anchorMin = anchorMin;
        _textRect.anchorMax = anchorMax;
        _textRect.pivot = new Vector2(0.5f, 0.5f);
        _textRect.localScale = new Vector3(1f, 1f, 1f);
        _textRect.sizeDelta = parentRect.GetComponent<RectTransform>().sizeDelta;
        _textRect.anchoredPosition = new Vector2(0f, 0f);

        // Text propeties
        _text.font = Font.CreateDynamicFontFromOSFont("Arial", 8);
        _text.fontStyle = FontStyle.Bold;
        _text.color = Color.yellow;
        _text.fontSize = 30;
        _text.alignment = TextAnchor.MiddleCenter;
        _text.text = direction;
    }

    private void AddZoneToPanel(WorldDivision.Cell _zone, RectTransform _parentRect, Vector2 _scaleRatio)
    {
        GameObject _panelChild = AddChildPanel(_parentRect, _zone, _scaleRatio);
        AddText(_panelChild, _parentRect, _zone);
    }

    private GameObject AddChildPanel(RectTransform _parentRect, WorldDivision.Cell _zone, Vector2 _scaleRatio)
    {
        GameObject _panelChild = new GameObject($"Zone Panel: {_zone.Id}");
        // Set it as a child of mini map panel
        RectTransform _panelChildRect = _panelChild.AddComponent<RectTransform>();
        _panelChild.AddComponent<CanvasRenderer>();
        _panelChild.AddComponent<Image>().sprite = borderImage;
        _panelChild.transform.SetParent(miniMapPanel.transform, false);


        // Add & configure text holder rect transform
        _panelChildRect.localScale = new Vector3(1f, 1f, 1f);
        // Set text holder anchors relative to parent
        _panelChildRect.anchoredPosition = _parentRect.anchoredPosition;
        Vector2 _panelTopLeftCorner = new Vector2(0f, 1f);
        _panelChildRect.anchorMin = _panelTopLeftCorner;
        _panelChildRect.anchorMax = _panelTopLeftCorner;
        _panelChildRect.pivot = _panelTopLeftCorner;

        // Set text holder scaled dimension
        _panelChildRect.sizeDelta = new Vector2(_zone.Dimension.x / _scaleRatio.x,
                                                        _zone.Dimension.y / _scaleRatio.y);
        // Set text holder position (Invert y-axis because parent anchor is at the bottom-right)
        _panelChildRect.localPosition = new Vector3(_zone.StartPos.x / _scaleRatio.x,
                                                            -_zone.StartPos.y / _scaleRatio.y,
                                                            0f);

        return _panelChild;
    }

    private static void AddText(GameObject _childPanel, RectTransform _parentRect, WorldDivision.Cell _zone)
    {
        // Add text to the text holder
        GameObject _textHolder = new GameObject($"Zone Text: {_zone.Id}");
        Text _text = _textHolder.AddComponent<Text>();
        _textHolder.transform.SetParent(_childPanel.transform, false);

        RectTransform _textRect = _text.GetComponent<RectTransform>();
        // Center in parent
        // Set text holder anchors relative to parent
        _textRect.anchoredPosition = _parentRect.anchoredPosition;
        Vector2 _panelTopLeftCorner = new Vector2(0f, 1f);
        _textRect.anchorMin = _panelTopLeftCorner;
        _textRect.anchorMax = _panelTopLeftCorner;
        _textRect.pivot = _panelTopLeftCorner;
        _textRect.localScale = _childPanel.GetComponent<RectTransform>().localScale;
        _textRect.sizeDelta = _childPanel.GetComponent<RectTransform>().sizeDelta;
        _textRect.position = _childPanel.GetComponent<RectTransform>().position;

        // Text propeties
        _text.font = Font.CreateDynamicFontFromOSFont("Arial", 10);
        _text.fontStyle = FontStyle.Bold;
        _text.color = Color.white;
        _text.fontSize = 30;
        _text.alignment = TextAnchor.MiddleCenter;
        _text.text = _zone.Id.ToString();
    }

    private void Add_AOIM_Panel(RectTransform _parentRect, Vector2 _scaleRatio)
    {
        GameObject AOIM_Circle = new GameObject($"AOIM Panel");

        // Set it as a child of mini map panel
        AOIM_CircleRect = AOIM_Circle.AddComponent<RectTransform>();
        AOIM_Circle.AddComponent<CanvasRenderer>();
        AOIM_Circle.AddComponent<Image>().sprite = AOIM_Image;
        AOIM_Circle.transform.SetParent(miniMapPanel.transform, false);

        // Add & configure text holder rect transform
        AOIM_CircleRect.localScale = new Vector3(1f, 1f, 1f);
        // Set text holder anchors relative to parent
        AOIM_CircleRect.anchoredPosition = _parentRect.anchoredPosition;
        Vector2 _panelTopLeftCorner = new Vector2(0f, 1f);
        AOIM_CircleRect.anchorMin = _panelTopLeftCorner;
        AOIM_CircleRect.anchorMax = _panelTopLeftCorner;
        AOIM_CircleRect.pivot = _panelTopLeftCorner;

        AOIM_CircleRect.sizeDelta = new Vector2(2 * AOIM_Radius / _scaleRatio.x, 2 * AOIM_Radius / _scaleRatio.y);
        // Set text holder position (Invert y-axis because parent anchor is at the bottom-right)
        AOIM_CircleRect.localPosition = new Vector3((transform.position.z - (float)AOIM_Radius) / scaleRatio.x, -(transform.position.x - (float)AOIM_Radius) / scaleRatio.y, 0f);
    }

}
