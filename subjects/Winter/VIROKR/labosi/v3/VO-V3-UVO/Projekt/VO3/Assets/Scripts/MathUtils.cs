using UnityEngine;

public static class MathUtils
{
    public static bool IsLineIntersectingCircle(Vector2 p1, Vector2 p2, Vector2 _center, int _radius)
    {
        // Move center of circle to (0, 0) to get easier equation
        p1 = new Vector2(p1.x - _center.x, p1.y - _center.y);
        p2 = new Vector2(p2.x - _center.x, p2.y - _center.y);

        float dx = p2.x - p1.x;
        float dy = p2.y - p1.y;

        float A = Mathf.Pow(dx, 2) + Mathf.Pow(dy, 2);
        float B = 2 * (p1.x * dx + p1.y * dy);
        float C = Mathf.Pow(p1.x, 2) + Mathf.Pow(p1.y, 2) - Mathf.Pow(_radius, 2);

        float D = Mathf.Pow(B, 2) - 4 * A * C;

        if (D <= 0)
        {
            return false;
        }

        float sqrtD = Mathf.Sqrt(D);
        float t1 = (-B + sqrtD) / (2 * A);
        float t2 = (-B - sqrtD) / (2 * A);

        if ((t1 > 0 && t1 < 1) || (t2 > 0 && t2 < 1))
        {
            return true;
        }
        return false;
    }
}

