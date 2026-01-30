'use strict';

const WORDS = [
  'APPLE','BRAIN','CHAIR','DANCE','EAGLE','FLAME','GRACE','HEART','IMAGE','JUDGE',
  'KNIFE','LIGHT','MOUSE','NOBLE','OCEAN','PAINT','QUEST','RIVER','STONE','TABLE',
  'UNDER','VALVE','WATER','XENON','YOUTH','ZEBRA','ABOUT','BEACH','CROWN','DREAM'
];

let answer = '';
let board = [];
let colors = [];
let currentRow = 0;
let currentCol = 0;
let gameOver = false;

const boardEl = document.getElementById('board');
const keysEl = document.getElementById('keys');
const statusEl = document.getElementById('status');
const btnRestart = document.getElementById('btn-restart');

function init() {
  answer = WORDS[Math.floor(Math.random()*WORDS.length)];
  board = Array.from({length:6}, () => Array.from({length:5}, ()=>'');
  colors = Array.from({length:6}, () => Array.from({length:5}, ()=>'empty'));
  currentRow = 0; currentCol = 0; gameOver = false; statusEl.textContent='';
  renderBoard(); renderKeys();
}

function renderBoard(){
  boardEl.innerHTML = '';
  for(let r=0;r<6;r++){
    const rowEl = document.createElement('div'); rowEl.className='row';
    for(let c=0;c<5;c++){
      const t = document.createElement('div'); t.className='tile';
      const val = board[r][c] || '';
      t.textContent = val;
      if(r < currentRow){
        // 已提交行：顯示結果顏色
        if(colors[r][c]==='green') t.classList.add('green');
        else if(colors[r][c]==='yellow') t.classList.add('yellow');
        else t.classList.add('gray');
      } else if(r === currentRow){
        if(val) t.classList.add('filled');
      }
      rowEl.appendChild(t);
    }
    boardEl.appendChild(rowEl);
  }
}

function renderKeys(){
  keysEl.innerHTML='';
  const ACode = 'A'.charCodeAt(0);
  for(let i=0;i<26;i++){
    const ch = String.fromCharCode(ACode+i);
    const key = document.createElement('div'); key.className='key'; key.textContent = ch;
    // 若該字母被猜過（任一已提交行包含），則加上 used
    if(letterWasGuessed(ch)) key.classList.add('used');
    key.addEventListener('click', ()=>{
      handleKey(ch);
    });
    keysEl.appendChild(key);
  }
}

function letterWasGuessed(ch){
  for(let r=0;r<currentRow;r++){
    for(let c=0;c<5;c++){
      if(board[r][c]===ch) return true;
    }
  }
  // 也包含當前行已輸入的字母
  for(let c=0;c<currentCol;c++){
    if(board[currentRow][c]===ch) return true;
  }
  return false;
}

function handleKey(key){
  if(gameOver) return;
  if(key==='ENTER') return submitWord();
  if(key==='BACKSPACE') return removeLetter();
  if(/^[A-Z]$/.test(key)){
    addLetter(key);
  }
}

function addLetter(letter){
  if(currentCol<5){
    board[currentRow][currentCol]=letter;
    currentCol++;
    renderBoard();
  }
}

function removeLetter(){
  if(currentCol>0){
    currentCol--; board[currentRow][currentCol]=''; renderBoard();
  }
}

function submitWord(){
  if(currentCol<5){ statusEl.textContent='請輸入完整五個字母。'; return; }
  const guess = board[currentRow].join('');
  // 評分：先綠色
  let answerCounts = {};
  for(const ch of answer){ answerCounts[ch]=(answerCounts[ch]||0)+1; }
  // 設初始為 gray
  for(let c=0;c<5;c++) colors[currentRow][c]='gray';
  for(let c=0;c<5;c++){
    const g = board[currentRow][c];
    if(g===answer[c]){ colors[currentRow][c]='green'; answerCounts[g]--; }
  }
  for(let c=0;c<5;c++){
    const g = board[currentRow][c];
    if(colors[currentRow][c]==='gray'){
      if(answerCounts[g] && answerCounts[g]>0){ colors[currentRow][c]='yellow'; answerCounts[g]--; }
    }
  }
  renderBoard(); renderKeys();
  // 設為已猜過字母（右側格子變灰）—renderKeys 會自動處理
  if(guess===answer){ statusEl.textContent = '恭喜答對！答案：' + answer; gameOver=true; return; }
  currentRow++; currentCol=0;
  if(currentRow>=6){ statusEl.textContent = '遊戲結束，答案：' + answer; gameOver=true; renderBoard(); renderKeys(); return; }
  statusEl.textContent='';
}

// 鍵盤事件
window.addEventListener('keydown', (e)=>{
  if(gameOver) return;
  if(e.key==='Enter'){ handleKey('ENTER'); }
  else if(e.key==='Backspace'){ handleKey('BACKSPACE'); }
  else {
    const k = e.key.toUpperCase(); if(/^[A-Z]$/.test(k)) handleKey(k);
  }
});

btnRestart.addEventListener('click', ()=>init());

init();
