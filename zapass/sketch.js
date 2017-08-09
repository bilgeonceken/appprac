var b = [];
var path;
var bg2;
var img;
var sik = 0;
var c;
var c1 = [];
var c2 = [];
var m;
var paperlen;
var footlen;

function gotFile(file) {
//    "use strict";
    img = createImg(file.data).hide();
    sik = 1;
    for (var i = 0; i<4; i+=2) {
        b[i] = createSprite(20, i*100+150);
        b[i].addImage(loadImage("/static/zapass/s-cir.png"));
        b[i].mouseActive = true;
        b[i+1] = createSprite(150, i*100+150);
        b[i+1].addImage(loadImage("/static/zapass/s-cir.png"));
        b[i+1].mouseActive = true;
    }

    but = createSprite(280, 60);
    but.addImage(loadImage("/static/zapass/but.png"));
    but.mouseActive = true;

}



function setup() {
    c = createCanvas(319, 565);
    c.parent('cnt');
    c.drop(gotFile);
      // frameRate(5);
}



var dmod = [0,0,0,0];
function draw() {
    if (sik === 1) {
        background(51);
        image(img, 0,0, 319, 505);

        for(var i = 0; i<b.length; i+=2){
            line(b[i].position.x,b[i].position.y,b[i+1].position.x,b[i+1].position.y);
        }

        for (var i = 0; i< dmod.length; i++) {
            if ( b[i].mouseIsOver && mouseWentDown()) {
                if (!dmod[i]) {
                    dmod[i] = 1;
                }  else {
                    dmod[i] = 0;
                }
            }

            if (dmod[i] === 1) {
                b[i].position.x = mouseX;
                b[i].position.y = mouseY;
            }
        }

        for (var i = 0; i< dmod.length; i++){

        }

        if ( but.mouseIsOver && mouseWentDown() ) {
            sik = 2;
            console.log("asd");
            c1 = [(b[0].position.x + b[1].position.x)/2, (b[0].position.y + b[1].position.y)/2 ];
            c2 = [(b[2].position.x + b[3].position.x)/2, (b[2].position.y + b[3].position.y)/2 ];

            paperlen = Math.sqrt(Math.pow((c1[0]-c2[0]),2)+Math.pow((c1[1]-c2[1]),2));

            // b.pop();
            // b.pop();
            // b.pop();

            for (var i = 1; i < 4; i++) {
                b[i].remove();
            }
        b[0].position.x = c1[0];
        b[0].position.y = c1[1];
        }
        drawSprites();

    } else if (sik === 2) {
        image(img, 0,0);
        line( c1[0],c1[1],c2[0],c2[1]);
        m = (c2[1] - c1[1])/(c2[0]-c1[0]);
//        console.log(m);
//        console.log(c1,c2);


        if ( b[0].mouseIsOver && mouseWentDown() ){
            if (!dmod[0]) {
                dmod[0] = 1;
            }else {
                dmod[0] = 0;
            }
        }

        if (dmod[0] === 1) {
            b[0].position.y = constrain(mouseY, Math.min(c1[1], c2[1]), Math.max(c1[1], c2[1]));
            b[0].position.x = ((mouseY - c1[1])/m)+c1[0];

        }
        line(b[0].position.x,b[0].position.y, 0,  (-1/m)*(0-b[0].position.x)+ b[0].position.y );
        line(b[0].position.x,b[0].position.y, 319,  (-1/m)*(319-b[0].position.x)+ b[0].position.y);


        footlen = (297/paperlen)*Math.sqrt(Math.pow((b[0].position.x-c2[0]),2)+Math.pow((b[0].position.y-c2[1]),2));
        console.log(footlen);
        textSize(24);
        text(((footlen/10).toPrecision(4))+" "+"cm", 200, 500);
        drawSprites();
    }
}
