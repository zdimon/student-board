## Нахождение общего делителя.

Создаем поток

    import { range } from 'rxjs';

    const CONST1 = 20;

    const stream1 = range(1,CONST1);

Преобразуем в массив и сортируем.

    ...
    import { toArray, map } from 'rxjs/operators';

    stream1
    .pipe(toArray(),map(arr=>arr.sort((a,b) => b-a)))
    .subscribe((el) => {
        console.log(el);
    })

Переключаемся на второй поток из масива и выбираем из него все что делится без остатка.

    stream1
    .pipe(
        toArray(),
        map(arr=>arr.sort((a,b) => b-a)),
        switchMap( (rez) => from(rez)
                            .pipe(filter((el: any) => CONST1%el === 0))
        )
    )
    .subscribe((el) => {
        console.log(el);
    })

Оформляем 2 потока.


    const CONST1 = 20;
    const CONST2 = 50;

    const stream1 = range(1,CONST1)
    .pipe(
        toArray(),
        map(arr=>arr.sort((a,b) => b-a)),
        switchMap( (rez) => from(rez)
                            .pipe(filter((el: any) => CONST1%el === 0))
        )
    );

    const stream2 = range(1,CONST2)
    .pipe(
        toArray(),
        map(arr=>arr.sort((a,b) => b-a)),
        switchMap( (rez) => from(rez)
                            .pipe(filter((el: any) => CONST2%el === 0))
        )
    );


    stream1.subscribe((el) => {
        console.log(`stream1 = ${el}`);
    })

    stream2.subscribe((el) => {
        console.log(`stream2 = ${el}`);
    })

Создаем 3 поток где выбираем совпадающие элементы, переключаясь на второй поток, переводим их в массив и получаем наибольшее.

    const stream3 = stream1.pipe(
        switchMap((el1) => stream2.pipe(filter((el2) => el2 === el1))),
        toArray()
    ).subscribe((el) => {
        console.log(Math.max(...el));
    })

Полный код примера.

    import { from } from 'rxjs';
    import { range } from 'rxjs';
    import { toArray, map, switchMap, filter } from 'rxjs/operators';

    const CONST1 = 20;
    const CONST2 = 50;

    const stream1 = range(1,CONST1)
    .pipe(
        toArray(),
        map(arr=>arr.sort((a,b) => b-a)),
        switchMap( (rez) => from(rez)
                            .pipe(filter((el: any) => CONST1%el === 0))
        )
    );

    const stream2 = range(1,CONST2)
    .pipe(
        toArray(),
        map(arr=>arr.sort((a,b) => b-a)),
        switchMap( (rez) => from(rez)
                            .pipe(filter((el: any) => CONST2%el === 0))
        )
    );

    const stream3 = stream1.pipe(
        switchMap((el1) => stream2.pipe(filter((el2) => el2 === el1))),
        toArray()
    ).subscribe((el) => {
        console.log(Math.max(...el));
    })





