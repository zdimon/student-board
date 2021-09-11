class Animal {
    size = 150;
    constructor(canJumpObj){
        this.canJump = canJumpObj; 
    }
   
    show() {
        const tpl = `
        <div>
             <img src="${this.image}" width="${this.size}" />
             <p>
                <button id="v-button-${this.name}">Voice</button>
                <button id="m-button-${this.name}">Move</button>
                <button id="j-button-${this.name}">Jump</button>
             </p>
        </div>
        `
        $("#root").append(tpl);
        $('#m-button-'+this.name).on('click',this.move);
        $('#v-button-'+this.name).on('click',()=> {this.voice()});
        $('#j-button-'+this.name).on('click',()=> {this.jump()});
    };
    move() {
        console.log('I am mooving');
    };

    jump() {
        this.canJump.jump();
    };

}


class Dog extends Animal {

    constructor(name,image,canJumpObj) {
        super(canJumpObj);
        this.name = name;
        this.image = image;
    }

    voice() {
        console.log(this);
        console.log(`gav gav my name is ${this.name}`);
    }
}

class Cat extends Animal {

    constructor(name,image,canJumpObj) {
        super(canJumpObj);
        this.name = name;
        this.image = image;
    }

    voice() {
        console.log(this);
        console.log(`miau miau my name is ${this.name}`);
    }
}

class WoodenCat extends Animal {

    constructor(name,image,canJumpObj) {
        super(canJumpObj);
        this.name = name;
        this.image = image;
    }

    voice() {
        console.log(`I am a wooden cat miau miau my name is ${this.name}`);
    }

}

class CanJump {
    jump() {
        console.log(`Jump Jump!`);
    }
}

class CanNotJump {
    jump() {
        console.log(`I can not jump!`);
    }
}




var dogObj = new Dog('Bobik','bobik.png',new CanJump());
dogObj.show();

var catObj = new Cat('Murka','murka.png',new CanJump());
catObj.show();

var catMaket = new WoodenCat('WoodMurka','catwood.png',new CanNotJump());
catMaket.canJump = new CanJump();
catMaket.show();




