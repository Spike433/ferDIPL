using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using static MathUtils;

namespace Tests
{
    public class MathUtilsTest
    {
        [UnityTest]
        public IEnumerator LineNoIntersectionWithCircleAtCenter()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 7;
            Vector2 p1 = new Vector2(-2f, 7.001f);
            Vector2 p2 = new Vector2(3f, 7.001f);
            Assert.IsFalse(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineNoIntersectionWithCircleAtCenter2()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 9;
            Vector2 p1 = new Vector2(10f, 0f);
            Vector2 p2 = new Vector2(20f, 0f);
            Assert.IsFalse(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIsTangentOfCircleAtCenter()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 3;
            Vector2 p1 = new Vector2(-2f, -3f);
            Vector2 p2 = new Vector2(3f, -3f);
            Assert.IsFalse(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIntersectsCircleAtCenterInOnePoint()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 9;
            Vector2 p1 = new Vector2(-11.1f, -8.3f);
            Vector2 p2 = new Vector2(7.01f, -3f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIntersectsCircleAtCenterInOnePoint2()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 12;
            Vector2 p1 = new Vector2(0f, 10);
            Vector2 p2 = new Vector2(13f, -3f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIsSecantOfCircleAtCenter()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 9;
            Vector2 p1 = new Vector2(-11.2f, -8.325f);
            Vector2 p2 = new Vector2(-5f, 9.5f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIsSecantOfCircleAtCenter2()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 9;
            Vector2 p1 = new Vector2(-11.2f, -8.325f);
            Vector2 p2 = new Vector2(10.2f, 9.5f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIsSecantOfCircleAtCenter3()
        {
            yield return null;
            Vector2 _center = new Vector2(0f, 0f);
            int _radius = 9;
            Vector2 p1 = new Vector2(-11.2f, -8.325f);
            Vector2 p2 = new Vector2(10.2f, -3f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineNoIntersectionWithCircle()
        {
            yield return null;
            Vector2 _center = new Vector2(10f, 13.25f);
            int _radius = 12;
            Vector2 p1 = new Vector2(-3.25f, 3f);
            Vector2 p2 = new Vector2(13f, -3f);
            Assert.IsFalse(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIsTangentOfCircle()
        {
            yield return null;
            Vector2 _center = new Vector2(-3f, 3f);
            int _radius = 2;
            Vector2 p1 = new Vector2(1f, 1f);
            Vector2 p2 = new Vector2(-5f, 1f);
            Assert.IsFalse(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIntersectsCircleInOnePoint()
        {
            yield return null;
            Vector2 _center = new Vector2(-5.1f, -5.1f);
            int _radius = 5;
            Vector2 p1 = new Vector2(1f, 1f);
            Vector2 p2 = new Vector2(-5f, -7.25f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIntersectsCircleInOnePoint2()
        {
            yield return null;
            Vector2 _center = new Vector2(7.25f, -5f);
            int _radius = 4;
            Vector2 p1 = new Vector2(7.1f, -3.25f);
            Vector2 p2 = new Vector2(-5f, -7.25f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIsSecantOfCircle()
        {
            yield return null;
            Vector2 _center = new Vector2(7.25f, -5f);
            int _radius = 4;
            Vector2 p1 = new Vector2(13.1f, -3.25f);
            Vector2 p2 = new Vector2(-5f, -7.25f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

        [UnityTest]
        public IEnumerator LineIsSecantOfCircle2()
        {
            yield return null;
            Vector2 _center = new Vector2(-12.5f, 7.9f);
            int _radius = 5;
            Vector2 p1 = new Vector2(-10f, 13f);
            Vector2 p2 = new Vector2(-5f, -7.25f);
            Assert.IsTrue(IsLineIntersectingCircle(p1, p2, _center, _radius));
        }

    }
}
