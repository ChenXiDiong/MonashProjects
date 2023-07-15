/**
 * Name: Chen Xi Diong
 * Student ID: 32722656
 * Email: cdio0004@student.monash.edu
 * 
 * S2 2022 FIT2102 Assignment 1
 */


 import "./style.css";
 import { fromEvent, interval, merge} from 'rxjs'; 
 import { map, filter, scan} from 'rxjs/operators';
 
 type Key = 'w' | 'a' | 's' | 'd' | 'r'
 type Event = 'keydown' | 'keyup'
 
 function main() {
   /**
    * Inside this function you will use the classes and functions from rx.js
    * to add visuals to the svg element in pong.html, animate them, and make them interactive.
    *
    * Study and complete the tasks in observable examples first to get ideas.
    *
    * Course Notes showing Asteroids in FRP: https://tgdwyer.github.io/asteroids/
    *
    * You will be marked on your functional programming style
    * as well as the functionality that you implement.
    *
    * Document your code!
    */
 
   const CONSTANTS = {
     CANVAS_SIZE: 600,
     START_TIME: 0,
     START_SCORE: 0,
     START_LIVES: 5,
     HISCORE: 0,
     START_LEVEL: 1,
     LEVEL2: 2,
     //display for gameover/gameclear text
     DISPLAY_X: 0,
     DISPLAY_Y: 200,
     DISPLAY_HEIGHT: 150,
     DISPLAY_WIDTH: 600,
     //movement of the frog
     MOVE_X: 25,
     MOVE_Y: 30,
     //goal
     GOAL1_X: 90,
     GOAL1_Y: 215,
     GOAL2_X: 190,
     GOAL2_Y: 215,
     GOAL3_X: 290,
     GOAL3_Y: 215,
     GOAL4_X: 390,
     GOAL4_Y: 215,
     GOAL5_X: 490,
     GOAL5_Y: 215,
     //frog
     FROG_HEIGHT: 25,
     FROG_WIDTH: 25,
     FROG_SPAWN_X: 300,
     FROG_SPAWN_Y: 575,
     FROG_VEL: 0,
     //femaLe frog
     FEMALE_FROG_SPAWN_X: 200,
     FEMALE_FROG_SPAWN_Y: 575,
     //car1
     START_CAR1_COUNT: 3,
     CAR1_HEIGHT: 25,
     CAR1_WIDTH: 25,
     CAR1_SPAWN_X: 200,
     CAR1_SPAWN_Y: 545,
     CAR1_VEL: -5,
     CAR1_INTERVAL: 150,
     //car2
     START_CAR2_COUNT: 3,
     CAR2_HEIGHT: 25,
     CAR2_WIDTH: 25,
     CAR2_SPAWN_X: 300,
     CAR2_SPAWN_Y: 515,
     CAR2_VEL: 5,
     CAR2_INTERVAL: 125,
     //car3
     START_CAR3_COUNT: 3,
     CAR3_HEIGHT: 25,
     CAR3_WIDTH: 25,
     CAR3_SPAWN_X: 175,
     CAR3_SPAWN_Y: 485,
     CAR3_VEL: -5,
     CAR3_INTERVAL: 150,
     //racecar
     START_RACECAR_COUNT: 1,
     LEVEL2_RACECAR_COUNT: 2,
     RACECAR_HEIGHT: 25,
     RACECAR_WIDTH: 35,
     RACECAR_SPAWN_X: 0,
     RACECAR_SPAWN_Y: 455,
     RACECAR_VEL: 5,
     LEVEL2_RACECAR_VEL: 15,
     RACECAR_INTERVAL: 100,
     //truck
     START_TRUCK_COUNT: 2,
     TRUCK_HEIGHT: 25,
     TRUCK_WIDTH: 70,
     TRUCK_SPAWN_X: 290,
     TRUCK_SPAWN_Y: 425,
     TRUCK_INTERVAL: 200,
     TRUCK_VEL: -7,
     //log1
     START_LOG1_COUNT: 3,
     LOG1_HEIGHT: 25,
     LOG1_WIDTH: 100,
     LOG1_SPAWN_X: 100,
     LOG1_SPAWN_Y: 335,
     LOG1_INTERVAL: 200,
     LOG1_VEL: 5,
     //log2
     START_LOG2_COUNT: 2,
     LOG2_HEIGHT: 25,
     LOG2_WIDTH: 200,
     LOG2_SPAWN_X: 100,
     LOG2_SPAWN_Y: 305,
     LOG2_INTERVAL: 300,
     LOG2_VEL: 10,
     //log3
     START_LOG3_COUNT: 3,
     LEVEL2_LOG3_COUNT: 2,
     LOG3_HEIGHT: 25,
     LOG3_WIDTH: 125,
     LOG3_SPAWN_X: 20,
     LEVEL2_LOG3_SPAWN_X: 220,
     LOG3_SPAWN_Y: 245,
     LOG3_INTERVAL: 200,
     LOG3_VEL: 5,
     //turtle1
     START_TURTLE1_COUNT: 4,
     TURTLE1_HEIGHT: 25,
     TURTLE1_WIDTH: 100,
     TURTLE1_SPAWN_X: 0,
     TURTLE1_SPAWN_Y: 365,
     TURTLE1_INTERVAL: 170,
     TURTLE1_VEL: -7,
     LEVEL2_TURTLE1_VEL: 7,
     //turtle2
     START_TURTLE2_COUNT: 4,
     TURTLE2_HEIGHT: 25,
     TURTLE2_WIDTH: 80,
     TURTLE2_SPAWN_X: 100,
     TURTLE2_SPAWN_Y: 275,
     TURTLE2_INTERVAL: 165,
     TURTLE2_VEL: -7,
     LEVEL2_TURTLE2_VEL: 7,
     //crocodile
     CROCODILE_COUNT:1,
     CROCODILE_HEIGHT: 25,
     CROCODILE_WIDTH: 125,
     CROCODILE_SPAWN_X: 20,
     CROCODILE_SPAWN_Y: 245,
     CROCODILE_INTERVAL: 100,
     CROCODILE_VEL: 5,
     CROCODILE_BACK: 80,
     //game over text
     GAME_OVER_X: 100,
     GAME_OVER_Y: 300,
     //game clear text
     GAME_CLEAR_X: 100,
     GAME_CLEAR_Y: 300,
     //restart text
     RESTART_X: 250,
     RESTART_Y: 320
 
   } as const
 
   //the game has the following view element types:
   type ViewType = 'frog' | 'femalefrog' | 'car1' | 'car2' | 'car3' | 'racecar' | 'truck' | 'log1' | 'log2' | 'log3' | 'turtle1' | 'turtle2' | 'crocodile'
 
   //three types of game state transitions
   class Tick { constructor(public readonly elapsed:number) {} }
   class Move { constructor(public readonly x:number, public readonly y:number) {} }
   class Restart { constructor() {} }
  
   const 
    gameClock = interval(100)
     .pipe(map(elapsed=>new Tick(elapsed))),
 
     /** 
      * Adapted from Tim's Asteroids code.
      */
     keyObservable = <T>(e:Event, k:Key, result:()=>T)=>
       fromEvent<KeyboardEvent>(document,e)
         .pipe(
           filter((e)=>e.key === k),
           filter(({repeat})=>!repeat),
           map(result)),
 
 
     moveUp$ = keyObservable('keydown', 'w', () => new Move(0, -CONSTANTS.MOVE_Y)),
     moveDown$ = keyObservable('keydown', 's', () => new Move(0, CONSTANTS.MOVE_Y)),
     moveLeft$ = keyObservable('keydown', 'a', () => new Move(-CONSTANTS.MOVE_X, 0)),
     moveRight$ = keyObservable('keydown', 'd', () => new Move(CONSTANTS.MOVE_X, 0)),
     restart = keyObservable('keydown','r', () => new Restart())
   
   type Rect = Readonly<{pos_x:number, pos_y:number, width:number, height:number, vel:number}>
   type ObjectId = Readonly<{id:string, createTime:number}>
   interface IBody extends Rect, ObjectId{
     viewType: ViewType
   }
 
   // Every object that participates in collisions is a Body
   type Body = Readonly<IBody>
 
   type State = {
     time: number
     score: number
     hiscore: number
     level: number
     frog: Body
     femalefrog: Body
     lives: number
     cars1: ReadonlyArray<Body>
     cars2: ReadonlyArray<Body>
     cars3: ReadonlyArray<Body>
     racecars: ReadonlyArray<Body>
     trucks: ReadonlyArray<Body>
     turtles1: ReadonlyArray<Body>
     logs1: ReadonlyArray<Body>
     logs2: ReadonlyArray<Body>
     turtles2: ReadonlyArray<Body>
     logs3: ReadonlyArray<Body>
     crocs: ReadonlyArray<Body>
     goal1: boolean
     goal2: boolean
     goal3: boolean
     goal4: boolean
     goal5: boolean
     carryfemale: boolean
     gameOver: boolean
     stage1Clear: boolean
     gameClear: boolean
     restart: boolean
   }
 
   //cars, logs and turtles are just rectangles
     const createRectangles = (viewType: ViewType)=> (oid:ObjectId)=> (rect:Rect)=>
     <Body>{
       ...oid,
       ...rect,
       id: viewType+oid.id,
       viewType: viewType
     },
     createCar1 = createRectangles('car1'),
     createCar2 = createRectangles('car2'),
     createCar3 = createRectangles('car3'),
     createRaceCar = createRectangles('racecar'),
     createTruck = createRectangles('truck'),
     createTurtle1 = createRectangles('turtle1'),
     createLog1 = createRectangles('log1'),
     createLog2 = createRectangles('log2'),
     createTurtle2 = createRectangles('turtle2'),
     createLog3 = createRectangles('log3'),
     createCrocs = createRectangles('crocodile')
 
 
     function createFrog():Body{
       return {
         id:'frog',
         viewType:'frog',
         pos_x:CONSTANTS.FROG_SPAWN_X,
         pos_y:CONSTANTS.FROG_SPAWN_Y,
         width:CONSTANTS.FROG_WIDTH,
         height:CONSTANTS.FROG_HEIGHT,
         createTime:CONSTANTS.START_TIME,
         vel:CONSTANTS.FROG_VEL
       }
     }
 
     function createFemaleFrog():Body{
       return {
         id:'femalefrog',
         viewType:'femalefrog',
         pos_x:CONSTANTS.FEMALE_FROG_SPAWN_X,
         pos_y:CONSTANTS.FEMALE_FROG_SPAWN_Y,
         width:CONSTANTS.FROG_WIDTH,
         height:CONSTANTS.FROG_HEIGHT,
         createTime:CONSTANTS.START_TIME,
         vel:CONSTANTS.FROG_VEL
       }
     }
 
     function createObjList(createfunc:(oid:ObjectId)=> (rect:Rect)=>Body, objcount:number, objspawn_x:number, objspawn_y:number, objheight:number, objwidth:number, objvel:number, obj_interval:number):Array<Body>{
       return [...Array(objcount)]
               .map((_,i) => createfunc({id:String(i),createTime:CONSTANTS.START_TIME})
                                       ({pos_x:objspawn_x + i*obj_interval, pos_y:objspawn_y, height:objheight, width:objwidth, vel:objvel}))
     }
 
     const
       startCars1 = createObjList(createCar1, CONSTANTS.START_CAR1_COUNT, CONSTANTS.CAR1_SPAWN_X, CONSTANTS.CAR1_SPAWN_Y, CONSTANTS.CAR1_HEIGHT, CONSTANTS.CAR1_WIDTH, CONSTANTS.CAR1_VEL, CONSTANTS.CAR1_INTERVAL),
       startCars2 = createObjList(createCar2, CONSTANTS.START_CAR2_COUNT, CONSTANTS.CAR2_SPAWN_X, CONSTANTS.CAR2_SPAWN_Y, CONSTANTS.CAR2_HEIGHT, CONSTANTS.CAR2_WIDTH, CONSTANTS.CAR2_VEL, CONSTANTS.CAR2_INTERVAL),
       startCars3 = createObjList(createCar3, CONSTANTS.START_CAR3_COUNT, CONSTANTS.CAR3_SPAWN_X, CONSTANTS.CAR3_SPAWN_Y, CONSTANTS.CAR3_HEIGHT, CONSTANTS.CAR3_WIDTH, CONSTANTS.CAR3_VEL, CONSTANTS.CAR3_INTERVAL),
       startRaceCar =  createObjList(createRaceCar, CONSTANTS.START_RACECAR_COUNT, CONSTANTS.RACECAR_SPAWN_X, CONSTANTS.RACECAR_SPAWN_Y, CONSTANTS.RACECAR_HEIGHT, CONSTANTS.RACECAR_WIDTH, CONSTANTS.RACECAR_VEL, CONSTANTS.RACECAR_INTERVAL),
       level2RaceCar =  createObjList(createRaceCar, CONSTANTS.LEVEL2_RACECAR_COUNT, CONSTANTS.RACECAR_SPAWN_X, CONSTANTS.RACECAR_SPAWN_Y, CONSTANTS.RACECAR_HEIGHT, CONSTANTS.RACECAR_WIDTH, CONSTANTS.LEVEL2_RACECAR_VEL, CONSTANTS.RACECAR_INTERVAL),
       startTruck = createObjList(createTruck, CONSTANTS.START_TRUCK_COUNT, CONSTANTS.TRUCK_SPAWN_X, CONSTANTS.TRUCK_SPAWN_Y, CONSTANTS.TRUCK_HEIGHT, CONSTANTS.TRUCK_WIDTH, CONSTANTS.TRUCK_VEL, CONSTANTS.TRUCK_INTERVAL),
       
       startLogs1 = createObjList(createLog1, CONSTANTS.START_LOG1_COUNT, CONSTANTS.LOG1_SPAWN_X, CONSTANTS.LOG1_SPAWN_Y, CONSTANTS.LOG1_HEIGHT, CONSTANTS.LOG1_WIDTH, CONSTANTS.LOG1_VEL, CONSTANTS.LOG1_INTERVAL),
       startLogs2 = createObjList(createLog2, CONSTANTS.START_LOG2_COUNT, CONSTANTS.LOG2_SPAWN_X, CONSTANTS.LOG2_SPAWN_Y, CONSTANTS.LOG2_HEIGHT, CONSTANTS.LOG2_WIDTH, CONSTANTS.LOG2_VEL, CONSTANTS.LOG2_INTERVAL),
       startLogs3 = createObjList(createLog3, CONSTANTS.START_LOG3_COUNT, CONSTANTS.LOG3_SPAWN_X, CONSTANTS.LOG3_SPAWN_Y, CONSTANTS.LOG3_HEIGHT, CONSTANTS.LOG3_WIDTH, CONSTANTS.LOG3_VEL, CONSTANTS.LOG3_INTERVAL),
       level2Logs3 = createObjList(createLog3, CONSTANTS.LEVEL2_LOG3_COUNT, CONSTANTS.LEVEL2_LOG3_SPAWN_X, CONSTANTS.LOG3_SPAWN_Y, CONSTANTS.LOG3_HEIGHT, CONSTANTS.LOG3_WIDTH, CONSTANTS.LOG3_VEL, CONSTANTS.LOG3_INTERVAL),
       level2crocodiles = createObjList(createCrocs, CONSTANTS.CROCODILE_COUNT, CONSTANTS.CROCODILE_SPAWN_X, CONSTANTS.CROCODILE_SPAWN_Y, CONSTANTS.CROCODILE_HEIGHT, CONSTANTS.CROCODILE_WIDTH, CONSTANTS.CROCODILE_VEL, CONSTANTS.CROCODILE_INTERVAL),
 
       startTurtles1 = createObjList(createTurtle1, CONSTANTS.START_TURTLE1_COUNT, CONSTANTS.TURTLE1_SPAWN_X, CONSTANTS.TURTLE1_SPAWN_Y, CONSTANTS.TURTLE1_HEIGHT, CONSTANTS.TURTLE1_WIDTH, CONSTANTS.TURTLE1_VEL, CONSTANTS.TURTLE1_INTERVAL),
       startTurtles2 = createObjList(createTurtle2, CONSTANTS.START_TURTLE2_COUNT, CONSTANTS.TURTLE2_SPAWN_X, CONSTANTS.TURTLE2_SPAWN_Y, CONSTANTS.TURTLE2_HEIGHT, CONSTANTS.TURTLE2_WIDTH, CONSTANTS.TURTLE2_VEL, CONSTANTS.TURTLE2_INTERVAL),
 
       initialState:State = {
       time: CONSTANTS.START_TIME,
       score: CONSTANTS.START_SCORE,
       hiscore: CONSTANTS.HISCORE,
       level: CONSTANTS.START_LEVEL,
       frog: createFrog(),
       femalefrog: createFemaleFrog(),
       lives: CONSTANTS.START_LIVES,
       cars1: startCars1,
       cars2: startCars2,
       cars3: startCars3,
       racecars: startRaceCar,
       trucks: startTruck,
       turtles1: startTurtles1,
       logs1: startLogs1,
       logs2: startLogs2,
       turtles2: startTurtles2,
       logs3: startLogs3,
       crocs: [],
       goal1: false,
       goal2: false,
       goal3: false,
       goal4: false,
       goal5: false,
       carryfemale: false,
       gameOver: false,
       stage1Clear: false,
       gameClear: false,
       restart: false
     },
 
       level2:State = {
       time: CONSTANTS.START_TIME,
       score: CONSTANTS.START_SCORE,
       hiscore: CONSTANTS.HISCORE,
       level: CONSTANTS.LEVEL2,
       frog: createFrog(),
       femalefrog: createFemaleFrog(),
       lives: CONSTANTS.START_LIVES,
       cars1: startCars1,
       cars2: startCars2,
       cars3: startCars3,
       racecars: level2RaceCar,
       trucks: startTruck,
       turtles1: startTurtles1,
       logs1: startLogs1,
       logs2: startLogs2,
       turtles2: startTurtles2,
       logs3: level2Logs3,
       crocs: level2crocodiles,
       goal1: false,
       goal2: false,
       goal3: false,
       goal4: false,
       goal5: false,
       carryfemale: false,
       gameOver: false,
       stage1Clear: true,
       gameClear: false,
       restart: false
       },
     
       //wrap positions around edges of screen
       s = CONSTANTS.CANVAS_SIZE,
       wrap = (v:number) => (width:number) => { return v+width < 0 ? v+width + s : v > s ? v-width - s : v},
 
       //limit the frog's movement to the edge of screen 
       limitx = (v:number) => { 
         return v < CONSTANTS.FROG_WIDTH ? 0 : v > s-CONSTANTS.FROG_WIDTH ? s-CONSTANTS.FROG_WIDTH : v
       },
       limity = (v:number) => { return v < CONSTANTS.FROG_HEIGHT ? 0 : v > s-CONSTANTS.FROG_HEIGHT ? s-CONSTANTS.FROG_HEIGHT : v},
 
       // all movement comes through here
       moveBody = (object:Body) => <Body>{
         ...object,
         pos_x: wrap(object.pos_x + object.vel)(object.width),
       },
 
       // frog cannot wrap around edges of the map, so it has a different movement logic
       moveFrog = (object:Body) => <Body>{
         ...object,
         pos_x: limitx(object.pos_x + object.vel),
       },
 
       handleCollisions = (state:State) => {
         const 
           //check whether a is to the left of b, apply appropriate collision calculation
           bodiesCollided = ([frog,car]: [Body, Body]) => frog.pos_y === car.pos_y && (frog.pos_x-car.pos_x > 0 ? frog.pos_x-car.pos_x <= car.width : car.pos_x-frog.pos_x <= frog.width),
           crocCollided = ([frog,croc]: [Body, Body]) => frog.pos_y === croc.pos_y && frog.pos_x-croc.pos_x > 0 && (frog.pos_x-croc.pos_x) >= CONSTANTS.CROCODILE_BACK,
           frogCollided = state.cars1.filter(c => bodiesCollided([state.frog,c])).length > 0 
                           || state.cars2.filter(c => bodiesCollided([state.frog,c])).length > 0
                           || state.cars3.filter(c => bodiesCollided([state.frog,c])).length > 0
                           || state.racecars.filter(c => bodiesCollided([state.frog,c])).length > 0
                           || state.trucks.filter(c => bodiesCollided([state.frog,c])).length > 0
                           || state.crocs.filter(c => crocCollided([state.frog,c])).length > 0,
 
           //checking for turtle collision in stage 2 mechanics
           turtleCollided = ([frog,turtle]: [Body, Body]) => frog.pos_y === turtle.pos_y && frog.pos_x-turtle.pos_x < turtle.width && frog.pos_x-turtle.pos_x >= 0,
           frogOnTurtle1 = state.turtles1.filter(t => turtleCollided([state.frog,t])).length > 0,
           frogOnTurtle2 = state.turtles2.filter(t => turtleCollided([state.frog,t])).length > 0,
 
           //check whether the frog is on a log, apply appriopriate movement to frog (i.e. gives the frog the same velocity as the log)
           frogOnLog = ([frog,log]: [Body, Body]) => frog.pos_y === log.pos_y && frog.pos_x-log.pos_x < log.width && frog.pos_x-log.pos_x >= 0,
           carryFrog = state.turtles1.filter(l => frogOnLog([state.frog,l])).length > 0 
                       ? state.turtles1[0].vel
                       : state.logs1.filter(l => frogOnLog([state.frog,l])).length > 0 
                       ? state.logs1[0].vel
                       : state.logs2.filter(l => frogOnLog([state.frog,l])).length > 0 
                       ? state.logs2[0].vel
                       : state.turtles2.filter(l => frogOnLog([state.frog,l])).length > 0 
                       ? state.turtles2[0].vel
                       : state.logs3.filter(l => frogOnLog([state.frog,l])).length > 0 
                       ? state.logs3[0].vel
                       : state.crocs.filter(l => frogOnLog([state.frog,l])).length > 0
                       ? state.crocs[0].vel
                       : 0,
 
           //check whether the frog reaches a goal
           frogInGoal1 = state.frog.pos_y === CONSTANTS.GOAL1_Y && Math.abs(state.frog.pos_x - CONSTANTS.GOAL1_X) < state.frog.width,
           frogInGoal2 = state.frog.pos_y === CONSTANTS.GOAL2_Y && Math.abs(state.frog.pos_x - CONSTANTS.GOAL2_X) < state.frog.width,
           frogInGoal3 = state.frog.pos_y === CONSTANTS.GOAL3_Y && Math.abs(state.frog.pos_x - CONSTANTS.GOAL3_X) < state.frog.width,
           frogInGoal4 = state.frog.pos_y === CONSTANTS.GOAL4_Y && Math.abs(state.frog.pos_x - CONSTANTS.GOAL4_X) < state.frog.width,
           frogInGoal5 = state.frog.pos_y === CONSTANTS.GOAL5_Y && Math.abs(state.frog.pos_x - CONSTANTS.GOAL5_X) < state.frog.width,
           frogGoaled = frogInGoal1 || frogInGoal2 || frogInGoal3 || frogInGoal4 || frogInGoal5,
 
           //calculating the score, if a goal is already filled, it yields 0 points.
           score = frogInGoal1 ? state.goal1 ? 0 : bodiesCollided([state.frog, state.femalefrog]) ? 700 : 500 
                   : frogInGoal2 ? state.goal2 ? 0 : bodiesCollided([state.frog, state.femalefrog]) ? 700 : 500 
                   : frogInGoal3 ? state.goal3 ? 0 : bodiesCollided([state.frog, state.femalefrog]) ? 700 : 500 
                   : frogInGoal4 ? state.goal4 ? 0 : bodiesCollided([state.frog, state.femalefrog]) ? 700 : 500 
                   : frogInGoal5 ? state.goal5 ? 0 : bodiesCollided([state.frog, state.femalefrog]) ? 700 : 500 
                   : 0,
 
           //check whether the frog is in the river section
           frogInWater = state.frog.pos_y < 395 && !frogGoaled,
 
           //check whether the frog is dead
           frogDead = frogCollided || (carryFrog === 0 && frogInWater),
 
           //check whether to move on to the next stage
           stage1cleared = state.level === 1 && state.goal1 && state.goal2 && state.goal3 && state.goal4 && state.goal5
                           
         return stage1cleared ? {...level2, score:state.score, lives:state.lives} : {...state,
         frog: (frogGoaled || frogDead) ? createFrog() : {...state.frog, vel:carryFrog},
         femalefrog: state.carryfemale ? {...state.femalefrog, vel:carryFrog} : state.femalefrog,
         lives: frogDead ? state.lives - 1 : state.lives,
         turtles1: state.level == 2 && frogOnTurtle1 ? state.turtles1.map(t => <Body>{...t, vel:CONSTANTS.LEVEL2_TURTLE1_VEL}) : state.turtles1.map(t => <Body>{...t, vel:CONSTANTS.TURTLE1_VEL}),
         turtles2:  state.level == 2 && frogOnTurtle2 ? state.turtles2.map(t => <Body>{...t, vel:CONSTANTS.LEVEL2_TURTLE1_VEL}) : state.turtles2.map(t => <Body>{...t, vel:CONSTANTS.TURTLE2_VEL}),
         goal1: frogInGoal1 ? true : state.goal1,
         goal2: frogInGoal2 ? true : state.goal2,
         goal3: frogInGoal3 ? true : state.goal3,
         goal4: frogInGoal4 ? true : state.goal4,
         goal5: frogInGoal5 ? true : state.goal5,
         score: state.score + score, 
         carryfemale: bodiesCollided([state.frog, state.femalefrog]),
         gameOver: state.lives == 0,
         stage1clear: state.level == 1 && stage1cleared,
         gameClear: state.level == 2 && state.goal1 && state.goal2 && state.goal3 && state.goal4 && state.goal5}
       },
 
       
 
       tick = (state:State,elapsed:number) => {
         return handleCollisions({...state,
         frog: moveFrog(state.frog),
         femalefrog: moveFrog(state.femalefrog),
         cars1: state.cars1.map(moveBody),
         cars2: state.cars2.map(moveBody),
         cars3: state.cars3.map(moveBody),
         racecars: state.racecars.map(moveBody),
         trucks: state.trucks.map(moveBody),
         turtles1: state.turtles1.map(moveBody),
         logs1: state.logs1.map(moveBody),
         logs2: state.logs2.map(moveBody),
         turtles2: state.turtles2.map(moveBody),
         logs3: state.logs3.map(moveBody),
         crocs: state.crocs.map(moveBody),
         time: elapsed})
       },
 
     reduceState = (state:State, event:Move|Tick|Restart) =>
       event instanceof Move ? {...state,
         frog: {...state.frog, pos_x: limitx(state.frog.pos_x + event.x), pos_y: limity(state.frog.pos_y + event.y)},
         femalefrog: state.carryfemale ? {...state.femalefrog, pos_x: limitx(state.frog.pos_x + event.x), pos_y: limity(state.frog.pos_y + event.y)} : state.femalefrog,
         score: event.y < 0 ? state.score + 10 : state.score
       } 
       : event instanceof Restart ? {...initialState, 
         hiscore: state.score > state.hiscore ? state.score : state.hiscore,
         restart: true}
       : tick({...state, restart:false}, event.elapsed) 
 
     function updateView(state:State){
       const
         svg_b = document.getElementById("backgroundLayer")!,
         svg_f = document.getElementById("foregroundLayer")!,
         frog = document.getElementById("frog")!,
         femalefrog = document.getElementById("femalefrog")!,
         result = document.getElementById("res")!,
         hiscore = document.getElementById("res2")!,
         goal5 = document.getElementById("goal5")!,
         goal4 = document.getElementById("goal4")!,
         goal3 = document.getElementById("goal3")!,
         goal2 = document.getElementById("goal2")!,
         goal1 = document.getElementById("goal1")!,
         level = document.getElementById("level")!,
         life5 = document.getElementById("life5")!,
         life4 = document.getElementById("life4")!,
         life3 = document.getElementById("life3")!,
         life2 = document.getElementById("life2")!,
         life1 = document.getElementById("life1")!,
         updateBodyView = (b:Body) => {
           function createBodyView() {
             const v = document.createElementNS(svg_b.namespaceURI, "rect")!;
             attr(v,{id:b.id, height:b.height, width:b.width});
             v.classList.add(b.viewType)
             svg_b.appendChild(v)
             return v;
           }
           const v = document.getElementById(b.id) || createBodyView();
           attr(v,{x:b.pos_x, y:b.pos_y});
         };
         
         attr(frog,{x:`${state.frog.pos_x}`, y:`${state.frog.pos_y}`});
         attr(femalefrog,{x:`${state.femalefrog.pos_x}`, y:`${state.femalefrog.pos_y}`});
         state.cars1.forEach(updateBodyView);
         state.cars2.forEach(updateBodyView);
         state.cars3.forEach(updateBodyView);
         state.racecars.forEach(updateBodyView);
         state.trucks.forEach(updateBodyView);
         state.turtles1.forEach(updateBodyView);
         state.logs1.forEach(updateBodyView);
         state.logs2.forEach(updateBodyView);
         state.turtles2.forEach(updateBodyView);
         state.logs3.forEach(updateBodyView);
         state.crocs.forEach(updateBodyView);
 
         //update the score
         result.textContent = String(state.score)
         hiscore.textContent = String(state.hiscore)
 
         //update the current level
         level.textContent = "Level: " + String(state.level)
 
         //lets the player know which goal they have already put a frog in
         if(state.goal1){
             attr(goal1,{style:"fill:green"});
           }
         
 
         if(state.goal2){
             attr(goal2,{style:"fill:green"});
           }
         
 
         if(state.goal3){
             attr(goal3,{style:"fill:green"});
           }
         
 
         if(state.goal4){
             attr(goal4,{style:"fill:green"});
           }
         
 
         if(state.goal5){
             attr(goal5,{style:"fill:green"});
           }
         
 
         //update the lives of the frog on display
         if(state.lives == 4){
           attr(life5,{style:"fill:black"});
           }
         else if(state.lives == 3){
           attr(life4,{style:"fill:black"});
           }
         else if(state.lives == 2){
           attr(life3,{style:"fill:black"});
           }
         else if(state.lives == 1){
           attr(life2,{style:"fill:black"});
           }
         else if(state.lives == 0){
           attr(life1,{style:"fill:black"});
           }
         
         
         //remove the log from view to be replaced by a crocodile
         if(state.level == 2){
           const log = document.getElementById(initialState.logs3[2].id)
           if (log != null) {svg_b.removeChild(log)}
         }
 
         //resets the goals to original display
         function resetGoal(){
           const 
             goal1 = document.getElementById("goal1")!,
             goal2 = document.getElementById("goal2")!,
             goal3 = document.getElementById("goal3")!,
             goal4 = document.getElementById("goal4")!,
             goal5 = document.getElementById("goal5")!;
           attr(goal1,{style:"fill:aqua"});
           attr(goal2,{style:"fill:aqua"});
           attr(goal3,{style:"fill:aqua"});
           attr(goal4,{style:"fill:aqua"});
           attr(goal5,{style:"fill:aqua"});
           state.stage1Clear = false;
         }
 
         function resetLives(){
           const
             life5 = document.getElementById("life5")!,
             life4 = document.getElementById("life4")!,
             life3 = document.getElementById("life3")!,
             life2 = document.getElementById("life2")!,
             life1 = document.getElementById("life1")!
 
           attr(life1,{style:"fill:green"});
           attr(life2,{style:"fill:green"});
           attr(life3,{style:"fill:green"});
           attr(life4,{style:"fill:green"});
           attr(life5,{style:"fill:green"});
         }
 
         function restartGame(state:State){
           resetGoal();
           resetLives();
           function removeBodyView(b: Body){
             const v = document.getElementById(b.id)!;
             svg_b.removeChild(v);
             }
           state.cars1.forEach(removeBodyView);
           state.cars2.forEach(removeBodyView);
           state.cars3.forEach(removeBodyView);
           state.racecars.forEach(removeBodyView);
           state.trucks.forEach(removeBodyView);
           state.turtles1.forEach(removeBodyView);
           state.logs1.forEach(removeBodyView);
           state.logs2.forEach(removeBodyView);
           state.turtles2.forEach(removeBodyView);
           state.logs3.forEach(removeBodyView);
           state.crocs.forEach(removeBodyView);
           removeBodyView(state.frog);
           removeBodyView(state.femalefrog);
         }
 
         if(state.stage1Clear){
           resetGoal();
         }
 
         if(state.restart){
           resetGoal();
           resetLives();
         }
 
         if(state.gameOver) {
           const 
             display = document.createElementNS(svg_b.namespaceURI, "rect")!,
             v = document.createElementNS(svg_b.namespaceURI, "text")!,
             r = document.createElementNS(svg_b.namespaceURI, "text")!;
 
           attr(display,{x:CONSTANTS.DISPLAY_X,y:CONSTANTS.DISPLAY_Y,height:CONSTANTS.DISPLAY_HEIGHT,width:CONSTANTS.DISPLAY_WIDTH,class:"messagebackground"});
           svg_f.appendChild(display);
           
           attr(v,{x:CONSTANTS.GAME_OVER_X,y:CONSTANTS.GAME_OVER_Y,class:"gameover"});
           v.textContent = "Game Over";
           svg_f.appendChild(v);
           
           attr(r,{x:CONSTANTS.RESTART_X,y:CONSTANTS.RESTART_Y,class:"restart"});
           r.textContent = "press R to restart";
           svg_f.appendChild(r);
 
           //restart the game
           const restart = keyObservable('keydown','r', () => {svg_f.removeChild(display); svg_f.removeChild(v); svg_f.removeChild(r);});
           restart.subscribe(() => restartGame(state));
           
         } 
         else if (state.gameClear) {
           const 
             display = document.createElementNS(svg_b.namespaceURI, "rect")!,
             v = document.createElementNS(svg_b.namespaceURI, "text")!,
             r = document.createElementNS(svg_b.namespaceURI, "text")!;
 
           attr(display,{x:CONSTANTS.DISPLAY_X,y:CONSTANTS.DISPLAY_Y,height:CONSTANTS.DISPLAY_HEIGHT,width:CONSTANTS.DISPLAY_WIDTH,class:"messagebackground"});
           svg_f.appendChild(display);
 
           attr(v,{x:CONSTANTS.GAME_CLEAR_X,y:CONSTANTS.GAME_CLEAR_Y,class:"gameclear"});
           v.textContent = "Game Clear";
           svg_f.appendChild(v);
           
           attr(r,{x:CONSTANTS.RESTART_X,y:CONSTANTS.RESTART_Y,class:"restart"});
           r.textContent = "press R to restart";
           svg_f.appendChild(r);
           
           //restart the game
           const restart = keyObservable('keydown','r', () => {svg_f.removeChild(display); svg_f.removeChild(v); svg_f.removeChild(r)});
           restart.subscribe(() => restartGame(state));
         }
 
             
     }
     
   //Main game stream
   merge(gameClock, moveUp$, moveDown$, moveLeft$, moveRight$, restart)
     .pipe(
       scan(reduceState, initialState))
     .subscribe(updateView);
 }
 
 function showKeys() {
   function showKey(k:Key) {
     const directionKey = document.getElementById(k)!,
       o = (e:Event) => fromEvent<KeyboardEvent>(document,e).pipe(
         filter((e)=>e.key === k))
     o('keydown').subscribe(_ => directionKey.classList.add("highlight"))
     o('keyup').subscribe(_=>directionKey.classList.remove("highlight"))
   }
   showKey('w');
   showKey('a');
   showKey('s');
   showKey('d');
   showKey('r')
 }
 
 setTimeout(showKeys, 0)
 
 //Utility functions
 type Object = Readonly<{ [k:string] : unknown}>
 const
 /** Adapted from Tim's Asteroids code
  * 
  * set a number of attributes on an Element at once
  * @param e the Element
  * @param o a property bag
  */         
  attr = (e:Element,o:Object) =>
  { for(const k in o) e.setAttribute(k,String(o[k])) }
 
 
 
 // The following simply runs your main function on window load.  Make sure to leave it in place.
 if (typeof window !== "undefined") {
   window.onload = () => {
     main();
   };
 }
 