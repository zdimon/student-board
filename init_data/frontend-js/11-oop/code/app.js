var Animal = function(){
};

Animal.prototype.move = function() {
    console.log('I am mooving')
};
Animal.prototype.size = 100
Animal.prototype.show = function() {
    $("#root").append(`<img src="${this.image}" width="${this.size}" />`);
};


var Dog = function(name,image) {
    this.name = name;
    this.image = image;
    this.voice = function() {
        console.log(`gav gav my name is ${this.name} ${this.size}`);
    }
}

Dog.prototype = Animal.prototype;

var Cat = function(name,image) {
    this.name = name;
    this.image = image;
    this.voice = function() {
        console.log(`miau miau my name is ${this.name}`);
    }
}

Cat.prototype = Animal.prototype;


var d = new Dog('Bobik','bobik.png');
d.voice();
d.show();

