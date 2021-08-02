var canvas = document.getElementById("game");
var context = canvas.getContext("2d"),
W = window.innerWidth,
H = window.innerHeight,
ratio = window.devicePixelRatio;
canvas.width = W*ratio;
canvas.height = H*ratio;
canvas.style.width = W + "px";
canvas.style.height = H + "px";
context.scale(ratio,ratio);
var tau=2*Math.PI
document.addEventListener("keydown", keydown, false);
function keydown(e){
	v=e.keyCode
	console.log(v)
	if (v==38) {
		level++
	}else if (v==40){
		level--
	}else if (v==37){
		angle-=Math.PI/16
	}else if(v==39){
		angle+=Math.PI/16
	}else if(v==32){
		armada.push(new Missile())
	}
	//shell.textContent+=v+"\n";
	//context.fillStyle = "blue";
	//context.fillText(v,v*10,v*10);
}
class Missile{
	constructor(){
		this.attack=Math.random()*tau;
		this.x=(-Math.cos(this.attack)+1)*H/2+W/4
		this.y=(-Math.sin(this.attack)+1)*H/2
		this.dir=[Math.cos(this.attack),Math.sin(this.attack)]
		this.val=parseInt(Math.random()*level)/level
		this.coul="hsl("+this.val*360+",50%,50%)"
	}
	draw(){
		this.move()
		context.beginPath();
		context.fillStyle=this.coul;
		context.arc(this.x,this.y,10,0,tau);
		context.fill();
		context.closePath();
	}
	move(){
		this.x+=this.dir[0];
		this.y+=this.dir[1];
	}
}
var angle=0
var level=5
var armada=[new Missile()]
bLoop()
function distToCenter(m){
	return Math.sqrt((W/2-m.x)**2+(H/2-m.y)**2)
}
function bLoop() {
	context.beginPath()
	context.fillStyle = "black";
	context.fillRect(0,0,W,H);
	context.closePath()
	var nextarmada=[]
	for (var i = 0; i < armada.length; i++) {
		armada[i].draw()
		if (distToCenter(armada[i])>100){
			nextarmada.push(armada[i])
		}
	var armada=[...nextarmada]


		
	}
	for (var i = 0; i <= level; i++) {
		context.beginPath()
		context.moveTo(W/2,H/2)
		context.fillStyle="hsl("+i/level*360+",50%,50%)"
		context.arc(W/2,H/2,100,i/level*tau+angle,(i+1)/level*tau+angle);
		context.fill()
		context.closePath()

	}
	
	requestAnimationFrame(bLoop)
	
	/*
	context.font = "50px consolas";
	context.fillStyle = "blue";*/
}
