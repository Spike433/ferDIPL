function randomIntFromInterval(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
  }

  function changeVel(direction){
    

    switch(direction){
        case "u":
            dy*=-1*Math.abs(n);  
            break;          
        case "d":
            dy*=-1*Math.abs(n);
            break;
        case "l":
            dx*=-1*Math.abs(n);
            break;
        case "r":
            dx*=-1*Math.abs(n);
            break;
        default:
            console.log("wrong input");
            break;
    }
}

  
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
// var x = 500//randomIntFromInterval(50,850);
// var y = 500//randomIntFromInterval(50,800);
// var dx = 0;//randomIntFromInterval(-1,1);
// var dy = 1;//randomIntFromInterval(-1,1); 

class Rect{
    constructor(dx,dy, show){
        this.x = randomIntFromInterval(50,850);
        this.y = randomIntFromInterval(50,850);
        this.dx = dx;
        this.dy = dy;
        this.show = show;
    }

}
var made = 0;
var destroyed = 0;
var r1 = new Rect(0,1,1);
var r2 = new Rect(0,1,randomIntFromInterval(0,1));
var r3 = new Rect(0,1,randomIntFromInterval(0,1));

var pct=0.00;
var fps = 60;

const list = [];
list.push(r1);
list.push(r2);



function drawRectangle(x,y) {
    ctx.font = "30px Arial";
    ctx.fillStyle = "red";
    ctx.fillText("Made "+made+" Destroyed "+destroyed , 600, 50); 
    ctx.fillStyle = 'red';
    ctx.fillRect(x, y, 100, 100);
    ctx.fill();    
}
draw1();
function draw1() {
    setTimeout(() => {
        list.forEach(element => {
            rectCalc(element.x,element.y,element.dx,element.dy, element);
        });        
    }, 1000 / fps);
}

function rectCalc(x,y,dx,dy, obj){
  
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let n = 2;//randomIntFromInterval(1,5)
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

    console.log("x = "+x+"| dx = "+dx)
    console.log("y = "+y+"| dy = "+dy)
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
    obj.dx=dx;
    obj.dy=dy;
    obj.x=x;
    obj.y=y;
    if(pct<1.00){requestAnimationFrame(draw1)};
}
