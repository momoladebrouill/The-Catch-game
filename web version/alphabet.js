let canvas = document.getElementById("game");
let context = canvas.getContext("2d"),
			W = window.innerWidth,
			H = window.innerHeight,
ratio = window.devicePixelRatio;
canvas.width = W*ratio;
canvas.height = H*ratio;
canvas.style.width = W + "px";
canvas.style.height = H + "px";
context.scale(ratio,ratio);
const tau=2*Math.PI
let score=30
let level=0
let angle=0
let fakeangle=0
let count=0
const speed=1
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
	angle=angle%tau
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
		
		if(this.val!=this.landedon()){
			context.beginPath();
			context.fillStyle="white";
			context.arc(this.x,this.y,11,0,tau);
			context.fill();
			context.closePath();
		}
		context.beginPath();
		context.fillStyle="hsl("+this.val*360+",50%,50%)";
		context.arc(this.x,this.y,10,0,tau);
		context.fill();
		context.closePath();
	}
	move(){
		this.x+=this.dir[0]*speed;
		this.y+=this.dir[1]*speed;
	}
	landedon(){
		let ang=this.attack-angle-Math.PI
		ang=Math.abs(ang)%tau
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
	let nextarmada=[]
	for (let i = 0; i <=armada.length-1; i++) {
		armada[i].val=armada[i].landedon()
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
	/*if(parseInt(score/10)+2!=level){
		armada=[]
		level=parseInt(score/10)+2
	}*/
	fakeangle=angle
	for (let i = 0; i < level; i++) {
		context.beginPath()
		context.moveTo(W/2,H/2)
		context.fillStyle="hsl("+i/level*360+",50%,50%)"
		context.arc(W/2,H/2,100,i/level*tau+fakeangle,(i+1)/level*tau+fakeangle);
		context.fill()
		let k=(i+0.5)/level*tau+fakeangle
		//context.fillText(i/level,W/2+Math.cos(k)*150,H/2+Math.sin(k)*150)
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
