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
let score=0
let level=2
var angle=0
var fakeangle=0
var count=0
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
	}else if(v==27){
		angle=0
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
	}
	draw(){
		this.move()
		context.beginPath();
		context.fillStyle="hsl("+this.val*360+",50%,50%)";
		context.arc(this.x,this.y,10,0,tau);
		context.fill();
		context.closePath();
		if(this.val!=this.landedon()){
			context.fillText(this.landedon(),this.x,this.y)}
	}
	move(){
		this.x+=this.dir[0]/5;
		this.y+=this.dir[1]/5;
	}
	landedon(){
		let ang=Math.atan2(H/2-this.y,W/2-this.x)-Math.abs(angle%tau)
		ang+=Math.PI//pour passer de -pi pi à 0 tau
		ang=Math.abs(ang%tau)
		return parseInt(ang/tau*level)/level
	}
}

let armada=[new Missile()]
bLoop()
function distToCenter(m){
	return Math.sqrt((W/2-m.x)**2+(H/2-m.y)**2)
}
function bLoop() {
	count+=1
	if (count>100){
		count=0
		armada.push(new Missile())

	}
	context.beginPath()
	context.fillStyle = "black";
	context.fillRect(0,0,W,H);
	context.closePath()
	var nextarmada=[]
	for (var i = 0; i <=armada.length-1; i++) {
		//armada[i].val=armada[i].landedon()
		armada[i].draw()
		if (distToCenter(armada[i])>100){
			nextarmada.push(armada[i])
		}else{
			if(armada[i].landedon()==armada[i].val){
				score++
			}else{
				score--
				if(score<0){score=0}
			}
		}

	}
	armada=[...nextarmada]
	if(parseInt(score/10)+2!=level){
		armada=[]
		level=parseInt(score/10)+2
	}
	fakeangle+=(angle-fakeangle)/7
	for (var i = 0; i < level; i++) {
		context.beginPath()
		context.moveTo(W/2,H/2)
		context.fillStyle="hsl("+i/level*360+",50%,50%)"
		context.arc(W/2,H/2,100,i/level*tau+fakeangle,(i+1)/level*tau+fakeangle);
		context.fill()
		let k=(i+0.5)/level*tau+fakeangle
		context.fillText(i/level,W/2+Math.cos(k)*150,H/2+Math.sin(k)*150)
		context.closePath()
	}
	context.beginPath()
	context.fillStyle='black'
	context.arc(W/2,H/2,50,0,tau)
	context.fill()
	context.closePath()

	context.font = "50px cursive";
	context.fillStyle = "white";
	context.textBaseline = "middle"
	let size=context.measureText(score)

	
	context.fillText(score,W/2-size.width/2,size.actualBoundingBoxAscent+size.actualBoundingBoxDescent)
	requestAnimationFrame(bLoop)
	
	
}
