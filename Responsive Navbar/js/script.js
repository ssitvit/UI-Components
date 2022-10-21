let x = document.getElementById("logo");
let flag = 1;
function showMenu() {
  if (flag == 1) {
    document.getElementById("menu").style.display = "none";
    flag = 0;
  } else {
    document.getElementById("menu").style.display = "block";
    flag = 1;
  }
}
