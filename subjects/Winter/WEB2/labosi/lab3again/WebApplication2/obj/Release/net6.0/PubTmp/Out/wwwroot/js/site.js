

window.requestAnimFrame = (function () {
    return window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.requestAnimationFrame || window.msRequestAnimationFrame ||
        function () {
            window.setTimeout(cc, 2000 / 30);
        };
})();

class Rectangle {
    constructor(speedX, speedY) {
        this.sX = speedX;
        this.sY = speedY;
        this.x = rand(400, 20);
        this.y = rand(400, 20);
        this.changeDir = 0;
        this.fowardStep = -1;
        this.Color = 'green';
    }
}

function rand(maximum, minimum) {
    return Math.floor(Math.random() * (maximum - minimum + 1) + minimum)
}

function fillRectangles() {
    for (let i = 0; i < rand(5, 1); i++) {

        let speedX = rand(2, -2);
        let speedY = rand(2, -2);

        if (speedX == 0) 
            speedX = 1;
        if (speedY == 0) 
            speedY = 1;
        
        var r = new Rectangle(speedX, speedY)
        rectangles.push(r);
    }
}

function fowardAnimation() {
    setTimeout(function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.font = "20px Consolas";
        ctx.fillStyle = "black";
        ctx.fillText("Generated: " + generated + " | Hit:" + hit, 150, 20);

        for (var i = 0; i < rectangles.length; i++) {
            var rectangle = rectangles[i];
            ctx.fillStyle = rectangle.Color;
            ctx.fillRect(rectangle.x, rectangle.y, size, size);
            ctx.fill();

            if (rectangle.x < 0 || rectangle.x > 430) {
                rectangle.sX *= -2;

                if (rectangle.x < 0) {
                    rectangle.x += 0 - rectangle.x;
                } else if (rectangle.x > 430) {
                    rectangle.x -= rectangle.x - 430;
                }
            }

            if (rectangle.y < 0 || rectangle.y > 430) {
                rectangle.sY *= -2;
                if (rectangle.y < 0) {
                    rectangle.y += 0 - rectangle.y;
                }
                else if (rectangle.y > 430) {
                    rectangle.y -= rectangle.y - 430;
                }
            }

            let maxSpeed = 3;
            let lowSpeed = -3;
            let reset = 1;
            let stop = -1;

            if (rectangle.sY > maxSpeed)
                rectangle.sY = reset;
            if (rectangle.sY < lowSpeed)
                rectangle.sY = stop; 

            if (rectangle.sX > maxSpeed) 
                rectangle.sX = reset;
            if (rectangle.sX < lowSpeed) 
                rectangle.sX = stop;           


            rectangle.x += rectangle.sX;
            rectangle.y += rectangle.sY;

        }
        if (true) { requestAnimFrame(fowardAnimation) };
    }, 2);
}

async function RectangleDEstroyer(mouseEvent) {
    let previousState = rectangles.length;
    rectangles = rectangles.filter(rectangle => 
    mouseEvent.y > rectangle.y + size || mouseEvent.y < rectangle.y ||
    mouseEvent.x > rectangle.x + size || mouseEvent.x < rectangle.x 
    );

    let dif = previousState - rectangles.length;
    if (dif>0) {
        hit = hit + dif;
    }
}

var dim2 = '2d';
var click = 'click';
var can = 'can';
var canvas = document.getElementById(can);
var ctx = canvas.getContext(dim2);

var rectangles = [];
fillRectangles();
var hit = 0;
var size = 70;
var generated = rectangles.length;

canvas.addEventListener(click, RectangleDEstroyer);
fowardAnimation();


