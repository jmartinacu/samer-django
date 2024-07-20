var mini = true;

function openSidebar() {
  const pathname = window.location.pathname;
  if (pathname === "/") {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
  }
};

function toggleSidebar() {
  if (mini) {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
    this.mini = false;
  } else {
    document.getElementById("mySidebar").style.width = "85px";
    document.getElementById("main").style.marginLeft = "85px";
    this.mini = true;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  openSidebar();
});
