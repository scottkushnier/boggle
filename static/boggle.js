const wordList = [];

async function checkWordOnBoggleServer(word) {
  const res = await axios({
    method: "get",
    url: "http://localhost:5000/boggle/check-word/",
    params: { word: word },
  });
  return res.data;
}

// use JQuery axios.get function to check word
async function checkWordOnBoggleServerJ(word) {
  try {
    const res = await axios.get("http://localhost:5000/boggle/check-word/", {
      params: { word: word },
    });
    return res.data;
  } catch {
    console.log(error);
    return null;
  }
}

function addWordToListOnPage(word, first) {
  if (first) {
    $("#wordlist").prepend("<h2>Word List</h2>");
  }
  $("#word-list-items").append(`<li> ${word} </li>`);
}

function wordScore(word) {
  const len = word.length;
  // console.log("word:", word, "len:", len);
  let score = 0;
  if (len == 3 || len == 4) {
    score = 1;
  } else if (len == 5) {
    score = 2;
  } else if (len == 6) {
    score = 3;
  } else if (len == 7) {
    score = 5;
  } else if (len > 7) {
    score = 11;
  }
  return score;
}

function computeScore(wordList) {
  let sum = 0;
  for (word of wordList) {
    sum += wordScore(word);
  }
  return sum;
}

// given word submitted by user, see if valid & update game
async function tryWord(evt) {
  evt.preventDefault();
  const word = $("#word").val();
  let checkMsg = false;
  // allows words with lengths 1 (a & I) or 2, but no points awarded
  if (word.length < 1) {
    return;
  } else if (word.length == 1) {
    if (word != "a" && word != "i") {
      checkMsg = "not-word";
    }
  }
  // check for repeated words
  if (wordList.includes(word)) {
    checkMsg = "repeat";
  }
  if (!checkMsg) {
    checkMsg = await checkWordOnBoggleServerJ(word);
  }
  // construct readable message reflecting status of inputted word
  let msg;
  if (checkMsg == "ok") {
    msg = `Validated "${word}".`;
    wordList.push(word);
    if (wordList.length == 1) {
      addWordToListOnPage(word, (first = true));
    } else {
      addWordToListOnPage(word);
    }
    $("#score").text("Score: " + computeScore(wordList));
    // console.log("wordList: ", wordList);
  } else if (checkMsg == "not-on-board") {
    msg = `Sorry, not on board: "${word}".`;
  } else if (checkMsg == "not-word") {
    msg = `No such word: "${word}".`;
  } else if (checkMsg == "repeat") {
    msg = `Already used: "${word}".`;
  } else {
    msg = `Improper response from Boggle server for word: "${word}".`;
  }
  const msgElement = $("#msg");
  msgElement.text(msg);
  $("#word").val(""); // reset word input form for next word to be entered
}

$("#word-submit").on("submit", tryWord);

async function getGameStats() {
  const res = await axios.get(
    "http://localhost:5000/boggle/get-game-stats/",
    {}
  );
  console.log(res.data);
  return res.data;
}

async function submitScore(score) {
  json = JSON.stringify({ score: score });
  try {
    const res = await axios.post(
      "http://localhost:5000/boggle/post-game-stats/",
      json,
      { headers: { "Content-Type": "application/json" } }
    );
    return res.data;
  } catch {
    return null;
  }
}

// timer

let timeLeft;
let timer;

async function endGame() {
  $("#time-remaining").text("Game Over");
  clearInterval(timer);
  // deselect input field & show as inactive
  document.getElementById("word").blur();
  document
    .getElementById("word")
    .setAttribute("placeholder", "-- GAME OVER --");
  document.getElementById("word").setAttribute("disabled", true);
  const score = computeScore(wordList);
  await submitScore(score); // tell server about game that's now done
}

async function updateTimer() {
  if (timeLeft > 0) {
    // console.log("time left: ", timeLeft);
    timeLeft--;
    $("#time-left").text(timeLeft);
  }
  if (timeLeft == 0) {
    await endGame();
  }
}

function startTimer(maxTime) {
  timeLeft = maxTime;
  timer = setInterval(updateTimer, 1000);
}

async function postGameStats() {
  stats = await getGameStats();
  console.log(stats);
  $("#game-num").text(stats["num_games"] + 1);
  $("#high-score").text(stats["high_score"]);
}

startTimer(60);
postGameStats();

// automatically focus on word entry text area
document.getElementById("word").focus();
