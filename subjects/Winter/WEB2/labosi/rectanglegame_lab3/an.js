
//http://www.java2s.com/example/javascript/canvas/movement-multiple-objects-in-canvas-to-xy-coordinate.html

var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
window.requestAnimFrame = (function(callback) {
  return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
  function(callback) {
    window.setTimeout(callback, 1000 / 60);
  };
})();

class Rect{
    constructor(dx,dy){
        this.x = randomIntFromInterval(50,850);
        this.y = randomIntFromInterval(50,850);
        this.dx = dx;
        this.dy = dy;
    }
}

var shapes=[];
for(let c =0; c<randomIntFromInterval(5,10);c++){
    let vx = randomIntFromInterval(-1,1);    
    let vy = randomIntFromInterval(-1,1);    
    shapes.push(new Rect(vx==0?1:vx ,vy==0?-1:vy));
}

async function OnClick(e){
    console.log("clicked");
    console.log(e.x);
    console.log(e.y);
    let prev = shapes.length;
    shapes  = shapes.filter(rectangle => !
        ((e.x >= rectangle.x && e.x <= rectangle.x+100) &&
        (e.y >= rectangle.y && e.y <= rectangle.y+100)
        ));
    if(shapes.length != prev){
        destroyed++;
    }   
}


canvas.addEventListener('click',OnClick);

function randomIntFromInterval(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
  }

  function drawRectangle(x,y) {   
    ctx.fillStyle = 'red';
    ctx.fillRect(x, y, 100, 100);
    ctx.fill();    
}

var made = shapes.length;
var destroyed = 0;


//shapes.push(r2);

var fps = 60;
animate();
function animate() {
    setTimeout(function() { 
            
        ctx.clearRect(0,0,canvas.width,canvas.height);
        ctx.font = "30px Arial";
        ctx.fillStyle = "red";
        ctx.fillText("Made "+made+" Destroyed "+destroyed , 600, 50);   
        for(var i=0;i<shapes.length;i++){
            var shape=shapes[i];
            let n = 2;//randomIntFromInterval(1,5)
            let x = shape.x;
            let y = shape.y;        
            let dx = shape.dx;
            let dy = shape.dy;
            drawRectangle(x,y);
            if(x<0){
                x+=0-x;
                dx*=-1*Math.abs(n);
            }else if(x > 1000){
                x-=x-1000;        
                dx*=-1*Math.abs(n);
            }

            if(y<0){
                y+=0-y;
                dy*=-1*Math.abs(n);
            }
            if(y>1000){        
                y-=y-1000;
                dy*=-1*Math.abs(n);      
            }  

            //console.log("x = "+x+"| dx = "+dx)
            //console.log("y = "+y+"| dy = "+dy)
            x += dx;
            y += dy;

            if(dx>8){
                dx=1;
            }
            if(dx<-8){
                dx=-1;
            }
            if(dy>8){
                dy=1;
            }
            if(dy<-8){
                dy=-1;
            }
            shape.dx=dx;
            shape.dy=dy;
            shape.x=x;
            shape.y=y;            
        }
        if(true){requestAnimFrame(animate)};
    }, 1);
}

