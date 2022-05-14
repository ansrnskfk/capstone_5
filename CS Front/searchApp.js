const toDoForm = document.querySelector('#todo-form');
const toDoInput = toDoForm.querySelector('input');
const toDoList = document.querySelector('#todo-list');
const allDelete = document.querySelector('.allDelete');
const txt = document.querySelector('.txt');
const TODOS_KEY = "todos";

let toDos = new Array();

function saveToDos() { //item을 localStorage에 저장합니다.
    typeof(Storage) !== 'undefined' && localStorage.setItem(TODOS_KEY, JSON.stringify(toDos));
};

function allDeleteToDo() { //전체 item을 삭제
    localStorage.clear(toDos);
    toDoList.innerText = '최근검색어 내역이 없습니다.';
};

function deleteToDo(e) { //각각의 item을 삭제
    const li = e.target.parentElement;
    li.remove();
    toDos = toDos.filter((toDo) => toDo.id !== parseInt(li.id));
    toDos.length === 0 && (txt.innerText = '최근검색어 내역이 없습니다.')
    saveToDos();
};

function paintToDo(newTodo) { //화면에 뿌림
    const {id, text} = newTodo;
    const item = document.createElement("li");
    const span = document.createElement("span");
    const button = document.createElement("button");
    item.id = id;
    span.innerText = text;
    button.innerText = '❌';
    button.addEventListener("click", deleteToDo);
    allDelete.addEventListener("click", allDeleteToDo);
    item.appendChild(span);
    item.appendChild(button);
    toDoList.appendChild(item);
    newTodo !== null && allDelete.classList.remove('off');
};

function handleToDoSubmit(event) { //form 전송
    event.preventDefault();
    const newTodoItem = toDoInput.value;
    toDoInput.value = '';
    const newTodoObj = {
        id: Date.now(),
        text: newTodoItem
    };
    toDos.push(newTodoObj);
    paintToDo(newTodoObj);
    saveToDos();
};

toDoForm.addEventListener('submit', handleToDoSubmit);

const savedToDos = JSON.parse(localStorage.getItem(TODOS_KEY));
if(savedToDos !== null) {
    toDos = savedToDos //전에 있던 items들을 계속 가지도 있다록 합니다. 
    savedToDos.forEach(paintToDo);
}