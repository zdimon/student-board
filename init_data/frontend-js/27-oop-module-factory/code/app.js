class Card {
    
    constructor(number,pin,account){
        this.number = number; 
        this.account = account;
        var _pin = pin;
        this.getPin = function() { return _pin };
    }
}

class Bankomat {
    cards = [];

    constructor(){
        this.cardFabrik();
    }

    cardFabrik(){
        const card1 = new Card('123123','1',0);
        const card2 = new Card('223123','2',1);
        const card3 = new Card('323123','3',2);
        this.cards = [card1,card2,card3];
    }

    check(cardNumber,pin) {
        let isCorrect = false;
        this.cards.forEach((el) => {
            if(cardNumber === el.number){
                if(el.getPin() === pin) {
                    isCorrect = true;
                }
            }
        })
        return isCorrect;
    }

    replanish() {
        const pin = $('#cpin').val();
        const cardNumber = $('#cnum').val();
        if(!this.check(cardNumber,pin)) {
            alert('Wrong PIN!');
        } else {
            console.log('replanish money');
        }
        
    }

    show() {
        console.log('show money');
    }

    display() {
        const tpl = `
        <div>
             <img src="bankomat.png" width="200" />
             <p>
                <select id="cnum">
                    ${this.cards.map((el) => `<option value="${el.number}">${el.number}</option>`)}
                </select>
             </p>
             <p>
                <input id="cpin" type="text" placeholder="ПИН" />
             </p>
             <p>
                <input id="csum" type="text" placeholder="Сумма" />
             </p>
             <p>
                <button id="show-button">Show balance</button>
                <button id="repl-button">Add money</button>
             </p>
        </div>
        `
        $("#root").append(tpl);
        $('#show-button').on('click',()=> {this.show()});
        $('#repl-button').on('click',()=> {this.replanish()});        
    }
}


var bankomat = new Bankomat();
bankomat.display();

bankomat.cards[0]._pin = 'fake';